// Aparición sutil al entrar en pantalla. Si el usuario prefiere menos
// movimiento o el navegador no soporta IntersectionObserver, no hace nada.
const reduceMotion = () =>
  typeof window === 'undefined' ||
  !('IntersectionObserver' in window) ||
  window.matchMedia('(prefers-reduced-motion: reduce)').matches

export const reveal = {
  mounted(el) {
    if (reduceMotion()) return

    el.classList.add('reveal-init')
    el._revealObserver = new IntersectionObserver(
      ([entry], observer) => {
        if (!entry.isIntersecting) return
        el.classList.add('is-visible')
        observer.disconnect()
      },
      { rootMargin: '0px 0px -8% 0px', threshold: 0.05 }
    )
    el._revealObserver.observe(el)
  },
  unmounted(el) {
    el._revealObserver?.disconnect()
  }
}
