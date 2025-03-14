import './assets/main.css'

import App from './App.vue'
import router from './router'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import userLogin from '@/plugins/user/login.js'
import logoutUser from '@/plugins/user/logout.js'
import vClickOutside from "click-outside-vue3"
import userManager from "@/plugins/user/userManager";
import apolloPlugin from '@/plugins/apollo'; // Import the plugin
const app = createApp(App)

app.use(createPinia())
app.use(apolloPlugin);
app.use(router)
app.use(userLogin)
app.use(userManager)
app.use(logoutUser)
app.use(vClickOutside)
app.mount('#app')
