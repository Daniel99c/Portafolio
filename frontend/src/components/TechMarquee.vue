<script setup>
// Fila de tecnologías que se desplaza hacia la izquierda en bucle.
// La lista se repite una vez (oculta a lectores de pantalla) para que
// el bucle no tenga cortes; se pausa al pasar el mouse o con el foco.
import TechLogo from './TechLogo.vue'

defineProps({
  items: { type: Array, required: true },
  label: { type: String, required: true },
  // Segundos por vuelta completa: más alto = más lento
  duration: { type: Number, default: 40 }
})
</script>

<template>
  <div class="marquee" :style="{ '--marquee-duration': `${duration}s` }">
    <div class="marquee-track">
      <ul v-for="copy in 2" :key="copy" class="marquee-list" :aria-label="copy === 1 ? label : undefined" :aria-hidden="copy === 2 ? 'true' : undefined" :class="copy === 2 && 'marquee-dup'">
        <li
          v-for="item in items"
          :key="item"
          class="flex shrink-0 items-center gap-2.5 rounded-xl border border-line bg-surface px-4 py-2.5 text-sm font-medium text-ink"
        >
          <TechLogo :name="item" class="h-5 w-5 shrink-0" />
          {{ item }}
        </li>
      </ul>
    </div>
  </div>
</template>
