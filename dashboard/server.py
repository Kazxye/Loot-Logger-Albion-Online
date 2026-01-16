"""
Dashboard Server - Flask + SocketIO
Servidor local para dashboard web em tempo real

Feito por Kazz
"""

import os
import json
import threading
import webbrowser
from datetime import datetime
from typing import List, Dict, Optional, Callable
from dataclasses import asdict

from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, emit

# Configuração Flask
template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
app.config['SECRET_KEY'] = 'loot-logger-kazz-2024'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')


class DashboardServer:
    """Servidor do Dashboard local."""
    
    def __init__(self, host: str = '127.0.0.1', port: int = 5000):
        self.host = host
        self.port = port
        self.is_running = False
        self._thread: Optional[threading.Thread] = None
        
        # Storage local de eventos
        self.loot_events: List[Dict] = []
        self.max_events = 500
        
        # Stats
        self.stats = {
            'total_loots': 0,
            'total_items': 0,
            'players_active': set(),
            'session_start': None,
            'status': 'offline'
        }
        
        # Tier service reference (será injetado)
        self.tier_service = None
        
        self._setup_routes()
        self._setup_socketio()
    
    def _setup_routes(self):
        """Configura rotas HTTP."""
        
        @app.route('/')
        def index():
            """Página principal do dashboard."""
            return render_template('index.html')
        
        @app.route('/api/loots')
        def get_loots():
            """Retorna todos os loots."""
            limit = request.args.get('limit', 100, type=int)
            offset = request.args.get('offset', 0, type=int)
            
            events = self.loot_events[offset:offset + limit]
            return jsonify({
                'loots': events,
                'total': len(self.loot_events),
                'limit': limit,
                'offset': offset
            })
        
        @app.route('/api/loots/recent')
        def get_recent_loots():
            """Retorna os loots mais recentes (para polling HTMX)."""
            limit = request.args.get('limit', 20, type=int)
            events = self.loot_events[-limit:] if self.loot_events else []
            events.reverse()  # Mais recentes primeiro
            return jsonify({'loots': events})
        
        @app.route('/api/stats')
        def get_stats():
            """Retorna estatísticas da sessão."""
            return jsonify({
                'total_loots': self.stats['total_loots'],
                'total_items': self.stats['total_items'],
                'players_active': len(self.stats['players_active']),
                'session_start': self.stats['session_start'],
                'status': self.stats['status']
            })
        
        @app.route('/api/players')
        def get_players():
            """Retorna lista de jogadores ativos."""
            return jsonify({
                'players': list(self.stats['players_active'])
            })
        
        @app.route('/api/clear', methods=['POST'])
        def clear_loots():
            """Limpa todos os loots."""
            self.loot_events.clear()
            self.stats['total_loots'] = 0
            self.stats['total_items'] = 0
            self.stats['players_active'].clear()
            socketio.emit('clear', {})
            return jsonify({'success': True})
    
    def _setup_socketio(self):
        """Configura eventos SocketIO."""
        
        @socketio.on('connect')
        def handle_connect():
            """Cliente conectado."""
            print(f"[DASHBOARD] Cliente conectado: {request.sid}")
            # Envia estado atual
            emit('stats', {
                'total_loots': self.stats['total_loots'],
                'total_items': self.stats['total_items'],
                'players_active': len(self.stats['players_active']),
                'status': self.stats['status']
            })
        
        @socketio.on('disconnect')
        def handle_disconnect():
            """Cliente desconectado."""
            print(f"[DASHBOARD] Cliente desconectado: {request.sid}")
        
        @socketio.on('request_history')
        def handle_request_history(data):
            """Cliente solicita histórico."""
            limit = data.get('limit', 50)
            events = self.loot_events[-limit:] if self.loot_events else []
            emit('history', {'loots': events})
    
    def inject_tier_service(self, tier_service):
        """Injeta o tier_service para parsing de tiers."""
        self.tier_service = tier_service
    
    def on_loot_event(self, event):
        """
        Callback para eventos de loot.
        Deve ser registrado no data_handler.
        """
        try:
            # Converte para dict serializável
            loot_data = self._serialize_loot_event(event)
            
            # Adiciona ao storage
            self.loot_events.append(loot_data)
            if len(self.loot_events) > self.max_events:
                self.loot_events = self.loot_events[-self.max_events:]
            
            # Atualiza stats
            self.stats['total_loots'] += 1
            self.stats['total_items'] += event.quantity
            self.stats['players_active'].add(event.looted_by.name)
            
            # Emite via WebSocket
            if self.is_running:
                socketio.emit('new_loot', loot_data)
                socketio.emit('stats', {
                    'total_loots': self.stats['total_loots'],
                    'total_items': self.stats['total_items'],
                    'players_active': len(self.stats['players_active']),
                    'status': self.stats['status']
                })
        
        except Exception as e:
            print(f"[DASHBOARD] Erro ao processar loot: {e}")
    
    def _serialize_loot_event(self, event) -> Dict:
        """Serializa um LootEvent para JSON."""
        # Parse tier info
        tier_info = None
        tier_display = ""
        tier_color = ""
        is_rare = False
        
        if self.tier_service:
            tier_info = self.tier_service.parse_tier(event.item_id)
            if tier_info:
                tier_display = tier_info.display_name
                tier_color = self.tier_service.get_tier_color(event.item_id)
                is_rare = tier_info.is_rare
        
        return {
            'id': f"{event.timestamp.timestamp()}-{event.item_id}-{event.looted_by.name}",
            'timestamp': event.timestamp.isoformat(),
            'timestamp_display': event.timestamp.strftime("%H:%M:%S"),
            'item_id': event.item_id,
            'item_name': event.item_name,
            'quantity': event.quantity,
            'looted_by': {
                'name': event.looted_by.name,
                'guild': event.looted_by.guild or '',
                'alliance': event.looted_by.alliance or ''
            },
            'looted_from': {
                'name': event.looted_from.name,
                'guild': event.looted_from.guild or '',
                'alliance': event.looted_from.alliance or ''
            },
            'tier': {
                'display': tier_display,
                'color': tier_color,
                'is_rare': is_rare
            }
        }
    
    def set_status(self, status: str):
        """Define status do sniffer."""
        self.stats['status'] = status
        if self.is_running:
            socketio.emit('status', {'status': status})
    
    def start(self, open_browser: bool = True):
        """Inicia o servidor em background."""
        if self.is_running:
            return
        
        # Usar timestamp com timezone para evitar bugs de fuso horário
        self.stats['session_start'] = datetime.now().isoformat()
        self.is_running = True
        
        def run_server():
            try:
                print(f"[DASHBOARD] Servidor iniciado em http://{self.host}:{self.port}")
                socketio.run(app, host=self.host, port=self.port, 
                           debug=False, use_reloader=False, allow_unsafe_werkzeug=True)
            except Exception as e:
                print(f"[DASHBOARD] Erro no servidor: {e}")
                self.is_running = False
        
        self._thread = threading.Thread(target=run_server, daemon=True)
        self._thread.start()
        
        if open_browser:
            # Aguarda servidor iniciar
            import time
            time.sleep(1)
            webbrowser.open(f"http://{self.host}:{self.port}")
    
    def stop(self):
        """Para o servidor."""
        self.is_running = False
        # Flask-SocketIO não tem método stop() direto,
        # mas como é daemon thread, será encerrado com a app


# Instância global
dashboard_server = DashboardServer()
