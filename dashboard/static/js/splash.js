/**
 * Splash.js - Splash Screen Controller
 * Loot Logger Dashboard by Kazz
 */

// ========================================
// SPLASH SCREEN CONTROLLER
// ========================================

document.addEventListener('DOMContentLoaded', () => {
    const splash = document.getElementById('splashScreen');
    const app = document.getElementById('app');
    
    if (!splash || !app) return;
    
    // Initialize Lucide icons
    if (typeof lucide !== 'undefined') {
        lucide.createIcons();
    }
    
    // Check if splash was already shown in this session
    const splashShown = sessionStorage.getItem('lootlogger_splash_shown');
    
    if (splashShown) {
        // Skip splash, show app immediately
        splash.remove();
        app.classList.add('visible');
        return;
    }
    
    // Mark splash as shown for this session
    sessionStorage.setItem('lootlogger_splash_shown', 'true');
    
    // Hide splash after animation completes (2.5s)
    const splashDuration = 2500;
    
    setTimeout(() => {
        // Hide splash
        splash.classList.add('hidden');
        
        // Show app
        app.classList.add('visible');
        
        // Remove splash from DOM after transition
        setTimeout(() => {
            splash.remove();
        }, 500);
        
    }, splashDuration);
});
