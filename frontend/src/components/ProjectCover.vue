<script setup>
// Portada de un proyecto sin captura: se arma con sus propios datos
// (tecnologías y estado), así no se muestra nada inventado.
import { computed } from 'vue'
import TechLogo from './TechLogo.vue'

const props = defineProps({
  project: { type: Object, required: true },
  large: { type: Boolean, default: false }
})

const tiles = computed(() => props.project.tech.slice(0, props.large ? 6 : 4))
</script>

<template>
  <div
    aria-hidden="true"
    class="theme-navy relative flex h-full items-center justify-center overflow-hidden bg-bg p-6"
    :class="large ? 'min-h-56 md:min-h-64' : 'min-h-48'"
  >
    <!-- Fondo: retícula y brillo -->
    <div class="grid-pattern absolute inset-0 opacity-70 mask-[radial-gradient(ellipse_at_center,black,transparent_75%)]"></div>
    <div class="absolute -top-16 -right-16 h-48 w-48 rounded-full bg-accent/25 blur-3xl"></div>
    <div class="absolute -bottom-20 -left-10 h-40 w-40 rounded-full bg-accent/10 blur-3xl"></div>

    <!-- Ventana -->
    <div
      class="relative w-full max-w-xs overflow-hidden rounded-xl border border-line bg-surface/80 shadow-[0_20px_40px_-20px_rgb(0_0_0/0.6)]
             backdrop-blur transition-transform duration-300 group-hover/card:-translate-y-1"
    >
      <div class="flex items-center gap-1.5 border-b border-line px-3 py-2">
        <span class="h-2 w-2 rounded-full bg-line-strong"></span>
        <span class="h-2 w-2 rounded-full bg-line-strong"></span>
        <span class="h-2 w-2 rounded-full bg-accent"></span>
        <span class="ml-2 truncate font-mono text-[0.7rem] text-muted">~/proyectos/{{ project.id }}</span>
      </div>

      <div class="p-4">
        <ul class="grid gap-2" :class="large ? 'grid-cols-3' : 'grid-cols-4'">
          <li
            v-for="(t, i) in tiles"
            :key="t"
            class="flex flex-col items-center gap-1.5 rounded-lg border border-line bg-surface-2 px-1 py-2.5 transition duration-300
                   group-hover/card:-translate-y-0.5 group-hover/card:border-accent motion-reduce:transition-none"
            :style="{ transitionDelay: `${i * 40}ms` }"
          >
            <span class="grid h-8 w-8 place-items-center rounded-md bg-white">
              <TechLogo :name="t" class="h-4.5 w-4.5" />
            </span>
            <span class="w-full truncate text-center font-mono text-[0.6rem] text-muted">{{ t }}</span>
          </li>
        </ul>

        <p class="mt-3 flex items-center gap-2 font-mono text-[0.7rem] text-muted">
          <span class="relative flex h-2 w-2">
            <span class="absolute inline-flex h-full w-full animate-ping rounded-full bg-accent opacity-60 motion-reduce:hidden"></span>
            <span class="relative inline-flex h-2 w-2 rounded-full bg-accent"></span>
          </span>
          status: <span class="text-ink">{{ project.status }}</span>
        </p>
      </div>
    </div>
  </div>
</template>

