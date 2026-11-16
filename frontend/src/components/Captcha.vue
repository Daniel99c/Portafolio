<script setup>
// Verificación humana sin servicios externos: un código dibujado en canvas
// con ruido. La verificación se recuerda durante la sesión del navegador.
import { ref, onMounted, nextTick } from 'vue'
import Icon from './Icon.vue'

const emit = defineEmits(['verified'])

// Sin caracteres ambiguos (0/O, 1/I/l)
const CHARS = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789'
const LENGTH = 5
const MAX_ATTEMPTS = 3

const canvas = ref(null)
const input = ref(null)
const answer = ref('')
const error = ref('')
const attempts = ref(0)
let code = ''

const rand = (min, max) => Math.random() * (max - min) + min

const cssVar = (name) => getComputedStyle(document.documentElement).getPropertyValue(name).trim()

const draw = () => {
  const el = canvas.value
  if (!el) return
  const ctx = el.getContext('2d')
  const { width, height } = el

  ctx.fillStyle = cssVar('--surface-2') || '#f1f3f5'
  ctx.fillRect(0, 0, width, height)

  const ink = cssVar('--ink') || '#0b2545'
  const accent = cssVar('--accent') || '#0b7285'
  const muted = cssVar('--muted') || '#6b7280'

  // Líneas de ruido
  for (let i = 0; i < 6; i++) {
    ctx.strokeStyle = i % 2 ? accent : muted
    ctx.globalAlpha = 0.45
    ctx.lineWidth = rand(1, 2)
    ctx.beginPath()
    ctx.moveTo(rand(0, width), rand(0, height))
    ctx.bezierCurveTo(rand(0, width), rand(0, height), rand(0, width), rand(0, height), rand(0, width), rand(0, height))
    ctx.stroke()
  }

  // Caracteres rotados y desplazados
  ctx.globalAlpha = 1
  ctx.textBaseline = 'middle'
  const step = width / (LENGTH + 1)
  ;[...code].forEach((char, i) => {
    ctx.save()
    ctx.translate(step * (i + 1), height / 2 + rand(-6, 6))
    ctx.rotate(rand(-0.4, 0.4))
    ctx.font = `600 ${Math.round(rand(26, 32))}px ui-monospace, monospace`
    ctx.fillStyle = i % 2 ? accent : ink
    ctx.textAlign = 'center'
    ctx.fillText(char, 0, 0)
    ctx.restore()
  })

  // Puntos de ruido
  for (let i = 0; i < 40; i++) {
    ctx.fillStyle = muted
    ctx.globalAlpha = 0.5
    ctx.fillRect(rand(0, width), rand(0, height), 1.5, 1.5)
  }
  ctx.globalAlpha = 1
}

const generate = () => {
  const values = crypto.getRandomValues(new Uint32Array(LENGTH))
  code = Array.from(values, (v) => CHARS[v % CHARS.length]).join('')
  answer.value = ''
  draw()
}

const refresh = () => {
  error.value = ''
  attempts.value = 0
  generate()
  input.value?.focus()
}

const submit = () => {
  if (answer.value.trim().toUpperCase() === code) {
    emit('verified')
    return
  }
  attempts.value++
  if (attempts.value >= MAX_ATTEMPTS) {
    attempts.value = 0
    error.value = 'Demasiados intentos. Te mostramos un código nuevo.'
    generate()
  } else {
    error.value = 'El código no coincide. Inténtalo de nuevo.'
    answer.value = ''
  }
  nextTick(() => input.value?.focus())
}

onMounted(generate)
</script>

<template>
  <div class="card mx-auto max-w-md p-6 shadow-2xl md:p-8">
    <div class="flex items-center gap-3">
      <span class="grid h-10 w-10 shrink-0 place-items-center rounded-xl bg-accent-soft text-accent">
        <Icon name="shield" class="h-5 w-5" />
      </span>
      <div>
        <h2 id="captcha-titulo" class="font-display text-lg font-semibold text-ink">Verificación de seguridad</h2>
        <p class="text-sm text-muted">Confirma que no eres un robot para continuar.</p>
      </div>
    </div>

    <form class="mt-6" novalidate @submit.prevent="submit">
      <div class="flex items-center gap-2">
        <canvas
          ref="canvas"
          width="220"
          height="64"
          role="img"
          aria-label="Código de verificación en imagen"
          class="h-16 min-w-0 flex-1 rounded-lg border border-line select-none"
        ></canvas>
        <button type="button" class="icon-btn shrink-0" title="Generar otro código" @click="refresh">
          <Icon name="cycle" class="h-[1.1rem] w-[1.1rem]" />
          <span class="sr-only">Generar otro código</span>
        </button>
      </div>

      <label for="captcha-input" class="mt-5 block text-sm font-semibold text-ink">Escribe el código de la imagen</label>
      <input
        id="captcha-input"
        ref="input"
        autofocus
        v-model="answer"
        type="text"
        autocomplete="off"
        autocapitalize="characters"
        spellcheck="false"
        :maxlength="LENGTH"
        :aria-invalid="!!error"
        aria-describedby="captcha-error"
        class="mt-2 w-full rounded-lg border border-line-strong bg-surface px-4 py-3 font-mono text-lg tracking-[0.3em] text-ink uppercase outline-none transition-colors focus:border-accent"
      />
      <p id="captcha-error" class="mt-2 min-h-5 text-sm text-red-600 dark:text-red-400" aria-live="polite">{{ error }}</p>

      <button type="submit" class="btn btn-primary mt-2 w-full disabled:pointer-events-none disabled:opacity-50" :disabled="answer.trim().length < LENGTH">
        Verificar
      </button>
    </form>
  </div>
</template>
