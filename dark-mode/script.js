// Detectar preferência do sistema
const prefersDarkScheme = window.matchMedia('(prefers-color-scheme: dark)').matches;

// Aplicar tema automaticamente (caso o usuário não tenha definido manualmente)
if (!localStorage.getItem('theme')) {
  document.body.classList.toggle('dark', prefersDarkScheme);
}

// Se quiser armazenar manualmente depois com um botão, você pode sobrescrever:
document.getElementById('toggle-theme').addEventListener('click', () => {
  const isDark = document.body.classList.toggle('dark');
  localStorage.setItem('theme', isDark ? 'dark' : 'light');
});
const savedTheme = localStorage.getItem('theme');
const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;

if (savedTheme) {
  document.body.classList.toggle('dark', savedTheme === 'dark');
} else {
  document.body.classList.toggle('dark', prefersDark);
}

