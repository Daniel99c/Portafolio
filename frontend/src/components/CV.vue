<script setup>
import { profile } from '../data/portfolio'
import SectionHeader from './SectionHeader.vue'
import Icon from './Icon.vue'

const fileName = profile.cv.downloadName
</script>

<template>
  <section aria-labelledby="titulo-seccion">
    <SectionHeader
      title="Hoja de vida"
      description="Consulta o descarga la hoja de vida en PDF."
    />

    <div class="flex flex-col gap-3 sm:flex-row">
      <a :href="profile.cv.downloadUrl" :download="profile.cv.downloadName" class="btn btn-primary">
        <Icon name="download" class="h-4 w-4" />
        Descargar PDF
      </a>
      <a :href="profile.cv.url" target="_blank" rel="noopener noreferrer" class="btn btn-ghost">
        <Icon name="external" class="h-4 w-4" />
        Ver hoja de vida
        <span class="sr-only">(PDF, se abre en una pestaña nueva)</span>
      </a>
    </div>

    <!-- Vista previa (los navegadores móviles suelen no mostrar PDF incrustados) -->
    <figure class="theme-navy mt-8 hidden overflow-hidden rounded-2xl border border-line sm:block">
      <figcaption class="flex items-center justify-between gap-4 border-b border-line bg-surface px-4 py-3">
        <span class="flex items-center gap-2" aria-hidden="true">
          <span class="h-2.5 w-2.5 rounded-full bg-line-strong"></span>
          <span class="h-2.5 w-2.5 rounded-full bg-line-strong"></span>
          <span class="h-2.5 w-2.5 rounded-full bg-accent"></span>
        </span>
        <span class="truncate font-mono text-xs text-muted">{{ fileName }}</span>
        <span class="font-mono text-xs text-muted">PDF</span>
      </figcaption>
      <iframe
        :src="`${profile.cv.url}#view=FitH`"
        title="Vista previa de la hoja de vida"
        loading="lazy"
        class="block h-[80svh] w-full bg-white"
      ></iframe>
    </figure>
  </section>
</template>
