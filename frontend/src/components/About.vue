<script setup>
import { about, stack } from '../data/portfolio'
import SectionHeader from './SectionHeader.vue'
import TechMarquee from './TechMarquee.vue'
import TechLogo from './TechLogo.vue'

// Banda 1: stack principal · Banda 2: complementarias y calidad
const mainStack = stack.find((g) => g.primary).items
const secondaryStack = stack
  .filter((g) => ['Complementarias', 'Calidad y herramientas'].includes(g.title))
  .flatMap((g) => g.items)

</script>

<template>
  <section aria-labelledby="titulo-seccion">
    <SectionHeader title="Sobre mí" />

    <div class="grid gap-12 xl:grid-cols-12 xl:gap-12">
      <!-- BIO -->
      <div class="space-y-5 text-base leading-[1.8] text-muted md:text-[1.0625rem] xl:col-span-7">
        <p class="text-lg leading-relaxed text-ink md:text-xl">{{ about.paragraphs[0] }}</p>
        <p v-for="p in about.paragraphs.slice(1)" :key="p">{{ p }}</p>
      </div>

      <!-- ENFOQUE -->
      <div class="xl:col-span-5">
        <h2 class="eyebrow">Enfoque</h2>
        <ol class="mt-4 space-y-3">
          <li v-for="item in about.approach" :key="item" class="card flex gap-4 p-5">
            <span aria-hidden="true" class="mt-2 h-2 w-2 shrink-0 rounded-full bg-accent shadow-[0_0_8px_var(--accent)]"></span>
            <span class="leading-snug text-ink">{{ item }}</span>
          </li>
        </ol>
      </div>
    </div>

    <!-- STACK -->
    <div v-reveal class="mt-16 md:mt-20">
      <h2 class="font-display text-xl font-semibold text-ink md:text-2xl">Stack tecnológico</h2>
      <p class="mt-2 text-sm text-muted">Agrupado por uso, sin niveles de dominio.</p>

      <!-- Bandas en movimiento (se detienen al pasar el mouse) -->
      <div class="mt-6 space-y-3">
        <TechMarquee :items="mainStack" label="Stack principal" :duration="38" />
        <TechMarquee :items="secondaryStack" label="Tecnologías complementarias y herramientas" :duration="60" />
      </div>

      <div class="mt-8 grid gap-4 md:grid-cols-2">
        <div
          v-for="group in stack"
          :key="group.title"
          class="card p-5 md:p-6"
          :class="group.primary && 'border-accent/40 md:col-span-2'"
        >
          <h3 class="eyebrow" :class="group.primary && 'text-accent!'">{{ group.title }}</h3>
          <ul class="mt-4 flex flex-wrap gap-2">
            <li
              v-for="item in group.items"
              :key="item"
              class="chip gap-2"
              :class="group.primary && 'border-accent/30 bg-accent-soft font-semibold'"
            >
              <TechLogo :name="item" class="h-3.5 w-3.5 shrink-0" />
              {{ item }}
            </li>
          </ul>
        </div>
      </div>
    </div>
  </section>
</template>
