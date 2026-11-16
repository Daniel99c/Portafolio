// Contenido del portafolio. Se administra desde el panel de Django; estos datos
// son la copia de respaldo que se muestra si el backend no está disponible.
// Al cargar la página, loadPortfolio() los reemplaza por los del backend.
import { fetchPortfolio } from '../services/api'

export const profile = {
  name: 'Daniel Enrique Cáceres Torres',
  shortName: 'Daniel Cáceres',
  title: 'Desarrollador de Software',
  stackLine: ['PHP', 'Laravel', 'React', 'PostgreSQL'],
  profession: 'Ingeniero de Sistemas',
  location: 'Pasto, Nariño, Colombia',
  summary:
    'Desarrollo y mantengo aplicaciones web para los sectores tributario, salud y académico. Combino desarrollo full-stack, bases de datos, pruebas y soporte de sistemas en producción.',
  badges: ['Grado de Honor', 'Tesis laureada', 'Experiencia en producción'],
  // Ruta a una fotografía real (por ejemplo '/img/daniel.jpg'). Vacía = se muestra la ficha.
  photo: '',
  cv: {
    url: '/cv/cv-daniel-caceres.pdf',
    downloadUrl: '/cv/cv-daniel-caceres.pdf',
    downloadName: 'CV_Daniel_Caceres_Torres.pdf'
  }
}

// El correo se guarda por partes y se arma solo al usarlo, para que los
// bots que buscan direcciones en el código no lo encuentren completo.
let emailParts = ['daniele.caceres212', 'umariana', 'edu', 'co']

export const getEmail = () => `${emailParts[0]}@${emailParts.slice(1).join('.')}`

export const openMail = () => {
  window.location.href = `mailto:${getEmail()}`
}

export const contact = {
  github: 'https://github.com/Daniel99c',
  linkedin: 'https://www.linkedin.com/in/daniel-enrique-caceres-torres-b70ab432b'
}

// Cada sección es una ruta: /portafolio/<id>
export const sections = [
  { id: 'sobre-mi', label: 'Sobre mí', title: 'Sobre mí', icon: 'user' },
  { id: 'experiencia', label: 'Experiencia', title: 'Experiencia', icon: 'briefcase' },
  { id: 'proyectos', label: 'Proyectos', title: 'Proyectos', icon: 'folder' },
  { id: 'formacion', label: 'Formación', title: 'Formación y certificaciones', icon: 'cap' },
  { id: 'hoja-de-vida', label: 'Hoja de vida', title: 'Hoja de vida', icon: 'file' }
]

export const about = {
  paragraphs: [
    'Soy Daniel Enrique Cáceres Torres, Ingeniero de Sistemas de la Universidad Mariana, graduado el 6 de abril de 2026 con Grado de Honor y tesis laureada.',
    'Mi enfoque principal es el desarrollo de aplicaciones web con PHP, Laravel, React, TypeScript y PostgreSQL. Tengo experiencia en soluciones para los sectores tributario, salud y académico, combinando desarrollo, bases de datos, pruebas, despliegue y soporte a usuarios.',
    'Actualmente trabajo en DataSoft Ingeniería, donde realizo mantenimiento de aplicaciones PHP, diagnóstico de incidencias y corrección de datos en los sistemas tributarios de la Gobernación de Nariño.',
    'Me interesa construir soluciones útiles y mantenibles, comprender los procesos que resuelven y participar en su mejora continua.'
  ],
  approach: [
    'Comprender el problema y el proceso de negocio.',
    'Desarrollar, probar y documentar soluciones mantenibles.',
    'Diagnosticar incidencias y validar cambios antes de llevarlos a producción.'
  ],
  facts: [
    { key: 'ubicacion', label: 'Ubicación', value: 'Pasto, Nariño, Colombia' },
    { key: 'profesion', label: 'Profesión', value: 'Ingeniero de Sistemas' },
    { key: 'graduacion', label: 'Graduación', value: '6 de abril de 2026 · Universidad Mariana' },
    { key: 'actualmente', label: 'Actualmente', value: 'DataSoft Ingeniería Ltda.' }
  ]
}

