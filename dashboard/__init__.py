"""
Dashboard Module - Loot Logger Web Dashboard
Servidor local Flask + SocketIO para visualização em tempo real

Feito por Kazz
"""

from .server import DashboardServer, dashboard_server

__all__ = ['DashboardServer', 'dashboard_server']
