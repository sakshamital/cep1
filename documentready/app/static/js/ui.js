/**
 * ui.js — Toast notifications, focus management, aria-live announcer, escape helpers.
 */

// ── Aria-live announcer ────────────────────────────────────────────────────

const _liveRegion = document.getElementById('aria-live');

/**
 * Announce a message to screen readers.
 * @param {string} message
 */
export function announce(message) {
  if (!_liveRegion) return;
  _liveRegion.textContent = '';
  // Force re-announce even if same message
  requestAnimationFrame(() => {
    _liveRegion.textContent = message;
  });
}

// ── Toast ──────────────────────────────────────────────────────────────────

const _toastContainer = document.getElementById('toast-container');

/**
 * Show a toast notification.
 * @param {string} message
 * @param {"info"|"success"|"error"|"warning"} type
 * @param {number} durationMs
 */
export function showToast(message, type = 'info', durationMs = 3000) {
  if (!_toastContainer) return;

  const toast = document.createElement('div');
  toast.className = `toast toast--${type}`;
  toast.setAttribute('role', 'status');

  // Icon
  const icon = document.createElement('span');
  icon.setAttribute('aria-hidden', 'true');
  icon.textContent = type === 'success' ? '✓' : type === 'error' ? '✗' : type === 'warning' ? '⚠' : 'ℹ';
  toast.appendChild(icon);

  const text = document.createElement('span');
  text.textContent = message;
  toast.appendChild(text);

  _toastContainer.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateX(20px)';
    toast.style.transition = 'opacity 300ms, transform 300ms';
    setTimeout(() => toast.remove(), 320);
  }, durationMs);
}

// ── Focus trap ─────────────────────────────────────────────────────────────

/**
 * Trap focus within a container element.
 * @param {HTMLElement} container
 * @returns {Function} cleanup function
 */
export function trapFocus(container) {
  const focusableSelectors = [
    'a[href]', 'button:not([disabled])', 'input:not([disabled])',
    'select:not([disabled])', 'textarea:not([disabled])',
    '[tabindex]:not([tabindex="-1"])',
  ].join(', ');

  function getFocusable() {
    return Array.from(container.querySelectorAll(focusableSelectors));
  }

  function handleKeyDown(e) {
    if (e.key !== 'Tab') return;
    const focusable = getFocusable();
    if (focusable.length === 0) return;
    const first = focusable[0];
    const last = focusable[focusable.length - 1];

    if (e.shiftKey) {
      if (document.activeElement === first) {
        e.preventDefault();
        last.focus();
      }
    } else {
      if (document.activeElement === last) {
        e.preventDefault();
        first.focus();
      }
    }
  }

  container.addEventListener('keydown', handleKeyDown);

  // Auto-focus first focusable
  const first = getFocusable()[0];
  if (first) first.focus();

  return () => container.removeEventListener('keydown', handleKeyDown);
}

// ── Escape key helper ──────────────────────────────────────────────────────

/**
 * Listen for Escape key and call a callback.
 * @param {Function} callback
 * @returns {Function} cleanup
 */
export function onEscape(callback) {
  function handler(e) {
    if (e.key === 'Escape') callback(e);
  }
  document.addEventListener('keydown', handler);
  return () => document.removeEventListener('keydown', handler);
}

// ── Escape HTML (safety helper) ────────────────────────────────────────────

/**
 * Escape special HTML characters. Use textContent where possible instead.
 * @param {string} str
 * @returns {string}
 */
export function escHtml(str) {
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

// ── Scroll to element ──────────────────────────────────────────────────────

/**
 * Smoothly scroll an element into view and focus it.
 * @param {HTMLElement|string} target - element or CSS selector
 */
export function scrollAndFocus(target) {
  const el = typeof target === 'string' ? document.querySelector(target) : target;
  if (!el) return;
  el.scrollIntoView({ behavior: 'smooth', block: 'center' });
  if (el.tabIndex < 0) el.tabIndex = -1;
  el.focus({ preventScroll: true });
}
