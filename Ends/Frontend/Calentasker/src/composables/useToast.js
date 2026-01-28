
import { ref } from 'vue';

const toasts = ref([]);

export function useToast() {

    // Type: 'success', 'error', 'info', 'warning'
    const addToast = (message, type = 'info', duration = 3000) => {
        const id = Date.now();
        toasts.value.push({ id, message, type });

        if (duration > 0) {
            setTimeout(() => {
                removeToast(id);
            }, duration);
        }
    };

    const removeToast = (id) => {
        toasts.value = toasts.value.filter(t => t.id !== id);
    };

    return {
        toasts,
        addToast,
        removeToast
    };
}
