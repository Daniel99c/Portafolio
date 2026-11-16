<script setup>
import { ref, computed, watch } from 'vue'
import { useRoute } from 'vue-router'
import { sections } from '../data/portfolio'
import Sidebar from '../components/Sidebar.vue'
import SiteFooter from '../components/SiteFooter.vue'
import Icon from '../components/Icon.vue'

const STORAGE_KEY = 'sidebar-expanded'

const readExpanded = () => {
  try {
    return localStorage.getItem(STORAGE_KEY) !== 'false'
  } catch {
    return true
  }
}

const expanded = ref(readExpanded())

watch(expanded, (value) => {
  try {
    localStorage.setItem(STORAGE_KEY, String(value))
  } catch {
    // almacenamiento no disponible: la preferencia dura solo esta visita
  }
})

const route = useRoute()
const main = ref(null)

const position = computed(() => sections.findIndex((s) => s.id === route.name))
const prev = computed(() => sections[position.value - 1])
const next = computed(() => sections[position.value + 1])

// Tras cambiar de sección, lleva el foco al título (teclado y lectores de pantalla).
// En la primera carga no se mueve el foco.
let firstLoad = true
const onAfterEnter = () => {
  if (firstLoad) {
    firstLoad = false
    return
  }
  main.value?.querySelector('h1')?.focus({ preventScroll: true })
}
</script>

<template>
  <div class="relative min-h-svh bg-bg">
    <Sidebar :expanded="expanded" @toggle="expanded = !expanded" />

    <!-- Retícula decorativa del área de contenido -->
    <div
      aria-hidden="true"
      class="grid-pattern pointer-events-none fixed inset-0 opacity-50
             mask-[radial-gradient(ellipse_60%_45%_at_80%_0%,black,transparent)]"
    ></div>

    <div class="relative transition-[padding] duration-300 ease-out" :class="expanded ? 'lg:pl-72' : 'lg:pl-20'">
      <main id="contenido" ref="main" tabindex="-1" class="focus:outline-none">
        <div class="mx-auto max-w-5xl px-5 py-12 md:px-10 md:py-16">
          <router-view v-slot="{ Component, route: current }">
            <Transition name="page" mode="out-in" @after-enter="onAfterEnter">
              <component :is="Component" :key="current.name" />
            </Transition>
          </router-view>

          <!-- Navegación anterior / siguiente -->
          <nav v-if="position > -1" class="mt-16 grid gap-3 border-t border-line pt-8 sm:grid-cols-2" aria-label="Sección anterior y siguiente">
            <router-link
              v-if="prev"
              :to="{ name: prev.id }"
              class="card group flex flex-col gap-1 p-4 transition-colors hover:border-accent"
            >
              <span class="eyebrow">← Anterior</span>
              <span class="font-semibold text-ink group-hover:text-accent">{{ prev.label }}</span>
            </router-link>
            <span v-else aria-hidden="true" class="hidden sm:block"></span>

            <router-link
              v-if="next"
              :to="{ name: next.id }"
              class="card group flex flex-col gap-1 p-4 text-right transition-colors hover:border-accent"
            >
              <span class="eyebrow">Siguiente →</span>
              <span class="font-semibold text-ink group-hover:text-accent">{{ next.label }}</span>
            </router-link>
            <router-link
              v-else
              to="/"
              class="card group flex items-center justify-end gap-2 p-4 font-semibold text-ink transition-colors hover:border-accent hover:text-accent"
            >
              Volver a la portada
              <Icon name="arrowRight" class="h-4 w-4" />
            </router-link>
          </nav>
        </div>
      </main>

      <SiteFooter />
    </div>
  </div>
</template>