// Sin niveles ni porcentajes: solo agrupación por uso.
export const stack = [
  {
    title: 'Stack principal',
    primary: true,
    items: ['PHP nativo', 'Laravel', 'React', 'TypeScript', 'JavaScript', 'PostgreSQL', 'SQL', 'Git', 'API REST']
  },
  {
    title: 'Complementarias',
    items: ['Filament', 'Inertia.js', 'Python', 'Django', 'Astro', 'MySQL', 'SQL Server', 'HTML5', 'CSS3']
  },
  {
    title: 'Calidad y herramientas',
    items: ['PHPUnit', 'Artillery', 'GitHub', 'GitLab', 'XAMPP', 'pgAdmin', 'MySQL Workbench']
  },
  {
    title: 'Metodologías y documentación',
    items: ['Scrum', 'Metodologías ágiles', 'Astro para documentación técnica']
  },
  {
    title: 'Herramientas de apoyo',
    items: ['Claude Code', 'ChatGPT']
  }
]

// Ordenada de la más reciente a la más antigua.
export const experience = [
  {
    company: 'DataSoft Ingeniería Ltda.',
    role: 'Soporte Técnico en Sitio',
    context: 'Gobernación de Nariño · Pasto',
    period: 'Febrero de 2026 – Actualidad',
    current: true,
    note: 'Funciones de desarrollo PHP, bases de datos y soporte de aplicaciones.',
    description:
      'Realizo mantenimiento y corrección de aplicaciones PHP para tres sistemas tributarios de la Gobernación de Nariño: Impuesto Vehicular —SISCAR—, Estampillas y Tasa Pro Deporte.',
    groups: [
      {
        title: 'Desarrollo y mantenimiento',
        items: [
          'Ajustes y correcciones de código PHP, incluida la compatibilidad con ADOdb Lite y FPDF.',
          'Pruebas locales con XAMPP y PHP 8, y despliegue de ajustes a producción.'
        ]
      },
      {
        title: 'Bases de datos PostgreSQL',
        items: [
          'Diagnóstico de incidencias con consultas SQL y revisión de triggers, funciones, procedimientos almacenados y vistas.',
          'Depuración de duplicados, ajuste de estados y validación de correcciones mediante BEGIN, COMMIT y ROLLBACK.'
        ]
      },
      {
        title: 'Operación y soporte',
        items: [
          'Generación y validación de reportes resumidos y detallados de dispersión de recaudos.',
          'Atención de incidencias y apoyo a procesos PSE, archivos Asobancaria y firma electrónica.'
        ]
      }
    ],
    tech: ['PHP 8', 'PostgreSQL', 'SQL', 'XAMPP', 'ADOdb Lite', 'FPDF']
  },
  {
    company: 'Unidad Cardioquirúrgica de Nariño',
    role: 'Desarrollador de Software — Practicante',
    context: 'Pasto, Nariño',
    period: '2025',
    groups: [
      {
        items: [
          'Soporte y participación en el desarrollo final de un sistema de gestión de quirófano en PHP nativo para admisiones, programación de procedimientos y transacciones del ciclo quirúrgico.',
          'Desarrollo de una aplicación en PHP nativo para visualizar el estado de las cirugías, desde el ingreso hasta la salida o traslado del paciente.',
          'Desarrollo de una aplicación de Atención Primaria en Salud con Laravel, React, TypeScript e Inertia.js.',
          'Pruebas unitarias con PHPUnit y pruebas de carga con Artillery.'
        ]
      }
    ],
    tech: ['PHP nativo', 'Laravel', 'React', 'TypeScript', 'Inertia.js', 'PHPUnit', 'Artillery']
  },
  {
    company: 'Calzado Nueva Moda',
    role: 'Asistente Administrativo',
    context: 'Bogotá D.C.',
    period: '2018',
    minor: true,
    description:
      'Apoyo en gestión documental, control de inventario, atención al cliente, pedidos, seguimiento a proveedores e informes administrativos.'
  }
]

