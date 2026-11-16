<script setup>
import { experience } from '../data/portfolio'
import SectionHeader from './SectionHeader.vue'

const tech = experience.filter((exp) => !exp.minor)
const other = experience.filter((exp) => exp.minor)
</script>

<template>
  <section aria-labelledby="titulo-seccion">
    <SectionHeader
      title="Experiencia"
      description="Desarrollo, bases de datos y soporte de aplicaciones en los sectores tributario y salud."
    />

    <!-- EXPERIENCIA TECNOLÓGICA (línea de tiempo) -->
    <ol
      class="relative space-y-6 md:pl-10 md:before:absolute md:before:top-4 md:before:bottom-4 md:before:left-2.75
             md:before:w-px md:before:bg-line-strong md:before:content-['']"
    >
      <li v-for="exp in tech" :key="exp.company" v-reveal class="relative">
        <span
          aria-hidden="true"
          class="absolute -left-10 top-8 hidden h-5.5 w-5.5 place-items-center rounded-full border-2 bg-bg md:grid"
          :class="exp.current ? 'border-accent shadow-[0_0_12px_var(--accent-soft)]' : 'border-line-strong'"
        >
          <span class="h-2 w-2 rounded-full" :class="exp.current ? 'bg-accent' : 'bg-line-strong'"></span>
        </span>

        <article class="card p-6 md:p-8">
          <header class="flex flex-col gap-3 md:flex-row md:items-start md:justify-between md:gap-6">
            <div class="min-w-0">
              <h2 class="font-display text-xl font-semibold leading-snug text-ink md:text-2xl">{{ exp.company }}</h2>
              <p class="mt-1 font-semibold text-accent">{{ exp.role }}</p>
              <p class="mt-1 text-sm text-muted">{{ exp.context }}</p>
            </div>
            <p class="shrink-0">
              <span class="badge" :class="!exp.current && 'bg-surface-2! text-muted!'">
                <span v-if="exp.current" aria-hidden="true" class="h-1.5 w-1.5 rounded-full bg-current"></span>
                {{ exp.period }}
              </span>
            </p>
          </header>

          <p v-if="exp.note" class="mt-5 rounded-lg border-l-2 border-accent bg-accent-soft px-4 py-3 text-sm text-ink">
            {{ exp.note }}
          </p>

          <p v-if="exp.description" class="mt-5 max-w-3xl leading-relaxed text-muted">{{ exp.description }}</p>

          <div class="mt-6 grid gap-6" :class="exp.groups.length > 1 && 'xl:grid-cols-3'">
            <div v-for="(group, gi) in exp.groups" :key="gi">
              <h3 v-if="group.title" class="eyebrow mb-3">{{ group.title }}</h3>
              <ul class="space-y-2.5">
                <li v-for="item in group.items" :key="item" class="flex gap-3 text-[0.95rem] leading-relaxed text-ink/90">
                  <span aria-hidden="true" class="mt-[0.6em] h-1.5 w-1.5 shrink-0 rounded-full bg-accent"></span>
                  <span>{{ item }}</span>
                </li>
              </ul>
            </div>
          </div>

          <ul v-if="exp.tech?.length" class="mt-6 flex flex-wrap gap-2 border-t border-line pt-5" aria-label="Tecnologías">
            <li v-for="t in exp.tech" :key="t" class="chip font-mono text-xs">{{ t }}</li>
          </ul>
        </article>
      </li>
    </ol>

    <!-- OTRA EXPERIENCIA (menor protagonismo) -->
    <div v-if="other.length" v-reveal class="mt-10 md:pl-10">
      <h2 class="eyebrow">Otra experiencia</h2>
      <ul class="mt-3 divide-y divide-line border-y border-line">
        <li v-for="exp in other" :key="exp.company" class="grid gap-2 py-5 md:grid-cols-[1fr_auto] md:gap-6">
          <div>
            <p class="font-semibold text-ink">
              {{ exp.role }} <span class="font-normal text-muted">· {{ exp.company }}, {{ exp.context }}</span>
            </p>
            <p class="mt-1 text-sm leading-relaxed text-muted">{{ exp.description }}</p>
          </div>
          <p class="text-sm text-muted md:text-right">{{ exp.period }}</p>
        </li>
      </ul>
    </div>
  </section>
</template>
