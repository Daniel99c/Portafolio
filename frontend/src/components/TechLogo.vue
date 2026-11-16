<script setup>
import { computed } from 'vue'
import { techLogo } from '../data/techLogos'
import Icon from './Icon.vue'

// Logo decorativo: el nombre de la tecnología siempre se muestra junto a él.
const props = defineProps({
  name: { type: String, required: true }
})

const logo = computed(() => techLogo(props.name))
</script>

<template>
  <svg
    v-if="logo?.path"
    viewBox="0 0 24 24"
    aria-hidden="true"
    focusable="false"
    :style="{ color: logo.color ?? 'var(--ink)' }"
    fill="currentColor"
  >
    <path :d="logo.path" />
  </svg>
  <Icon v-else-if="logo?.icon" :name="logo.icon" class="text-muted" />
</template>