// Las secciones de detalle solo incluyen información confirmada.
export const projects = [
  {
    id: 'biblioteca',
    title: 'Sistema de Gestión Bibliotecaria — Maridiaz',
    status: 'En producción',
    distinction: 'Tesis laureada',
    role: 'Investigador y desarrollador principal',
    description:
      'Sistema web que digitaliza procesos bibliotecarios antes realizados manualmente y actualmente ayuda a optimizar la gestión de una colección de más de 40.000 libros. Incluye funcionalidades de catalogación, préstamos y consultas.',
    participation: 'Diseño, desarrollo y despliegue de la solución.',
    tech: ['Laravel 12', 'PHP', 'React', 'TypeScript', 'Inertia.js', 'Tailwind CSS'],
    // Captura real del sistema, si se incorpora: { src: '/img/proyectos/biblioteca.webp', alt: '...' }
    image: null,
    // Única acción externa permitida para este proyecto.
    repo: 'https://github.com/Daniel99c/gestionBibliotecaMaridiaz',
    details: [
      { label: 'Contexto', text: 'Proyecto de grado para optar al título de Ingeniero de Sistemas en la Universidad Mariana.' },
      { label: 'Problema', text: 'Los procesos bibliotecarios se realizaban de forma manual.' },
      { label: 'Mi participación', text: 'Investigador y desarrollador principal: diseño, desarrollo y despliegue de la solución.' },
      { label: 'Solución implementada', text: 'Aplicación web con funcionalidades de catalogación, préstamos y consultas.' },
      {
        label: 'Detalle técnico',
        text: 'Construido sobre el React Starter Kit de Laravel: Laravel 12 con PHP 8.2, React con TypeScript e Inertia.js, y Tailwind CSS.'
      },
      {
        label: 'Evidencia disponible',
        text: 'Repositorio público. Tesis laureada y presentada en la fase Nodal de Semilleros de Investigación y en el Congreso Internacional de Ciencias de la Información —CICI—.'
      },
      { label: 'Estado actual', text: 'En producción.' }
    ]
  },
  {
    id: 'egresados',
    title: 'Sistema de Egresados',
    status: 'Proyecto académico',
    role: 'Desarrollador full-stack',
    description:
      'Aplicación web para administrar información personal, académica y laboral de egresados universitarios, con distintos roles, control de acceso e integración entre backend y frontend.',
    participation: 'Desarrollo full-stack de la aplicación.',
    tech: ['Laravel 12', 'PHP', 'React', 'TypeScript', 'Inertia.js', 'Tailwind CSS'],
    image: null,
    repo: 'https://github.com/Daniel99c/Sistema-de-Egresados',
    details: [
      { label: 'Contexto', text: 'Proyecto académico orientado a los egresados del programa de Ingeniería de Sistemas de la Universidad Mariana.' },
      { label: 'Mi participación', text: 'Desarrollador full-stack.' },
      {
        label: 'Detalle técnico',
        text: 'Construido sobre el React Starter Kit de Laravel: Laravel 12 con PHP 8.2, React con TypeScript e Inertia.js, y Tailwind CSS.'
      },
      { label: 'Evidencia disponible', text: 'Repositorio público.' },
      { label: 'Estado actual', text: 'Proyecto académico.' }
    ]
  },
  {
    id: 'portafolio',
    title: 'Portafolio profesional',
    status: 'En desarrollo',
    role: 'Diseño y desarrollo',
    description:
      'Portafolio personal para presentar mi experiencia, proyectos y habilidades en desarrollo de software, con una interfaz responsive y contenido organizado.',
    tech: ['Vue.js', 'Tailwind CSS', 'Vite'],
    image: null,
    repo: null,
    details: []
  }
]

export const education = {
  degree: {
    title: 'Ingeniería de Sistemas',
    institution: 'Universidad Mariana',
    date: 'Graduación: 6 de abril de 2026',
    honors: ['Grado de Honor', 'Tesis laureada: Sistema de Gestión Bibliotecaria']
  },
  research: {
    title: 'Ponente',
    text: 'Presentación del Sistema de Gestión Bibliotecaria en la fase Nodal de Semilleros de Investigación y en el Congreso Internacional de Ciencias de la Información —CICI—.'
  }
}

