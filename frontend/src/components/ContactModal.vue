<script setup>
// Formulario de contacto en un <dialog> nativo. Lo protegen Cloudflare
// Turnstile (verificado en el backend), un campo trampa y un límite de envíos.
import { ref, reactive, watch, nextTick } from 'vue'
import { sendContact } from '../services/api'
import Icon from './Icon.vue'

const props = defineProps({
  open: { type: Boolean, default: false }
})

const emit = defineEmits(['close'])

// Llave de prueba de Cloudflare (siempre aprueba) si no hay una configurada
const SITE_KEY = import.meta.env.VITE_TURNSTILE_SITE_KEY || '1x00000000000000000000AA'
const SCRIPT_URL = 'https://challenges.cloudflare.com/turnstile/v0/api.js?render=explicit'

const dialog = ref(null)
const widget = ref(null)
const form = reactive({ name: '', email: '', phone: '', message: '', website: '' })
const token = ref('')
const state = ref('idle') // idle | sending | sent
const error = ref('')
let widgetId = null

const loadTurnstile = () =>
  window.turnstile
    ? Promise.resolve()
    : new Promise((resolve, reject) => {
        const script = document.createElement('script')
        script.src = SCRIPT_URL
        script.async = true
        script.onload = resolve
        script.onerror = reject
        document.head.appendChild(script)
      })

const renderCaptcha = async () => {
  try {
    await loadTurnstile()
  } catch {
    error.value = 'No se pudo cargar la verificación de seguridad. Revisa tu conexión.'
    return
  }
  if (!widget.value) return
  widgetId = window.turnstile.render(widget.value, {
    sitekey: SITE_KEY,
    language: 'es',
    theme: document.documentElement.classList.contains('dark') ? 'dark' : 'light',
    callback: (value) => (token.value = value),
    'expired-callback': () => (token.value = ''),
    'error-callback': () => (token.value = '')
  })
}

const resetCaptcha = () => {
  token.value = ''
  if (widgetId !== null) window.turnstile?.reset(widgetId)
}

watch(
  () => props.open,
  async (open) => {
    await nextTick()
    if (open && !dialog.value?.open) {
      dialog.value?.showModal()
      if (state.value === 'sent') Object.assign(form, { name: '', email: '', phone: '', message: '' })
      state.value = 'idle'
      error.value = ''
      if (widgetId === null) renderCaptcha()
      else resetCaptcha()
    }
    if (!open && dialog.value?.open) dialog.value.close()
  }
)

const submit = async () => {
  error.value = ''
  if (!token.value) {
    error.value = 'Completa la verificación de seguridad.'
    return
  }
  state.value = 'sending'
  try {
    await sendContact({ ...form, token: token.value })
    state.value = 'sent'
  } catch (e) {
    error.value = e.message
    state.value = 'idle'
    // Cada token sirve una sola vez
    resetCaptcha()
  }
}

const onClick = (event) => {
  if (event.target === dialog.value) emit('close')
}

const field =
  'mt-1.5 w-full rounded-lg border border-line-strong bg-surface px-3.5 py-2.5 text-ink outline-none transition-colors focus:border-accent'
</script>

<template>
  <dialog
    ref="dialog"
    aria-labelledby="contacto-form-titulo"
    class="contact-dialog m-auto max-h-[calc(100svh-2rem)] w-[calc(100%-2rem)] max-w-lg overflow-y-auto rounded-2xl bg-transparent p-0 backdrop:bg-black/55 backdrop:backdrop-blur-sm"
    @click="onClick"
    @close="emit('close')"
  >
    <div class="card relative p-6 shadow-2xl md:p-8">
      <button
        type="button"
        class="absolute top-3 right-3 grid h-9 w-9 place-items-center rounded-lg text-muted transition-colors hover:bg-surface-2 hover:text-ink"
        @click="emit('close')"
      >
        <Icon name="close" class="h-5 w-5" />
        <span class="sr-only">Cerrar</span>
      </button>

      <div class="flex items-center gap-3 pr-8">
        <span class="grid h-10 w-10 shrink-0 place-items-center rounded-xl bg-accent-soft text-accent">
          <Icon name="mail" class="h-5 w-5" />
        </span>
        <div>
          <h2 id="contacto-form-titulo" class="font-display text-lg font-semibold text-ink">Escríbeme un mensaje</h2>
          <p class="text-sm text-muted">Te responderé al correo que indiques.</p>
        </div>
      </div>

      <!-- ENVIADO -->
      <div v-if="state === 'sent'" class="mt-8 text-center" role="status">
        <span class="mx-auto grid h-12 w-12 place-items-center rounded-full bg-accent-soft text-accent">
          <Icon name="shield" class="h-6 w-6" />
        </span>
        <p class="mt-4 font-display text-lg font-semibold text-ink">¡Mensaje enviado!</p>
        <p class="mt-1 text-muted">Gracias por escribir. Te responderé pronto.</p>
        <button type="button" class="btn btn-primary mt-6 w-full" @click="emit('close')">Cerrar</button>
      </div>

      <!-- FORMULARIO -->
      <form v-else class="mt-6 space-y-4" @submit.prevent="submit">
        <div>
          <label for="contacto-nombre" class="text-sm font-semibold text-ink">Nombre o empresa</label>
          <input id="contacto-nombre" v-model.trim="form.name" required maxlength="100" autocomplete="name" :class="field" />
        </div>

        <div class="grid gap-4 sm:grid-cols-2">
          <div>
            <label for="contacto-correo" class="text-sm font-semibold text-ink">Correo</label>
            <input id="contacto-correo" v-model.trim="form.email" type="email" required maxlength="254" autocomplete="email" :class="field" />
          </div>
          <div>
            <label for="contacto-telefono" class="text-sm font-semibold text-ink">
              Teléfono <span class="font-normal text-muted">(opcional)</span>
            </label>
            <input id="contacto-telefono" v-model.trim="form.phone" type="tel" maxlength="30" autocomplete="tel" :class="field" />
          </div>
        </div>

        <div>
          <label for="contacto-mensaje" class="text-sm font-semibold text-ink">Mensaje</label>
          <textarea
            id="contacto-mensaje"
            v-model.trim="form.message"
            required
            minlength="10"
            maxlength="3000"
            rows="5"
            :class="[field, 'resize-y']"
          ></textarea>
        </div>

        <!-- Trampa para bots: invisible para las personas -->
        <div class="sr-only" aria-hidden="true">
          <label for="contacto-web">Sitio web</label>
          <input id="contacto-web" v-model="form.website" tabindex="-1" autocomplete="off" />
        </div>

        <div ref="widget" class="min-h-[65px]"></div>

        <p class="min-h-5 text-sm text-red-600 dark:text-red-400" aria-live="polite">{{ error }}</p>

        <button
          type="submit"
          class="btn btn-primary w-full disabled:pointer-events-none disabled:opacity-50"
          :disabled="state === 'sending'"
        >
          {{ state === 'sending' ? 'Enviando…' : 'Enviar mensaje' }}
        </button>
      </form>
    </div>
  </dialog>
</template>

<style scoped>
.contact-dialog[open] {
  animation: contact-in 0.2s ease-out;
}

@keyframes contact-in {
  from {
    opacity: 0;
    transform: translateY(8px) scale(0.98);
  }
}

@media (prefers-reduced-motion: reduce) {
  .contact-dialog[open] {
    animation: none;
  }
}
</style>
