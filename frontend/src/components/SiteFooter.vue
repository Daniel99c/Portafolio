<script setup>
import { ref } from 'vue'
import { profile, contact, getEmail, openMail } from '../data/portfolio'
import Icon from './Icon.vue'
import ContactModal from './ContactModal.vue'

const year = new Date().getFullYear()
const email = getEmail()
const showForm = ref(false)

const links = [
  { label: 'GitHub', value: 'github.com/Daniel99c', href: contact.github, icon: 'github' },
  { label: 'LinkedIn', value: profile.name, href: contact.linkedin, icon: 'linkedin' }
]
</script>

<template>
  <footer id="contacto" aria-labelledby="contacto-titulo" class="theme-navy relative overflow-hidden border-t border-line">
    <span aria-hidden="true" class="absolute inset-x-0 top-0 h-px bg-linear-to-r from-transparent via-accent to-transparent"></span>

    <div class="mx-auto max-w-5xl px-5 py-14 md:px-10 md:py-16">
      <div class="grid gap-10 xl:grid-cols-12 xl:items-end">
        <div class="min-w-0 xl:col-span-7">
          <p class="eyebrow">Contacto</p>
          <h2 id="contacto-titulo" class="mt-3 font-display text-3xl font-semibold tracking-[-0.02em] md:text-4xl">
            Conversemos
          </h2>
          <p class="mt-3 max-w-lg leading-relaxed text-muted">
            Envíame un mensaje, escríbeme por correo o encuéntrame en GitHub y LinkedIn.
          </p>
          <div>
            <button type="button" class="btn btn-primary mt-6" aria-haspopup="dialog" @click="showForm = true">
              <Icon name="chat" class="h-4 w-4" />
              Enviar un mensaje
            </button>
          </div>
          <a
            href="#contacto"
            @click.prevent="openMail"
            class="mt-5 inline-flex max-w-full items-center gap-3 rounded-lg font-display text-base font-semibold text-accent
                   underline decoration-accent/40 underline-offset-[6px] transition-colors hover:decoration-accent sm:text-lg"
          >
            <Icon name="mail" class="h-5 w-5 shrink-0" />
            <span class="break-all">{{ email }}</span>
          </a>
        </div>

        <ul class="space-y-3 xl:col-span-5">
          <li v-for="link in links" :key="link.label">
            <a
              :href="link.href"
              target="_blank"
              rel="noopener noreferrer"
              class="flex items-center gap-4 rounded-xl border border-line bg-surface/60 p-4 transition-colors hover:border-accent"
            >
              <Icon :name="link.icon" class="h-5 w-5 shrink-0 text-accent" />
              <span class="min-w-0">
                <span class="block text-sm font-semibold">{{ link.label }}</span>
                <span class="block truncate text-sm text-muted">{{ link.value }}</span>
              </span>
              <span class="sr-only">(se abre en una pestaña nueva)</span>
              <Icon name="external" class="ml-auto h-4 w-4 shrink-0 text-muted" />
            </a>
          </li>
          <li class="flex items-center gap-4 px-4 py-2 text-sm text-muted">
            <Icon name="pin" class="h-5 w-5 shrink-0 text-accent" />
            {{ profile.location }}
          </li>
        </ul>
      </div>

      <p class="mt-12 border-t border-line pt-6 text-sm text-muted">© {{ year }} {{ profile.name }}</p>
    </div>
    <!-- Fuera del pie oscuro para que siga el tema de la página -->
    <Teleport to="body">
      <ContactModal :open="showForm" @close="showForm = false" />
    </Teleport>
  </footer>
</template>
