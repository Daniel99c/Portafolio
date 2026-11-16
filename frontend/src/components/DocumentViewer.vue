<script setup>
// Visor de PDF en un <dialog> nativo: atrapa el foco, cierra con Escape
// y devuelve el foco al botón que lo abrió.
import { ref, computed, watch, onBeforeUnmount } from 'vue'
import Icon from './Icon.vue'

const props = defineProps({
  // { title, url, subtitle?, downloadUrl?, downloadName? } o null para cerrar
  doc: { type: Object, default: null }
})

const emit = defineEmits(['close'])

const dialog = ref(null)

const downloadName = computed(() => props.doc?.downloadName ?? props.doc?.url.split('/').pop())

const lockScroll = (locked) => {
  document.documentElement.style.overflow = locked ? 'hidden' : ''
}

watch(
  () => props.doc,
  (doc) => {
    const el = dialog.value
    if (!el) return
    if (doc && !el.open) {
      el.showModal()
      lockScroll(true)
    } else if (!doc && el.open) {
      el.close()
    }
  },
  { flush: 'post' }
)

const onClose = () => {
  lockScroll(false)
  emit('close')
}

// Clic en el fondo oscuro: el destino es el propio <dialog>
const onBackdropClick = (e) => {
  if (e.target === dialog.value) dialog.value.close()
}

onBeforeUnmount(() => lockScroll(false))
</script>

<template>
  <dialog
    ref="dialog"
    class="doc-dialog m-auto w-[min(64rem,calc(100vw-1.5rem))] max-w-none overflow-hidden rounded-2xl border border-line
           bg-surface p-0 text-ink shadow-2xl sm:h-[min(90svh,58rem)]"
    aria-labelledby="visor-titulo"
    @close="onClose"
    @click="onBackdropClick"
  >
    <div v-if="doc" class="flex h-full flex-col">
      <header class="flex flex-wrap items-start justify-between gap-4 border-b border-line p-4 sm:p-5">
        <div class="min-w-0 flex-1">
          <p v-if="doc.subtitle" class="font-mono text-xs text-accent">{{ doc.subtitle }}</p>
          <h2 id="visor-titulo" class="mt-1 font-display text-lg font-semibold leading-snug">{{ doc.title }}</h2>
        </div>

        <div class="flex items-center gap-2">
          <a :href="doc.url" target="_blank" rel="noopener noreferrer" class="btn btn-ghost min-h-0 px-3 py-2 text-sm">
            <Icon name="external" class="h-4 w-4" />
            <span class="hidden sm:inline">Abrir</span>
            <span class="sr-only">el PDF en una pestaña nueva</span>
          </a>
          <a :href="doc.downloadUrl ?? doc.url" :download="downloadName" class="btn btn-ghost min-h-0 px-3 py-2 text-sm">
            <Icon name="download" class="h-4 w-4" />
            <span class="hidden sm:inline">Descargar</span>
            <span class="sr-only">PDF</span>
          </a>
          <button type="button" class="icon-btn" aria-label="Cerrar visor" @click="dialog.close()">
            <Icon name="close" class="h-5 w-5" />
          </button>
        </div>
      </header>

      <!-- Vista previa: los navegadores móviles suelen no mostrar PDF incrustados -->
      <iframe
        :src="`${doc.url}#view=FitH`"
        :title="`Vista previa: ${doc.title}`"
        class="hidden w-full flex-1 bg-white sm:block"
      ></iframe>

      <div class="p-5 text-sm text-muted sm:hidden">
        <p>En el celular, abre el documento para verlo completo.</p>
        <a :href="doc.url" target="_blank" rel="noopener noreferrer" class="btn btn-primary mt-4 w-full">
          <Icon name="file" class="h-4 w-4" />
          Ver documento
          <span class="sr-only">(PDF, se abre en una pestaña nueva)</span>
        </a>
      </div>
    </div>
  </dialog>
</template>
