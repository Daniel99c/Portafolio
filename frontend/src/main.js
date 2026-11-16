import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from './router'
import { reveal } from './directives/reveal'
import { loadPortfolio } from './data/portfolio'
import { track } from './services/api'

// Primero se trae el contenido del backend (si no responde, se usa el local)
loadPortfolio().finally(() => {
  createApp(App)
    .use(router)
    .directive('reveal', reveal)
    .mount('#app')
})

// Una visita por sesión del navegador
try {
  if (!sessionStorage.getItem('visit-tracked')) {
    sessionStorage.setItem('visit-tracked', '1')
    track('visit')
  }
} catch {
  // almacenamiento no disponible: no se cuenta la visita
}
