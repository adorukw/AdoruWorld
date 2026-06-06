import { createApp } from 'vue'
import PixelUI from '@mmt817/pixel-ui'
import '@mmt817/pixel-ui/dist/index.css'
import './style.css'
import App from './App.vue'

import { createPinia } from 'pinia'
import router from './router'

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(PixelUI)

app.mount('#app')

