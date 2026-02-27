// ============================================
// Notification System
// ============================================

class NotificationManager {
    constructor() {
        this.notifications = [];
    }

    /**
     * Show success notification
     */
    success(message, duration = 5000) {
        this.show(message, 'success', duration);
    }

    /**
     * Show error notification
     */
    error(message, duration = 5000) {
        this.show(message, 'danger', duration);
    }

    /**
     * Show warning notification
     */
    warning(message, duration = 5000) {
        this.show(message, 'warning', duration);
    }

    /**
     * Show info notification
     */
    info(message, duration = 5000) {
        this.show(message, 'info', duration);
    }

    /**
     * Show notification
     */
    show(message, type = 'info', duration = 5000) {
        const container = this.getOrCreateContainer();
        
        const notification = document.createElement('div');
        notification.className = `alert alert-${type} alert-dismissible fade show`;
        notification.setAttribute('role', 'alert');
        notification.style.marginBottom = '1rem';
        notification.innerHTML = `
            <div class="d-flex justify-content-between align-items-center">
                <span>${this.getIcon(type)} ${message}</span>
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            </div>
        `;

        container.appendChild(notification);

        // Auto-dismiss
        if (duration > 0) {
            setTimeout(() => {
                const bsAlert = new bootstrap.Alert(notification);
                bsAlert.close();
            }, duration);
        }

        return notification;
    }

    /**
     * Get notification icon
     */
    getIcon(type) {
        const icons = {
            'success': '<i class="fas fa-check-circle"></i>',
            'danger': '<i class="fas fa-exclamation-circle"></i>',
            'warning': '<i class="fas fa-exclamation-triangle"></i>',
            'info': '<i class="fas fa-info-circle"></i>',
        };
        return icons[type] || icons['info'];
    }

    /**
     * Get or create notification container
     */
    getOrCreateContainer() {
        let container = document.getElementById('notification-container');
        
        if (!container) {
            container = document.createElement('div');
            container.id = 'notification-container';
            container.style.position = 'fixed';
            container.style.top = '80px';
            container.style.right = '20px';
            container.style.zIndex = '9999';
            container.style.maxWidth = '400px';
            document.body.appendChild(container);
        }

        return container;
    }
}

// Create global notification manager instance
const notify = new NotificationManager();