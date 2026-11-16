<script setup>
import { ref, computed, nextTick } from 'vue'
import { education, certificates } from '../data/portfolio'
import SectionHeader from './SectionHeader.vue'
import DocumentViewer from './DocumentViewer.vue'
import Icon from './Icon.vue'

const showAll = ref(false)
const list = ref(null)
const openDoc = ref(null)

const featured = certificates.filter((c) => c.featured)
const restCount = certificates.length - featured.length
const visible = computed(() => (showAll.value ? certificates : featured))

const meta = (cert) => [cert.issuer, cert.year, cert.hours && `${cert.hours} h`].filter(Boolean).join(' · ')

const toggle = async () => {
  showAll.value = !showAll.value
  // Lleva el foco al primer documento revelado (teclado y lectores de pantalla)
  if (showAll.value) {
    await nextTick()
    list.value?.children[featured.length]?.querySelector('button, [tabindex]')?.focus()
  }
}

const view = (cert) => {
  openDoc.value = {
    title: cert.title,
    subtitle: `${cert.type} · ${meta(cert)}`,
    // Del backend llega fileUrl; sin backend se usa la copia del frontend
    url: cert.fileUrl || `/certificates/${cert.file}`,
    downloadUrl: cert.fileUrl ? `${cert.fileUrl}?download=1` : undefined,
    downloadName: `${cert.title}.pdf`
  }
}
</script>

<template>
  <section aria-labelledby="titulo-seccion">
    <SectionHeader title="Formación y certificaciones" />

    <!-- DESTACADOS -->
    <div class="grid gap-5 xl:grid-cols-12">
      <article class="card relative overflow-hidden p-6 md:p-8 xl:col-span-7">
        <span aria-hidden="true" class="absolute inset-y-0 left-0 w-1 bg-linear-to-b from-navy to-accent"></span>
        <p class="eyebrow">Pregrado</p>
        <h2 class="mt-3 font-display text-2xl font-semibold text-ink md:text-[1.75rem]">{{ education.degree.title }}</h2>
        <p class="mt-1 font-semibold text-accent">{{ education.degree.institution }}</p>
        <p class="mt-1 text-muted">{{ education.degree.date }}</p>
        <ul class="mt-5 flex flex-wrap gap-2" aria-label="Distinciones">
          <li v-for="honor in education.degree.honors" :key="honor" class="badge">
            <Icon name="award" class="h-3.5 w-3.5" />
            {{ honor }}
          </li>
        </ul>
      </article>

      <article class="card p-6 md:p-8 xl:col-span-5">
        <p class="eyebrow">Investigación</p>
        <h2 class="mt-3 font-display text-xl font-semibold text-ink">{{ education.research.title }}</h2>
        <p class="mt-3 leading-relaxed text-muted">{{ education.research.text }}</p>
      </article>
    </div>

    <!-- DOCUMENTOS -->
    <div v-reveal class="mt-14">
      <div class="flex flex-wrap items-end justify-between gap-3">
        <h2 class="font-display text-xl font-semibold text-ink md:text-2xl">Cursos, títulos y certificados</h2>
        <p class="font-mono text-xs text-muted">{{ certificates.length }} documentos</p>
      </div>

      <ul id="formacion-lista" ref="list" class="mt-6 grid gap-3 md:grid-cols-2">
        <li v-for="cert in visible" :key="cert.id ?? cert.file">
          <!-- Toda la tarjeta abre el visor -->
          <button
            v-if="cert.publicFile"
            type="button"
            class="card group flex h-full w-full items-start justify-between gap-4 p-5 text-left transition-colors hover:border-accent"
            @click="view(cert)"
          >
            <span class="min-w-0">
              <span class="block text-xs font-semibold uppercase tracking-wide text-accent">{{ cert.type }}</span>
              <span class="mt-1.5 block font-semibold leading-snug text-ink">{{ cert.title }}</span>
              <span class="mt-1 block text-sm text-muted">{{ meta(cert) }}</span>
            </span>
            <span class="icon-btn shrink-0 group-hover:border-accent group-hover:text-accent" aria-hidden="true">
              <Icon name="file" class="h-[1.1rem] w-[1.1rem]" />
            </span>
            <span class="sr-only">— ver documento</span>
          </button>

          <div v-else tabindex="-1" class="card flex h-full items-start justify-between gap-4 p-5 focus:outline-none">
            <div class="min-w-0">
              <p class="text-xs font-semibold uppercase tracking-wide text-accent">{{ cert.type }}</p>
              <p class="mt-1.5 font-semibold leading-snug text-ink">{{ cert.title }}</p>
              <p class="mt-1 text-sm text-muted">{{ meta(cert) }}</p>
              <p class="mt-2 font-mono text-xs text-muted">Soporte disponible a solicitud</p>
            </div>
          </div>
        </li>
      </ul>

      <div class="mt-6 flex justify-center">
        <button
          type="button"
          class="btn btn-ghost"
          :aria-expanded="showAll"
          aria-controls="formacion-lista"
          @click="toggle"
        >
          {{ showAll ? 'Mostrar menos' : `Ver toda la formación (${restCount} más)` }}
          <Icon name="chevron" class="h-4 w-4 transition-transform duration-200" :class="showAll && 'rotate-180'" />
        </button>
      </div>
    </div>

    <DocumentViewer :doc="openDoc" @close="openDoc = null" />
  </section>
</template>
