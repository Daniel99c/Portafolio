import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import { profile, sections } from '../data/portfolio'
import { track } from '../services/api'

// Cada sección se carga bajo demanda
const views = {
  'sobre-mi': () => import('../components/About.vue'),
  experiencia: () => import('../components/Experience.vue'),
  proyectos: () => import('../components/Projects.vue'),
  formacion: () => import('../components/Certifications.vue'),
  'hoja-de-vida': () => import('../components/CV.vue')
}

const routes = [
  {
    path: '/',
    name: 'home',
    component: Home
  },
  {
    path: '/portafolio',
    component: () => import('../views/PortfolioLayout.vue'),
    children: [
      { path: '', redirect: { name: sections[0].id } },
      ...sections.map((section) => ({
        path: section.id,
        name: section.id,
        component: views[section.id],
        meta: { title: section.title }
      }))
    ]
  },
  {
    // Ruta del diseño anterior
    path: '/about',
    redirect: { name: sections[0].id }
  },
  {
    path: '/:pathMatch(.*)*',
    redirect: '/'
  }
]

const prefersReducedMotion = () => window.matchMedia('(prefers-reduced-motion: reduce)').matches

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, _from, savedPosition) {
    if (savedPosition) return savedPosition
    if (to.hash) {
      // En móvil hay una barra fija superior
      const top = window.innerWidth < 1024 ? 128 : 24
      return { el: to.hash, top, behavior: prefersReducedMotion() ? 'auto' : 'smooth' }
    }
    return { top: 0 }
  }
})

const baseTitle = `${profile.name} — ${profile.title}`

router.afterEach((to, from) => {
  if (to.name && to.name !== from.name) track('page', to.meta.title || 'Portada')
  document.title = to.meta.title ? `${to.meta.title} · ${profile.shortName}` : baseTitle
})

export default router
