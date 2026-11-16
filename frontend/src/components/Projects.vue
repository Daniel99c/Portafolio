<script setup>
import { projects } from '../data/portfolio'
import { track } from '../services/api'
import SectionHeader from './SectionHeader.vue'
import Icon from './Icon.vue'
import ProjectCover from './ProjectCover.vue'

const statusStyle = {
  'En producción': 'bg-ok/12 text-ok',
  'Proyecto académico': 'bg-surface-2 text-muted',
  'En desarrollo': 'bg-accent-soft text-accent'
}
</script>

<template>
  <section aria-labelledby="titulo-seccion">
    <div>
      <SectionHeader
        title="Proyectos"
        description="Aplicaciones en las que he participado, con su estado real y los enlaces disponibles."
      />

      <ol class="grid gap-6 md:grid-cols-2">
        <li
          v-for="(project, i) in projects"
          :key="project.id"
          v-reveal
          class="min-w-0"
          :class="i === 0 && 'md:col-span-2'"
        >
          <article
            class="card group/card flex h-full flex-col overflow-hidden"
            :class="i === 0 && 'xl:grid xl:grid-cols-12'"
            :aria-labelledby="`proyecto-${project.id}`"
          >
            <!-- VISUAL: captura real o composición discreta -->
            <div
              class="relative border-b border-line bg-surface-2"
              :class="i === 0 ? 'xl:col-span-4 xl:border-b-0 xl:border-r' : ''"
            >
              <img
                v-if="project.image"
                :src="project.image.src"
                :alt="project.image.alt"
                loading="lazy"
                decoding="async"
                class="aspect-video h-full w-full object-cover"
              />
              <ProjectCover v-else :project="project" :large="i === 0" />
            </div>

            <div class="flex flex-1 flex-col p-6 md:p-7" :class="i === 0 && 'xl:col-span-8 xl:p-9'">
              <ul class="flex flex-wrap gap-2" aria-label="Estado">
                <li class="badge" :class="statusStyle[project.status]">
                  <span aria-hidden="true" class="h-1.5 w-1.5 rounded-full bg-current"></span>
                  {{ project.status }}
                </li>
                <li v-if="project.distinction" class="badge">
                  <Icon name="award" class="h-3.5 w-3.5" />
                  {{ project.distinction }}
                </li>
              </ul>

              <h2
                :id="`proyecto-${project.id}`"
                class="mt-4 font-display font-semibold leading-snug text-ink"
                :class="i === 0 ? 'text-2xl md:text-[1.75rem]' : 'text-xl md:text-2xl'"
              >
                {{ project.title }}
              </h2>

              <p class="mt-3 leading-relaxed text-muted">{{ project.description }}</p>

              <dl class="mt-5 grid gap-3 text-sm">
                <div>
                  <dt class="eyebrow">Rol</dt>
                  <dd class="mt-1 font-medium text-ink">{{ project.role }}</dd>
                </div>
                <div v-if="project.participation">
                  <dt class="eyebrow">Participación</dt>
                  <dd class="mt-1 text-ink">{{ project.participation }}</dd>
                </div>
              </dl>

              <ul class="mt-5 flex flex-wrap gap-2" aria-label="Tecnologías">
                <li v-for="t in project.tech" :key="t" class="chip font-mono text-xs">{{ t }}</li>
              </ul>

              <!-- DETALLE (solo información confirmada) -->
              <details v-if="project.details.length" class="group mt-6 rounded-xl border border-line">
                <summary
                  class="flex list-none items-center justify-between gap-4 rounded-xl px-4 py-3 text-sm font-semibold text-ink
                         transition-colors hover:text-accent [&::-webkit-details-marker]:hidden"
                >
                  Ver detalle del proyecto
                  <Icon name="chevron" class="h-4 w-4 transition-transform duration-200 group-open:rotate-180" />
                </summary>
                <dl class="space-y-4 border-t border-line px-4 py-4 text-sm">
                  <div v-for="d in project.details" :key="d.label">
                    <dt class="font-semibold text-ink">{{ d.label }}</dt>
                    <dd class="mt-1 leading-relaxed text-muted">{{ d.text }}</dd>
                  </div>
                </dl>
              </details>

              <div v-if="project.repo" class="mt-auto pt-6">
                <a
                  :href="project.repo"
                  target="_blank"
                  rel="noopener noreferrer"
                  class="btn btn-ghost min-h-0 px-4 py-2 text-sm"
                  @click="track('repo', project.title)"
                >
                  <Icon name="github" class="h-4 w-4" />
                  Ver repositorio
                  <span class="sr-only">de {{ project.title }} en GitHub (se abre en una pestaña nueva)</span>
                  <Icon name="external" class="h-3.5 w-3.5" />
                </a>
              </div>
            </div>
          </article>
        </li>
      </ol>
    </div>
  </section>
</template>
