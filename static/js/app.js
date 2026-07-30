/* App-level JS - Alpine.js globals */
document.addEventListener('alpine:init', () => {
    // Global store for notifications
    Alpine.store('notifications', {
        items: [],
        add(message, type = 'info') {
            const id = Date.now();
            this.items.push({ id, message, type });
            setTimeout(() => {
                this.items = this.items.filter(n => n.id !== id);
            }, 4000);
        }
    });
});

// HTMX event handlers
document.addEventListener('htmx:afterRequest', (event) => {
    if (event.detail.successful) {
        // Success handling
    }
});

// Keyboard shortcuts
document.addEventListener('keydown', (e) => {
    // Ctrl+Enter to submit code
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        const submitBtn = document.querySelector('[x-on\\:click="submitCode()"]');
        if (submitBtn) submitBtn.click();
    }
});
