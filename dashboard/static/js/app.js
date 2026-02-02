/**
 * App.js - Main Application Entry Point
 * Loot Logger Dashboard by Kazz
 */

// ========================================
// ALPINE.JS DATA STORE
// ========================================
function dashboard() {
    return {
        // Connection state
        connected: false,
        socket: null,
        
        // Data
        loots: [],
        players: [],
        
        // Stats
        stats: {
            total_loots: 0,
            total_items: 0,
            players_active: 0,
            status: 'offline'
        },
        
        // Session
        sessionTime: '00:00:00',
        sessionStartTime: null,
        sessionInterval: null,
        
        // Filters
        filters: {
            search: '',
            tiers: [4, 5, 6, 7, 8],
            categories: ['equipment', 'consumable', 'resource', 'rune', 'other'],
            players: [],
            rareOnly: false
        },
        
        // Categories config
        categories: [
            { id: 'equipment', name: 'Equipamentos' },
            { id: 'consumable', name: 'Consumíveis' },
            { id: 'resource', name: 'Recursos' },
            { id: 'rune', name: 'Runas' },
            { id: 'other', name: 'Outros' }
        ],
        
        // Server selection for price API
        priceServers: [
            { id: 'west', name: 'Americas', url: 'west.albion-online-data.com' },
            { id: 'europe', name: 'Europe', url: 'europe.albion-online-data.com' },
            { id: 'east', name: 'Asia', url: 'east.albion-online-data.com' }
        ],
        selectedServer: 'west',
        
        // Discord Webhook
        discordWebhook: '',
        discordModalOpen: false,
        discordTesting: false,
        discordTestResult: null,
        
        // Theme
        themes: [
            { id: 'purple', name: 'Royal Purple', icon: 'palette' },
            { id: 'outlands', name: 'Outlands Orange', icon: 'paintbrush' }
        ],
        currentTheme: 'purple',
        
        // Price cache
        priceCache: {},
        
        // ========================================
        // COMPUTED PROPERTIES
        // ========================================
        
        get filteredLoots() {
            return this.loots.filter(loot => {
                // Search filter
                if (this.filters.search) {
                    const search = this.filters.search.toLowerCase();
                    const matchesSearch = 
                        loot.item_name.toLowerCase().includes(search) ||
                        loot.item_id.toLowerCase().includes(search) ||
                        loot.looted_by.name.toLowerCase().includes(search) ||
                        loot.looted_from.name.toLowerCase().includes(search);
                    if (!matchesSearch) return false;
                }
                
                // Tier filter
                if (this.filters.tiers.length > 0 && loot.tier.display) {
                    const tierMatch = loot.tier.display.match(/T(\d)/);
                    if (tierMatch) {
                        const tier = parseInt(tierMatch[1]);
                        if (!this.filters.tiers.includes(tier)) return false;
                    }
                }
                
                // Category filter
                if (this.filters.categories.length > 0) {
                    const category = this.getItemCategory(loot.item_id);
                    if (!this.filters.categories.includes(category)) return false;
                }
                
                // Player filter
                if (this.filters.players.length > 0) {
                    if (!this.filters.players.includes(loot.looted_by.name)) return false;
                }
                
                // Rare only
                if (this.filters.rareOnly && !loot.tier.is_rare) return false;
                
                return true;
            });
        },
        
        get allTiersSelected() {
            return this.filters.tiers.length === 5;
        },
        
        get allCategoriesSelected() {
            return this.filters.categories.length === 5;
        },
        
        get totalEstimatedValue() {
            return this.filteredLoots.reduce((total, loot) => {
                if (loot.estimatedPrice !== null && loot.estimatedPrice > 0) {
                    return total + (loot.estimatedPrice * loot.quantity);
                }
                return total;
            }, 0);
        },
        
        get statusClass() {
            switch(this.stats.status) {
                case 'online': return 'online';
                case 'connecting': return 'connecting';
                default: return 'offline';
            }
        },
        
        get statusText() {
            switch(this.stats.status) {
                case 'online': return 'Capturando';
                case 'connecting': return 'Conectando...';
                default: return 'Offline';
            }
        },
        
        // ========================================
        // LIFECYCLE
        // ========================================
        
        init() {
            console.log('[Dashboard] Initializing...');
            
            // Load saved settings
            this.loadSettings();
            
            this.connectSocket();
            this.loadHistory();
            this.startSessionTimer();
            
            // Init icons after Alpine renders
            this.$nextTick(() => {
                lucide.createIcons();
            });
        },
        
        // ========================================
        // SETTINGS PERSISTENCE
        // ========================================
        
        loadSettings() {
            // Load server preference
            const savedServer = localStorage.getItem('lootlogger_server');
            if (savedServer && this.priceServers.find(s => s.id === savedServer)) {
                this.selectedServer = savedServer;
            }
            
            // Load Discord webhook
            const savedWebhook = localStorage.getItem('lootlogger_webhook');
            if (savedWebhook) {
                this.discordWebhook = savedWebhook;
            }
            
            // Load theme preference
            const savedTheme = localStorage.getItem('lootlogger_theme');
            if (savedTheme && this.themes.find(t => t.id === savedTheme)) {
                this.currentTheme = savedTheme;
            }
            
            // Apply theme to document
            this.applyTheme(this.currentTheme);
        },
        
        saveSettings() {
            localStorage.setItem('lootlogger_server', this.selectedServer);
            localStorage.setItem('lootlogger_webhook', this.discordWebhook);
            localStorage.setItem('lootlogger_theme', this.currentTheme);
        },
        
        // ========================================
        // THEME MANAGEMENT
        // ========================================
        
        setTheme(themeId) {
            if (!this.themes.find(t => t.id === themeId)) return;
            
            this.currentTheme = themeId;
            this.applyTheme(themeId);
            this.saveSettings();
        },
        
        applyTheme(themeId) {
            document.documentElement.setAttribute('data-theme', themeId);
        },
        
        changeServer(serverId) {
            this.selectedServer = serverId;
            this.priceCache = {}; // Clear cache when changing server
            this.saveSettings();
            
            // Refetch prices for current loots
            if (this.loots.length > 0) {
                this.fetchPricesForLoots(this.loots);
            }
        },
        
        // ========================================
        // DISCORD WEBHOOK
        // ========================================
        
        openDiscordModal() {
            this.discordModalOpen = true;
            this.discordTestResult = null;
        },
        
        closeDiscordModal() {
            this.discordModalOpen = false;
            this.discordTestResult = null;
        },
        
        saveDiscordWebhook() {
            this.saveSettings();
            this.discordTestResult = { success: true, message: 'Webhook salvo!' };
            setTimeout(() => {
                this.closeDiscordModal();
            }, 1500);
        },
        
        async testDiscordWebhook() {
            if (!this.discordWebhook) {
                this.discordTestResult = { success: false, message: 'Cole uma URL de webhook primeiro' };
                return;
            }
            
            if (!this.discordWebhook.startsWith('https://discord.com/api/webhooks/')) {
                this.discordTestResult = { success: false, message: 'URL de webhook inválida' };
                return;
            }
            
            this.discordTesting = true;
            this.discordTestResult = null;
            
            try {
                const response = await fetch(this.discordWebhook, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        embeds: [{
                            title: '🎮 Loot Logger - Teste',
                            description: 'Webhook configurado com sucesso!',
                            color: 0xa855f7,
                            footer: { text: 'Loot Logger Dashboard by Kazz' },
                            timestamp: new Date().toISOString()
                        }]
                    })
                });
                
                if (response.ok || response.status === 204) {
                    this.discordTestResult = { success: true, message: 'Teste enviado! Verifique o Discord.' };
                } else {
                    this.discordTestResult = { success: false, message: `Erro: ${response.status}` };
                }
            } catch (err) {
                this.discordTestResult = { success: false, message: 'Erro de conexão' };
            }
            
            this.discordTesting = false;
        },
        
        async sendToDiscord(loot) {
            if (!this.discordWebhook) return;
            
            try {
                const tierColors = {
                    4: 0x60a5fa, // Azul
                    5: 0xef4444, // Vermelho
                    6: 0xf97316, // Laranja
                    7: 0xeab308, // Amarelo
                    8: 0xffffff  // Branco
                };
                
                const tierMatch = loot.tier.display?.match(/T(\d)/);
                const tier = tierMatch ? parseInt(tierMatch[1]) : 4;
                const color = tierColors[tier] || 0xa855f7;
                
                await fetch(this.discordWebhook, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        embeds: [{
                            title: loot.item_name,
                            description: `**Quantidade:** ${loot.quantity}\n**Tier:** ${loot.tier.display || 'N/A'}`,
                            color: color,
                            thumbnail: { url: this.getItemImageUrl(loot.item_id, 128) },
                            fields: [
                                { name: 'Pegou', value: loot.looted_by.name, inline: true },
                                { name: 'Origem', value: this.formatOrigin(loot.looted_from.name), inline: true }
                            ],
                            footer: { text: 'Loot Logger Dashboard' },
                            timestamp: loot.timestamp
                        }]
                    })
                });
            } catch (err) {
                console.warn('[Discord] Error:', err);
            }
        },
        
        // ========================================
        // WEBSOCKET
        // ========================================
        
        connectSocket() {
            this.socket = io();
            
            this.socket.on('connect', () => {
                console.log('[WS] Connected');
                this.connected = true;
            });
            
            this.socket.on('disconnect', () => {
                console.log('[WS] Disconnected');
                this.connected = false;
            });
            
            this.socket.on('new_loot', async (loot) => {
                console.log('[WS] New loot:', loot);
                
                // Add loot with placeholder for price
                loot.estimatedPrice = null;
                this.loots = [loot, ...this.loots];
                
                // Update players list
                if (!this.players.includes(loot.looted_by.name) && !loot.looted_by.name.startsWith('@')) {
                    this.players = [...this.players, loot.looted_by.name];
                }
                
                // Limit to 500 items
                if (this.loots.length > 500) {
                    this.loots = this.loots.slice(0, 500);
                }
                
                // Re-init icons
                this.$nextTick(() => lucide.createIcons());
                
                // Fetch price asynchronously
                const price = await this.getItemPrice(loot.item_id);
                
                // Update price reactively
                const index = this.loots.findIndex(l => l.id === loot.id);
                if (index !== -1) {
                    const updatedLoot = { ...this.loots[index], estimatedPrice: price };
                    this.loots = [
                        ...this.loots.slice(0, index),
                        updatedLoot,
                        ...this.loots.slice(index + 1)
                    ];
                }
                
                // Send to Discord if configured and item is rare or valuable
                if (this.discordWebhook && (loot.tier.is_rare || price > 100000)) {
                    this.sendToDiscord({ ...loot, estimatedPrice: price });
                }
            });
            
            this.socket.on('stats', (stats) => {
                this.stats = { ...this.stats, ...stats };
            });
            
            this.socket.on('status', (data) => {
                this.stats.status = data.status;
            });
            
            this.socket.on('history', (data) => {
                this.loots = data.loots.reverse();
                this.updatePlayersList();
                this.$nextTick(() => lucide.createIcons());
            });
            
            this.socket.on('clear', () => {
                this.loots = [];
                this.players = [];
                this.stats.total_loots = 0;
                this.stats.total_items = 0;
                this.stats.players_active = 0;
            });
        },
        
        // ========================================
        // DATA LOADING
        // ========================================
        
        loadHistory() {
            fetch('/api/loots/recent?limit=100')
                .then(r => r.json())
                .then(data => {
                    if (data.loots && data.loots.length > 0) {
                        // Initialize all prices as null
                        this.loots = data.loots.map(loot => ({ ...loot, estimatedPrice: null }));
                        this.updatePlayersList();
                        this.$nextTick(() => lucide.createIcons());
                        
                        // Fetch prices for loaded items
                        this.fetchPricesForLoots(this.loots);
                    }
                })
                .catch(err => console.error('[API] Error:', err));
            
            fetch('/api/stats')
                .then(r => r.json())
                .then(data => {
                    this.stats = { ...this.stats, ...data };
                    if (data.session_start) {
                        this.sessionStartTime = new Date(data.session_start);
                    }
                })
                .catch(err => console.error('[API] Error:', err));
        },
        
        updatePlayersList() {
            const playerSet = new Set();
            this.loots.forEach(loot => {
                if (!loot.looted_by.name.startsWith('@')) {
                    playerSet.add(loot.looted_by.name);
                }
            });
            this.players = Array.from(playerSet);
        },
        
        // ========================================
        // SESSION TIMER
        // ========================================
        
        startSessionTimer() {
            if (!this.sessionStartTime) {
                this.sessionStartTime = new Date();
            }
            
            this.sessionInterval = setInterval(() => {
                const now = new Date();
                const diff = now - this.sessionStartTime;
                
                const hours = Math.floor(diff / 3600000);
                const minutes = Math.floor((diff % 3600000) / 60000);
                const seconds = Math.floor((diff % 60000) / 1000);
                
                this.sessionTime = [
                    hours.toString().padStart(2, '0'),
                    minutes.toString().padStart(2, '0'),
                    seconds.toString().padStart(2, '0')
                ].join(':');
            }, 1000);
        },
        
        // ========================================
        // HELPERS
        // ========================================
        
        getItemImageUrl(itemId, size = 60) {
            return `https://render.albiononline.com/v1/item/${itemId}.png?size=${size}&quality=1`;
        },
        
        getEnchantClass(tierDisplay) {
            if (!tierDisplay) return 'enchant-0';
            if (tierDisplay.includes('.4')) return 'enchant-4';
            if (tierDisplay.includes('.3')) return 'enchant-3';
            if (tierDisplay.includes('.2')) return 'enchant-2';
            if (tierDisplay.includes('.1')) return 'enchant-1';
            return 'enchant-0';
        },
        
        getItemCategory(itemId) {
            const id = itemId.toUpperCase();
            
            // Equipment patterns
            if (id.includes('_ARMOR_') || id.includes('_SHOES_') || id.includes('_HEAD_') ||
                id.includes('_CAPE') || id.includes('_BAG') || id.includes('_MOUNT_') ||
                id.includes('_2H_') || id.includes('_MAIN_') || id.includes('_OFF_') ||
                id.includes('WEAPON') || id.includes('SHIELD') || id.includes('_TOOL_')) {
                return 'equipment';
            }
            
            // Consumables
            if (id.includes('POTION') || id.includes('FOOD') || id.includes('MEAL') ||
                id.includes('FISH') || id.includes('_COOKED')) {
                return 'consumable';
            }
            
            // Runes
            if (id.includes('RUNE') || id.includes('SOUL') || id.includes('RELIC')) {
                return 'rune';
            }
            
            // Resources
            if (id.includes('_ROCK') || id.includes('_ORE') || id.includes('_HIDE') ||
                id.includes('_WOOD') || id.includes('_FIBER') || id.includes('_PLANKS') ||
                id.includes('_METALBAR') || id.includes('_LEATHER') || id.includes('_CLOTH')) {
                return 'resource';
            }
            
            return 'other';
        },
        
        getCategoryCount(categoryId) {
            return this.loots.filter(l => this.getItemCategory(l.item_id) === categoryId).length;
        },
        
        getPlayerLootCount(playerName) {
            return this.loots.filter(l => l.looted_by.name === playerName).length;
        },
        
        formatOrigin(name) {
            if (!name) return '-';
            if (name.startsWith('@')) return name.substring(1);
            if (name.startsWith('MOB_')) return name.substring(4).replace(/_/g, ' ');
            return name;
        },
        
        // ========================================
        // FILTER ACTIONS
        // ========================================
        
        toggleTier(tier) {
            const idx = this.filters.tiers.indexOf(tier);
            if (idx > -1) {
                this.filters.tiers.splice(idx, 1);
            } else {
                this.filters.tiers.push(tier);
            }
        },
        
        toggleAllTiers() {
            if (this.allTiersSelected) {
                this.filters.tiers = [];
            } else {
                this.filters.tiers = [4, 5, 6, 7, 8];
            }
        },
        
        toggleCategory(categoryId) {
            const idx = this.filters.categories.indexOf(categoryId);
            if (idx > -1) {
                this.filters.categories.splice(idx, 1);
            } else {
                this.filters.categories.push(categoryId);
            }
        },
        
        toggleAllCategories() {
            if (this.allCategoriesSelected) {
                this.filters.categories = [];
            } else {
                this.filters.categories = ['equipment', 'consumable', 'resource', 'rune', 'other'];
            }
        },
        
        togglePlayer(playerName) {
            const idx = this.filters.players.indexOf(playerName);
            if (idx > -1) {
                this.filters.players.splice(idx, 1);
            } else {
                this.filters.players.push(playerName);
            }
        },
        
        clearFilters() {
            this.filters = {
                search: '',
                tiers: [4, 5, 6, 7, 8],
                categories: ['equipment', 'consumable', 'resource', 'rune', 'other'],
                players: [],
                rareOnly: false
            };
        },
        
        // ========================================
        // ACTIONS
        // ========================================
        
        clearLoots() {
            if (!confirm('Tem certeza que deseja limpar todos os loots?')) return;
            
            fetch('/api/clear', { method: 'POST' })
                .then(r => r.json())
                .then(data => {
                    if (data.success) {
                        this.loots = [];
                        this.players = [];
                    }
                })
                .catch(err => console.error('[API] Error:', err));
        },
        
        // ========================================
        // PRICE API
        // ========================================
        
        async getItemPrice(itemId) {
            // Check cache first (5 min TTL)
            const cacheKey = `${this.selectedServer}_${itemId}`;
            const cached = this.priceCache[cacheKey];
            if (cached && Date.now() - cached.timestamp < 300000) {
                return cached.price;
            }
            
            try {
                const server = this.priceServers.find(s => s.id === this.selectedServer);
                const response = await fetch(
                    `https://${server.url}/api/v2/stats/prices/${itemId}.json?locations=Caerleon,Bridgewatch,Martlock,Thetford,FortSterling,Lymhurst`
                );
                const data = await response.json();
                
                if (data && data.length > 0) {
                    const prices = data.filter(d => d.sell_price_min > 0).map(d => d.sell_price_min);
                    const avgPrice = prices.length > 0 
                        ? Math.round(prices.reduce((a, b) => a + b, 0) / prices.length) 
                        : 0;
                    
                    this.priceCache[cacheKey] = { price: avgPrice, timestamp: Date.now() };
                    return avgPrice;
                }
            } catch (err) {
                console.warn('[Price API] Error:', err);
            }
            
            return 0;
        },
        
        formatSilver(amount) {
            if (amount >= 1000000) {
                return (amount / 1000000).toFixed(1) + 'M';
            } else if (amount >= 1000) {
                return (amount / 1000).toFixed(1) + 'K';
            }
            return amount.toString();
        },
        
        async fetchPricesForLoots(loots) {
            const uniqueIds = [...new Set(loots.map(l => l.item_id))];
            
            for (let i = 0; i < uniqueIds.length; i += 10) {
                const batch = uniqueIds.slice(i, i + 10);
                
                await Promise.all(batch.map(async (itemId) => {
                    const price = await this.getItemPrice(itemId);
                    
                    // Update all loots with this item_id reactively
                    this.loots = this.loots.map(loot => {
                        if (loot.item_id === itemId && loot.estimatedPrice === null) {
                            return { ...loot, estimatedPrice: price };
                        }
                        return loot;
                    });
                }));
                
                if (i + 10 < uniqueIds.length) {
                    await new Promise(r => setTimeout(r, 200));
                }
            }
        },
        
        // ========================================
        // TIER HELPERS
        // ========================================
        
        getTierFromDisplay(tierDisplay) {
            if (!tierDisplay) return 0;
            const match = tierDisplay.match(/T(\d)/);
            return match ? parseInt(match[1]) : 0;
        },
        
        getEnchantFromDisplay(tierDisplay) {
            if (!tierDisplay) return 0;
            const match = tierDisplay.match(/\.(\d)/);
            return match ? parseInt(match[1]) : 0;
        }
    };
}
