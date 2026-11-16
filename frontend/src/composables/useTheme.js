import { ref } from 'vue'

// Estado compartido: el tema inicial lo fija el script de index.html
const isDark = ref(document.documentElement.classList.contains('dark'))

export function useTheme() {
  const toggle = () => {
    isDark.value = !isDark.value
    document.documentElement.classList.toggle('dark', isDark.value)
    try {
      localStorage.theme = isDark.value ? 'dark' : 'light'
    } catch {
      // almacenamiento no disponible: el tema solo dura la sesión
    }
  }

  return { isDark, toggle }
}
