<script setup>
import { profile, contact, about } from '../data/portfolio'
import Icon from './Icon.vue'

const socials = [
  { label: 'GitHub', href: contact.github, icon: 'github' },
  { label: 'LinkedIn', href: contact.linkedin, icon: 'linkedin' }
]
</script>

<template>
  <section aria-labelledby="inicio-titulo" class="container-page grid w-full gap-12 py-10 md:py-14 lg:grid-cols-12 lg:items-center lg:gap-10">
    <!-- TEXTO -->
    <div class="min-w-0 lg:col-span-7">
      <p class="rise flex items-center gap-2 font-mono text-xs text-muted" style="--d: 1">
        <Icon name="pin" class="h-4 w-4 text-accent" />
        {{ profile.location }}
      </p>

      <h1
        id="inicio-titulo"
        class="rise mt-5 font-display text-[clamp(2.25rem,6vw,4.25rem)] font-semibold leading-[1.05] tracking-[-0.03em] text-ink"
        style="--d: 2"
      >
        {{ profile.name }}
      </h1>

      <p class="rise mt-5 text-lg font-semibold text-ink md:text-xl" style="--d: 3">
        {{ profile.title }}
        <span class="mx-1 hidden text-line-strong sm:inline" aria-hidden="true">|</span>
        <span class="mt-1 block font-medium text-accent sm:mt-0 sm:inline">{{ profile.stackLine.join(' · ') }}</span>
      </p>

      <p class="rise mt-5 max-w-xl text-base leading-relaxed text-muted md:text-lg" style="--d: 4">
        {{ profile.summary }}
      </p>

      <ul class="rise mt-7 flex flex-wrap gap-2" style="--d: 5" aria-label="Distinciones">
        <li v-for="badge in profile.badges" :key="badge" class="badge">
          <span aria-hidden="true" class="h-1.5 w-1.5 rounded-full bg-current"></span>
          {{ badge }}
        </li>
      </ul>

      <div class="rise mt-9 flex flex-col gap-3 sm:flex-row sm:flex-wrap sm:items-center" style="--d: 6">
        <router-link :to="{ name: 'sobre-mi' }" class="btn btn-primary group">
          Sobre mí
          <Icon name="arrowRight" class="h-4 w-4 transition-transform duration-200 group-hover:translate-x-0.5" />
        </router-link>
        <a :href="profile.cv.downloadUrl" :download="profile.cv.downloadName" class="btn btn-ghost">
          <Icon name="download" class="h-4 w-4" />
          Descargar hoja de vida
          <span class="sr-only">(PDF)</span>
        </a>
      </div>

      <ul class="rise mt-8 flex items-center gap-2" style="--d: 7" aria-label="Perfiles profesionales">
        <li v-for="social in socials" :key="social.label">
          <a
            :href="social.href"
            target="_blank"
            rel="noopener noreferrer"
            class="icon-btn"
            :aria-label="`${social.label} (se abre en una pestaña nueva)`"
            :title="social.label"
          >
            <Icon :name="social.icon" class="h-[1.1rem] w-[1.1rem]" />
          </a>
        </li>
      </ul>
    </div>

    <!-- FOTO REAL o FICHA ESTILO EDITOR -->
    <div class="rise min-w-0 lg:col-span-5" style="--d: 4">
      <figure v-if="profile.photo" class="mx-auto max-w-sm overflow-hidden rounded-2xl border border-line bg-surface">
        <img
          :src="profile.photo"
          :alt="`Fotografía de ${profile.name}`"
          class="aspect-4/5 h-full w-full object-cover"
          width="480"
          height="600"
        />
      </figure>

      <aside
        v-else
        class="theme-navy mx-auto max-w-md overflow-hidden rounded-2xl border border-line shadow-[0_30px_60px_-30px_rgb(11_37_69/0.6)]"
        aria-label="Resumen del perfil"
      >
        <!-- Barra de ventana -->
        <div class="flex items-center gap-2 border-b border-line bg-surface px-4 py-3" aria-hidden="true">
          <span class="h-2.5 w-2.5 rounded-full bg-line-strong"></span>
          <span class="h-2.5 w-2.5 rounded-full bg-line-strong"></span>
          <span class="h-2.5 w-2.5 rounded-full bg-accent"></span>
          <span class="ml-3 font-mono text-xs text-muted">perfil.ts</span>
        </div>

        <div class="p-5 font-mono text-[0.8rem] leading-7 sm:p-6 sm:text-sm">
          <p aria-hidden="true">
            <span class="text-accent">const</span> daniel <span class="text-muted">=</span> {
          </p>
          <dl class="pl-4 sm:pl-5">
            <div v-for="fact in about.facts" :key="fact.key" class="flex flex-wrap gap-x-2">
              <dt class="text-muted">
                <span class="sr-only">{{ fact.label }}</span>
                <span aria-hidden="true">{{ fact.key }}:</span>
              </dt>
              <dd class="min-w-0 text-ink">
                <span aria-hidden="true" class="text-accent">"</span>{{ fact.value }}<span aria-hidden="true" class="text-accent">"</span><span aria-hidden="true" class="text-muted">,</span>
              </dd>
            </div>
          </dl>
          <p aria-hidden="true">}</p>
        </div>
      </aside>
    </div>
  </section>
</template>
