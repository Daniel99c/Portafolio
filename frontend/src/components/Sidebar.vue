<script setup>
import { ref, watch, nextTick } from 'vue'
import { useRoute } from 'vue-router'
import { profile, contact, sections, openMail } from '../data/portfolio'
import { useTheme } from '../composables/useTheme'
import Monogram from './Monogram.vue'
import ThemeToggle from './ThemeToggle.vue'
import SideTooltip from './SideTooltip.vue'
import Icon from './Icon.vue'

defineProps({
  expanded: { type: Boolean, default: true }
})

const emit = defineEmits(['toggle'])

const route = useRoute()
const { isDark } = useTheme()
const mobileNav = ref(null)

const socials = [
  { label: 'GitHub', href: contact.github, icon: 'github', external: true },
  { label: 'LinkedIn', href: contact.linkedin, icon: 'linkedin', external: true },
  { label: 'Correo', href: '#', icon: 'mail', external: false, onClick: openMail }
]

// En móvil, mantiene visible la pestaña activa
watch(
  () => route.name,
  async () => {
    await nextTick()
    mobileNav.value
      ?.querySelector('[aria-current="page"]')
      ?.scrollIntoView({ block: 'nearest', inline: 'center' })
  },
  { immediate: true }
)
</script>

<template>
  <!-- ESCRITORIO -->
  <aside
    class="theme-navy fixed inset-y-0 left-0 z-40 hidden flex-col border-r border-line
           transition-[width] duration-300 ease-out lg:flex"
    :class="expanded ? 'w-72' : 'w-20'"
    aria-label="Navegación del portafolio"
  >
    <!-- Decoración: retícula tenue y línea de acento -->
    <div aria-hidden="true" class="grid-pattern pointer-events-none absolute inset-0 opacity-40 mask-[linear-gradient(to_bottom,black,transparent_70%)]"></div>
    <span aria-hidden="true" class="absolute inset-x-0 top-0 h-px bg-linear-to-r from-transparent via-accent to-transparent"></span>

    <!-- CABECERA -->
    <div
      class="relative flex h-20 items-center border-b border-line"
      :class="expanded ? 'justify-between gap-3 px-5' : 'justify-center'"
    >
      <router-link v-if="expanded" to="/" class="flex min-w-0 items-center gap-3 rounded-lg">
        <Monogram />
        <span class="min-w-0">
          <span class="block truncate font-display text-[0.95rem] font-semibold">{{ profile.shortName }}</span>
          <span class="block truncate text-xs text-muted">{{ profile.title }}</span>
        </span>
        <span class="sr-only">— ir a la portada</span>
      </router-link>

      <button
        type="button"
        class="icon-btn group relative h-9 w-9"
        :aria-label="expanded ? 'Contraer menú lateral' : 'Expandir menú lateral'"
        :aria-expanded="expanded"
        @click="emit('toggle')"
      >
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" aria-hidden="true"
             class="h-4 w-4 transition-transform duration-300" :class="!expanded && 'rotate-180'">
          <path stroke-linecap="round" stroke-linejoin="round" d="M15 18l-6-6 6-6" />
        </svg>
        <SideTooltip v-if="!expanded" text="Expandir menú" />
      </button>
    </div>

    <!-- MENÚ (sin overflow al estar contraído para no recortar las etiquetas) -->
    <nav class="relative flex-1 py-8" :class="expanded && 'overflow-y-auto'" aria-label="Secciones">
      <ul class="space-y-1" :class="expanded ? 'px-4' : 'px-3'">
        <li v-for="item in sections" :key="item.id">
          <router-link
            :to="{ name: item.id }"
            :aria-label="expanded ? undefined : item.label"
            class="group relative flex items-center gap-3 rounded-lg py-3 transition-colors duration-200"
            :class="[
              expanded ? 'px-3' : 'justify-center',
              route.name === item.id ? 'bg-accent-soft text-ink' : 'text-muted hover:bg-surface-2 hover:text-ink'
            ]"
          >
            <!-- Indicador activo -->
            <span
              aria-hidden="true"
              class="absolute inset-y-2 left-0 w-0.5 rounded-full bg-accent shadow-[0_0_10px_var(--accent)] transition-transform duration-300"
              :class="route.name === item.id ? 'scale-y-100' : 'scale-y-0'"
            ></span>

            <Icon
              :name="item.icon"
              class="h-5 w-5 shrink-0 transition-colors"
              :class="route.name === item.id ? 'text-accent' : 'group-hover:text-accent'"
            />

            <span
              v-if="expanded"
              class="whitespace-nowrap text-[0.95rem]"
              :class="route.name === item.id ? 'font-semibold' : 'font-medium'"
            >
              {{ item.label }}
            </span>

            <SideTooltip v-else :text="item.label" />
          </router-link>
        </li>
      </ul>
    </nav>

    <!-- PIE -->
    <div
      class="relative flex border-t border-line py-5"
      :class="expanded ? 'items-center justify-between px-5' : 'flex-col items-center gap-3'"
    >
      <ul class="flex gap-1.5" :class="!expanded && 'flex-col'" aria-label="Perfiles y contacto">
        <li v-for="social in socials" :key="social.label">
          <a
            :href="social.href"
            :target="social.external ? '_blank' : undefined"
            :rel="social.external ? 'noopener noreferrer' : undefined"
            class="icon-btn group relative h-9 w-9"
            :aria-label="social.external ? `${social.label} (se abre en una pestaña nueva)` : 'Enviar un correo'"
            :title="expanded ? social.label : undefined"
            @click="social.onClick && ($event.preventDefault(), social.onClick())"
          >
            <Icon :name="social.icon" class="h-4 w-4" />
            <SideTooltip v-if="!expanded" :text="social.label" />
          </a>
        </li>
      </ul>

      <span class="group relative">
        <ThemeToggle />
        <SideTooltip v-if="!expanded" :text="isDark ? 'Tema claro' : 'Tema oscuro'" />
      </span>
    </div>
  </aside>

  <!-- MÓVIL Y TABLET -->
  <div class="theme-navy sticky top-0 z-40 border-b border-line lg:hidden">
    <div class="flex h-16 items-center justify-between gap-3 px-5">
      <router-link to="/" class="flex min-w-0 items-center gap-3 rounded-lg">
        <Monogram />
        <span class="truncate font-display text-[0.95rem] font-semibold">{{ profile.shortName }}</span>
        <span class="sr-only">— ir a la portada</span>
      </router-link>
      <ThemeToggle />
    </div>

    <nav ref="mobileNav" class="no-scrollbar flex gap-1 overflow-x-auto px-3 pb-3" aria-label="Secciones">
      <router-link
        v-for="item in sections"
        :key="item.id"
        :to="{ name: item.id }"
        class="flex shrink-0 items-center gap-2 rounded-lg px-3 py-2 text-sm font-medium transition-colors"
        :class="route.name === item.id ? 'bg-accent-soft text-ink' : 'text-muted hover:text-ink'"
      >
        <Icon :name="item.icon" class="h-4 w-4 text-accent" />
        {{ item.label }}
      </router-link>
    </nav>
  </div>
</template>
