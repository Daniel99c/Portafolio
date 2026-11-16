<script setup>
import { profile, sections } from '../data/portfolio'
import Monogram from './Monogram.vue'
import ThemeToggle from './ThemeToggle.vue'

const linkClass = 'rounded-lg px-3 py-2 text-sm font-medium text-muted transition-colors hover:text-ink'
</script>

<template>
  <header class="rise relative z-10">
    <div class="container-page flex h-20 items-center justify-between gap-4">
      <router-link to="/" class="flex min-w-0 items-center gap-3 rounded-lg" aria-label="Inicio">
        <Monogram />
        <span class="hidden truncate font-display text-[0.95rem] font-semibold text-ink sm:block">{{ profile.shortName }}</span>
      </router-link>

      <div class="flex items-center gap-1 sm:gap-2">
        <nav aria-label="Principal">
          <ul class="flex items-center">
            <li>
              <router-link :to="{ name: sections[0].id }" :class="linkClass">Portafolio</router-link>
            </li>
            <li class="hidden sm:block">
              <router-link :to="{ name: 'proyectos' }" :class="linkClass">Proyectos</router-link>
            </li>
            <li>
              <a href="#contacto" :class="linkClass">Contacto</a>
            </li>
          </ul>
        </nav>
        <ThemeToggle />
      </div>
    </div>
  </header>
</template>
