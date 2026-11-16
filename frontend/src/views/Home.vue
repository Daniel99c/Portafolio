<script setup>
import { profile, stack } from '../data/portfolio'
import SiteHeader from '../components/SiteHeader.vue'
import Hero from '../components/Hero.vue'
import SiteFooter from '../components/SiteFooter.vue'

const year = new Date().getFullYear()
const mainStack = stack.find((group) => group.primary).items
</script>

<template>
  <div class="relative flex min-h-svh flex-col overflow-hidden bg-bg">
    <!-- Retícula tenue que se desvanece -->
    <div
      aria-hidden="true"
      class="grid-pattern pointer-events-none absolute inset-0 opacity-60
             mask-[radial-gradient(ellipse_70%_60%_at_70%_30%,black,transparent)]"
    ></div>

    <SiteHeader />

    <main id="contenido" tabindex="-1" class="relative flex flex-1 items-center focus:outline-none">
      <Hero />
    </main>

    <!-- BANDA INFERIOR: stack principal -->
    <div class="rise relative border-t border-line" style="--d: 8">
      <div class="container-page flex flex-wrap items-center justify-between gap-x-8 gap-y-3 py-5">
        <ul class="flex flex-wrap items-center gap-x-3 gap-y-2 font-mono text-xs text-muted" aria-label="Stack principal">
          <li v-for="(tech, i) in mainStack" :key="tech" class="flex items-center gap-3">
            <span v-if="i" aria-hidden="true" class="h-1 w-1 rounded-full bg-accent/70"></span>
            {{ tech }}
          </li>
        </ul>
        <p class="font-mono text-xs text-muted">© {{ year }} {{ profile.shortName }}</p>
      </div>
    </div>
  </div>

  <SiteFooter />
</template>
