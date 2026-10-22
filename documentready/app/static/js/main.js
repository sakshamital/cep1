/**
 * main.js — Bootstraps the application.
 */
import './ui.js';
import './api.js';
import { initI18n, setLocale, getLocale } from './i18n.js';
import { initStateSelector } from './state-selector.js';

// ── Initialise i18n ──────────────────────────────────────────────────────────

initI18n().then(() => {
  _setupLangSelector();
});

// ── Initialise state selector ────────────────────────────────────────────────

initStateSelector();

// ── Language selector wiring ─────────────────────────────────────────────────

function _setupLangSelector() {
  const btn = document.getElementById('lang-btn');
  const menu = document.getElementById('lang-menu');
  const label = document.getElementById('lang-btn-label');
  if (!btn || !menu) return;

  // Set initial label
  const locale = getLocale();
  const labelMap = { en: 'EN', hi: 'हिं', mr: 'मर' };
  label.textContent = labelMap[locale] || 'EN';

  // Mark the active item
  menu.querySelectorAll('[data-lang]').forEach(li => {
    li.setAttribute('aria-selected', li.dataset.lang === locale ? 'true' : 'false');
  });

  // Toggle menu
  btn.addEventListener('click', (e) => {
    e.stopPropagation();
    const expanded = btn.getAttribute('aria-expanded') === 'true';
    btn.setAttribute('aria-expanded', String(!expanded));
    menu.hidden = expanded;
  });

  // Select a language
  menu.addEventListener('click', async (e) => {
    const li = e.target.closest('[data-lang]');
    if (!li) return;

    const lang = li.dataset.lang;
    await setLocale(lang);

    label.textContent = labelMap[lang] || 'EN';
    menu.querySelectorAll('[data-lang]').forEach(item => {
      item.setAttribute('aria-selected', item.dataset.lang === lang ? 'true' : 'false');
    });
    menu.hidden = true;
    btn.setAttribute('aria-expanded', 'false');
  });

  // Close on outside click
  document.addEventListener('click', (e) => {
    if (!btn.contains(e.target) && !menu.contains(e.target)) {
      menu.hidden = true;
      btn.setAttribute('aria-expanded', 'false');
    }
  });
}

console.log('DocumentReady initialised.');
