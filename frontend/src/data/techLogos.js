// Logos de tecnologías. Las marcas vienen de simple-icons (CC0);
// las que no tienen logo oficial usan un ícono genérico de Icon.vue.
import {
  siPhp,
  siLaravel,
  siReact,
  siTypescript,
  siJavascript,
  siPostgresql,
  siGit,
  siFilament,
  siInertia,
  siPython,
  siDjango,
  siAstro,
  siMysql,
  siHtml5,
  siCss,
  siGithub,
  siGitlab,
  siXampp,
  siClaude,
  siVuedotjs,
  siTailwindcss,
  siVite
} from 'simple-icons'

const logos = {
  'PHP nativo': siPhp,
  PHP: siPhp,
  'PHP 8': siPhp,
  Laravel: siLaravel,
  'Laravel 12': siLaravel,
  React: siReact,
  TypeScript: siTypescript,
  JavaScript: siJavascript,
  PostgreSQL: siPostgresql,
  Git: siGit,
  Filament: siFilament,
  'Inertia.js': siInertia,
  Python: siPython,
  Django: siDjango,
  Astro: siAstro,
  'Astro para documentación técnica': siAstro,
  MySQL: siMysql,
  HTML5: siHtml5,
  CSS3: siCss,
  GitHub: siGithub,
  GitLab: siGitlab,
  XAMPP: siXampp,
  'Claude Code': siClaude,
  'Vue.js': siVuedotjs,
  'Tailwind CSS': siTailwindcss,
  Vite: siVite
}

const generic = {
  SQL: 'database',
  'SQL Server': 'database',
  pgAdmin: 'database',
  'MySQL Workbench': 'database',
  'API REST': 'api',
  PHPUnit: 'test',
  Artillery: 'test',
  Scrum: 'cycle',
  'Metodologías ágiles': 'cycle',
  ChatGPT: 'chat'
}

// Colores de marca muy oscuros se pierden en el tema oscuro:
// en esos casos el logo usa el color del texto.
const isTooDark = (hex) => {
  const [r, g, b] = [0, 2, 4].map((i) => parseInt(hex.slice(i, i + 2), 16) / 255)
  return 0.2126 * r + 0.7152 * g + 0.0722 * b < 0.18
}

/** Devuelve { path, color } para una marca, { icon } para un genérico, o null. */
export function techLogo(name) {
  const brand = logos[name]
  if (brand) {
    return { path: brand.path, color: isTooDark(brand.hex) ? null : `#${brand.hex}` }
  }
  return generic[name] ? { icon: generic[name] } : null
}