// 15 documentos originales en /public/certificates.
// type: Título | Constancia de curso | Certificado de curso | Certificado de participación
// publicFile: false cuando el PDF muestra un número de identificación; el archivo
// se conserva intacto, pero no se enlaza desde el sitio.
export const certificates = [
  { title: 'Fundamentos de Python 2', issuer: 'Cisco Networking Academy', type: 'Certificado de curso', year: '2026', file: 'certificado-python-2.pdf', publicFile: true, featured: true },
  { title: 'Fundamentos de Python 1', issuer: 'Cisco Networking Academy', type: 'Certificado de curso', year: '2025', file: 'certificado-python.pdf', publicFile: true, featured: true },
  { title: 'Desarrollo de Aplicaciones Web con PHP', issuer: 'SENA', type: 'Constancia de curso', year: '2024', hours: 80, file: 'aplicaciones-web-php.pdf', publicFile: false, featured: true },
  { title: 'Construcción de Bases de Datos con MySQL', issuer: 'SENA', type: 'Constancia de curso', year: '2024', hours: 48, file: 'bases-datos-mysql.pdf', publicFile: false, featured: true },
  { title: 'Java Fundamentals', issuer: 'Oracle Academy', type: 'Certificado de curso', year: '2022', file: 'certificado-oracle.pdf', publicFile: true, featured: true },
  { title: 'Inmersión IA', issuer: 'Alura con Google Gemini', type: 'Certificado de participación', year: '2025', hours: 6, file: 'inmersion-ia.pdf', publicFile: true, featured: true },
  { title: 'Ética Profesional', issuer: 'COPNIA', type: 'Certificado de curso', year: '2022', hours: 36, file: 'certificado-copnia.pdf', publicFile: false },
  { title: 'Tecnólogo en Gestión Empresarial', issuer: 'SENA', type: 'Título', year: '2019', file: 'gestion-empresarial.pdf', publicFile: false },
  { title: 'Aplicación de Herramientas Metodológicas en Investigación', issuer: 'SENA', type: 'Constancia de curso', year: '2018', hours: 50, file: 'herramientas-metodologicas.pdf', publicFile: false },
  { title: 'Técnico en Contabilización de Operaciones Comerciales y Financieras', issuer: 'SENA', type: 'Título', year: '2016', file: 'contabilizacion-operaciones-comerciales-financieras.pdf', publicFile: false },
  { title: 'Bachiller Académico', issuer: 'Colegio León Magno', type: 'Título', year: '2016', file: 'colegio-leon-magno.pdf', publicFile: false },
  { title: 'Contabilidad en las Organizaciones', issuer: 'SENA', type: 'Constancia de curso', year: '2015', hours: 40, file: 'contabilidad-organizaciones.pdf', publicFile: false },
  { title: 'Salud Ocupacional: Seguridad y Salud en el Trabajo', issuer: 'SENA', type: 'Constancia de curso', year: '2015', hours: 40, file: 'seguridad-salud-trabajo.pdf', publicFile: false },
  { title: 'Aprendiz Digital', issuer: 'SENA', type: 'Constancia de curso', year: '2015', hours: 60, file: 'aprendiz-digital.pdf', publicFile: false },
  { title: 'Inglés para principiantes (English Dot Works Beginner)', issuer: 'SENA', type: 'Constancia de curso', year: '2015', hours: 60, file: 'ingles.pdf', publicFile: false }
]

// Reemplaza el contenido por el del backend, sin cambiar las referencias que
// ya importaron los componentes. Se llama una vez, antes de montar la app.
const replaceList = (target, items) => target.splice(0, target.length, ...items)

export const loadPortfolio = async () => {
  const data = await fetchPortfolio()
  if (!data) return false

  const { emailParts: parts, ...remoteProfile } = data.profile
  if (parts?.length > 1) emailParts = parts
  // Sin hoja de vida subida al admin, se conserva la del frontend
  if (!remoteProfile.cv.url) delete remoteProfile.cv
  Object.assign(profile, remoteProfile)
  Object.assign(contact, data.contact)
  Object.assign(about, data.about)
  Object.assign(education, data.education)
  replaceList(stack, data.stack)
  replaceList(experience, data.experience)
  replaceList(projects, data.projects)
  replaceList(certificates, data.certificates)
  return true
}

