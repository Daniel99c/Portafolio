<script setup>
// Encabezado de cada sección del portafolio. Cada sección es una página,
// por eso su título es el <h1>.
defineProps({
  title: { type: String, required: true },
  description: { type: String, default: '' }
})
</script>

<template>
  <header class="mb-10 md:mb-14">
    <span aria-hidden="true" class="block h-1 w-12 rounded-full bg-linear-to-r from-accent to-transparent"></span>
    <h1
      id="titulo-seccion"
      tabindex="-1"
      class="mt-5 font-display text-3xl font-semibold tracking-[-0.02em] text-ink focus:outline-none md:text-[2.75rem]"
    >
      {{ title }}
    </h1>
    <p v-if="description" class="mt-4 max-w-2xl text-base leading-relaxed text-muted md:text-lg">
      {{ description }}
    </p>
  </header>
</template>
