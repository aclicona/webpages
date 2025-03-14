import {defineStore} from 'pinia';
import {ref, onMounted} from 'vue';

export const useSessionStore = defineStore('session', () => {
    const sideBarOpen = ref(false);

    const toggleSideBarState = () => {
        sideBarOpen.value = !sideBarOpen.value;
        localStorage.setItem('sideBarOpen', JSON.stringify(sideBarOpen.value));
    };

    const loadSideBarState = () => {
        const storedData = localStorage.getItem('sideBarOpen');
        if (storedData) {
            sideBarOpen.value = JSON.parse(storedData);
        }
    };

    const clearSideBarState = () => {
        sideBarOpen.value = null;
        localStorage.removeItem('sideBarOpen');
    };

    // Load data when store is initialized
    onMounted(() => {
        loadSideBarState();
    });

    return {sideBarOpen, toggleSideBarState, clearSideBarState, loadSideBarState};
});

window.addEventListener('storage', (event) => {
    if (event.key === 'sideBarOpen') {
        const {loadSideBarState} = useSessionStore();
        loadSideBarState()
    }
});