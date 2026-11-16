<script setup>
// Etiqueta que aparece a la derecha de un ícono del sidebar contraído.
// Se muestra al pasar el mouse o al enfocar con teclado el elemento padre
// (que debe tener la clase `group` y `relative`). Es decorativa: el nombre
// accesible lo aporta el propio enlace o botón con aria-label.
defineProps({
  text: { type: String, required: true }
})
</script>

<template>
  <span
    aria-hidden="true"
    class="pointer-events-none absolute left-full top-1/2 z-50 ml-4 -translate-x-1 -translate-y-1/2 whitespace-nowrap
           rounded-md border border-line bg-surface px-3 py-1.5 text-sm font-medium text-ink opacity-0 shadow-lg
           transition duration-150 group-hover:translate-x-0 group-hover:opacity-100
           group-focus-visible:translate-x-0 group-focus-visible:opacity-100
           group-focus-within:translate-x-0 group-focus-within:opacity-100"
  >
    <!-- Flecha -->
    <span class="absolute -left-1 top-1/2 h-2 w-2 -translate-y-1/2 rotate-45 border-b border-l border-line bg-surface"></span>
    {{ text }}
  </span>
</template>
