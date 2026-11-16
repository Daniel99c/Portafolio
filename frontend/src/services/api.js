// Cliente de la API del backend (Django).
// La dirección se configura en frontend/.env con VITE_API_URL.
export const API_URL = (import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000/api').replace(/\/$/, '')

const request = async (path, { timeout = 8000, ...options } = {}) => {
  const controller = new AbortController()
  const timer = setTimeout(() => controller.abort(), timeout)
  try {
    return await fetch(`${API_URL}${path}`, { ...options, signal: controller.signal })
  } finally {
    clearTimeout(timer)
  }
}

// Contenido del portafolio. Devuelve null si el backend no responde.
export const fetchPortfolio = async () => {
  try {
    const response = await request('/portfolio/', { timeout: 2500 })
    return response.ok ? await response.json() : null
  } catch {
    return null
  }
}

// Envía el formulario de contacto. Lanza un Error con un mensaje para mostrar.
export const sendContact = async (data) => {
  let response
  try {
    response = await request('/contact/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    })
  } catch {
    throw new Error('No pudimos conectar con el servidor. Inténtalo más tarde.')
  }
  if (response.ok) return

  if (response.status === 429) {
    throw new Error('Enviaste varios mensajes seguidos. Inténtalo de nuevo en una hora.')
  }
  const body = await response.json().catch(() => ({}))
  throw new Error(body.detail || 'Revisa los datos del formulario e inténtalo de nuevo.')
}

// Estadísticas anónimas: si fallan, no afectan al visitante
export const track = (kind, target = '') => {
  request('/events/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ kind, target }),
    keepalive: true
  }).catch(() => {})
}
