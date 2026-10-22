/**
 * i18n.js — Client-side internationalisation engine.
 *
 * Supported locales: en, hi, mr
 */

const STORAGE_KEY = 'documentready:locale';
const SUPPORTED = ['en', 'hi', 'mr'];
const DEFAULT_LOCALE = 'en';

let _strings = {};  // current locale strings
let _fallback = {}; // English fallback
let _locale = DEFAULT_LOCALE;
const _listeners = new Set();

/**
 * Initialise i18n. Loads the saved locale (or default) and applies translations.
 */
export async function initI18n() {
  const saved = _readStorage();
  _locale = SUPPORTED.includes(saved) ? saved : DEFAULT_LOCALE;

  // Always load English as fallback
  _fallback = await _fetchLocale('en');

  if (_locale !== 'en') {
    _strings = await _fetchLocale(_locale);
  } else {
    _strings = _fallback;
  }

  _applyAll();
  _updateHtmlLang();
  _notifyListeners();
}

/**
 * Switch locale.
 * @param {string} locale - 'en', 'hi', or 'mr'
 */
export async function setLocale(locale) {
  if (!SUPPORTED.includes(locale)) return;
  if (locale === _locale) return;

  _locale = locale;
  _writeStorage(locale);

  if (locale === 'en') {
    _strings = _fallback;
  } else {
    _strings = await _fetchLocale(locale);
  }

  _applyAll();
  _updateHtmlLang();
  _notifyListeners();
  document.dispatchEvent(new CustomEvent('localechange', { detail: { locale } }));
}

/**
 * Get the current locale code.
 * @returns {string}
 */
export function getLocale() {
  return _locale;
}

/**
 * Get a translated string by key, with optional parameter substitution.
 * @param {string} key
 * @param {Object} [params]
 * @returns {string}
 */
export function t(key, params = null) {
  let val = _strings[key] || _fallback[key] || key;
  if (params && typeof val === 'string') {
    for (const [k, v] of Object.entries(params)) {
      val = val.replace(new RegExp(`\\{${k}\\}`, 'g'), String(v));
    }
  }
  return val;
}

/**
 * Translate document name by ID.
 * @param {string} docId
 * @param {string} [defaultName]
 * @returns {string}
 */
export function tDoc(docId, defaultName = '') {
  if (!docId) return defaultName;
  const key = `doc_${docId}_name`;
  return _strings[key] || _fallback[key] || defaultName || docId;
}

/**
 * Translate document note by ID.
 * @param {string} docId
 * @param {string} [defaultNote]
 * @returns {string}
 */
export function tDocNote(docId, defaultNote = '') {
  if (!docId) return defaultNote;
  const key = `doc_note_${docId}`;
  return _strings[key] || _fallback[key] || defaultNote;
}

/**
 * Translate service name by ID.
 * @param {string} svcId
 * @param {string} [defaultName]
 * @returns {string}
 */
export function tSvc(svcId, defaultName = '') {
  if (!svcId) return defaultName;
  const key = `svc_${svcId}_name`;
  return _strings[key] || _fallback[key] || defaultName || svcId;
}

/**
 * Translate service description by ID.
 * @param {string} svcId
 * @param {string} [defaultDesc]
 * @returns {string}
 */
export function tSvcDesc(svcId, defaultDesc = '') {
  if (!svcId) return defaultDesc;
  const key = `svc_${svcId}_desc`;
  return _strings[key] || _fallback[key] || defaultDesc;
}

/**
 * Translate service department by ID.
 * @param {string} svcId
 * @param {string} [defaultDept]
 * @returns {string}
 */
export function tSvcDept(svcId, defaultDept = '') {
  if (!svcId) return defaultDept;
  const key = `svc_${svcId}_dept`;
  return _strings[key] || _fallback[key] || defaultDept;
}

/**
 * Translate document kind badge.
 * @param {string} kind
 * @returns {string}
 */
export function tKind(kind) {
  if (!kind) return '';
  const key = `kind_${String(kind).toLowerCase().trim()}`;
  return _strings[key] || _fallback[key] || kind;
}

/**
 * Translate applicant category.
 * @param {string} cat
 * @returns {string}
 */
export function tCategory(cat) {
  if (!cat) return '';
  const key = `cat_${String(cat).toLowerCase().trim()}`;
  return _strings[key] || _fallback[key] || cat;
}

/**
 * General text translation fallback.
 * @param {string} text
 * @returns {string}
 */
export function tText(text) {
  if (!text) return '';
  return _strings[text] || _fallback[text] || text;
}

/**
 * Subscribe to locale changes.
 * @param {Function} fn - called with the new locale code
 * @returns {Function} unsubscribe
 */
export function onLocaleChange(fn) {
  _listeners.add(fn);
  return () => _listeners.delete(fn);
}

/**
 * Re-apply translations to the DOM (useful after dynamic content is added).
 */
export function applyTranslations() {
  _applyAll();
}

// ── Internals ────────────────────────────────────────────────────────────────

async function _fetchLocale(code) {
  try {
    const resp = await fetch(`/static/lang/${code}.json?v=${Date.now()}`);
    if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
    return await resp.json();
  } catch (e) {
    console.warn(`[i18n] Failed to load locale "${code}":`, e);
    return {};
  }
}

function _applyAll() {
  const els = document.querySelectorAll('[data-i18n]');
  els.forEach(el => {
    const key = el.getAttribute('data-i18n');
    const val = _strings[key] || _fallback[key];
    if (val !== undefined && val !== null) {
      const isHtml = el.getAttribute('data-i18n-html') === 'true';
      const attr = el.getAttribute('data-i18n-attr');
      if (attr) {
        el.setAttribute(attr, val);
      } else if (isHtml) {
        el.innerHTML = val;
      } else {
        el.textContent = val;
      }
    }
  });
}

function _updateHtmlLang() {
  document.documentElement.lang = _locale;
}

function _readStorage() {
  try {
    return localStorage.getItem(STORAGE_KEY) || DEFAULT_LOCALE;
  } catch (_) {
    return DEFAULT_LOCALE;
  }
}

function _writeStorage(locale) {
  try {
    localStorage.setItem(STORAGE_KEY, locale);
  } catch (_) {
    // Silently ignore
  }
}

function _notifyListeners() {
  for (const fn of _listeners) {
    try { fn(_locale); } catch (err) { console.error('[i18n listener error]', err); }
  }
}
