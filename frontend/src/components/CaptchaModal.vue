<script setup>
// Ventana emergente con la verificación humana (usa <dialog> nativo:
// atrapa el foco, se cierra con Escape y bloquea el fondo).
import { ref, watch, nextTick } from 'vue'
import Captcha from './Captcha.vue'
import Icon from './Icon.vue'

const props = defineProps({
  open: { type: Boolean, default: false }
})

const emit = defineEmits(['close', 'verified'])

const dialog = ref(null)

watch(
  () => props.open,
  async (open) => {
    await nextTick()
    if (open && !dialog.value?.open) dialog.value?.showModal()
    if (!open && dialog.value?.open) dialog.value.close()
  }
)

// Clic fuera de la tarjeta (sobre el fondo) cierra la ventana
const onClick = (event) => {
  if (event.target === dialog.value) emit('close')
}
</script>

<template>
  <dialog
    ref="dialog"
    aria-labelledby="captcha-titulo"
    class="captcha-dialog m-auto w-[calc(100%-2rem)] max-w-md overflow-visible bg-transparent p-0 backdrop:bg-black/55 backdrop:backdrop-blur-sm"
    @click="onClick"
    @close="emit('close')"
  >
    <div v-if="open" class="relative">
      <button
        type="button"
        class="absolute top-3 right-3 z-10 grid h-9 w-9 place-items-center rounded-lg text-muted transition-colors hover:bg-surface-2 hover:text-ink"
        @click="emit('close')"
      >
        <Icon name="close" class="h-5 w-5" />
        <span class="sr-only">Cerrar</span>
      </button>
      <Captcha @verified="emit('verified')" />
    </div>
  </dialog>
</template>

<style scoped>
.captcha-dialog[open] {
  animation: captcha-in 0.2s ease-out;
}

@keyframes captcha-in {
  from {
    opacity: 0;
    transform: translateY(8px) scale(0.98);
  }
}

@media (prefers-reduced-motion: reduce) {
  .captcha-dialog[open] {
    animation: none;
  }
}
</style>
