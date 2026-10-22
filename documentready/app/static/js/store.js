/**
 * store.js — Checklist state store with localStorage persistence and subscription.
 */

const STORAGE_PREFIX = 'documentready:v1:';

let _state = {
  serviceId: null,
  category: null,
  statuses: {}, // { document_id: "available" | "missing" }
};

const _listeners = new Set();

/**
 * Initialise the store for a service. Loads persisted state if available.
 * @param {string} serviceId
 * @param {string|null} category
 */
export function initStore(serviceId, category = null) {
  _state = {
    serviceId,
    category,
    statuses: {},
  };

  // Try to load persisted statuses
  try {
    const key = STORAGE_PREFIX + serviceId;
    const raw = localStorage.getItem(key);
    if (raw) {
      const parsed = JSON.parse(raw);
      if (parsed && typeof parsed === 'object') {
        _state.statuses = parsed.statuses || {};
        if (!category && parsed.category) {
          _state.category = parsed.category;
        }
      }
    }
  } catch (_) {
    // localStorage unavailable — silently fall back to memory
  }

  _notify();
}

/**
 * Get the current state (immutable snapshot).
 */
export function getState() {
  return {
    serviceId: _state.serviceId,
    category: _state.category,
    statuses: { ..._state.statuses },
  };
}

/**
 * Set the status for a document.
 * @param {string} docId
 * @param {"available"|"missing"|null} status - null to clear
 */
export function setStatus(docId, status) {
  if (status === null || status === undefined) {
    delete _state.statuses[docId];
  } else {
    _state.statuses[docId] = status;
  }
  _persist();
  _notify();
}

/**
 * Set the applicant category.
 * @param {string|null} category
 */
export function setCategory(category) {
  _state.category = category;
  _persist();
  _notify();
}

/**
 * Get the status of a single document.
 * @param {string} docId
 * @returns {"available"|"missing"|"unmarked"}
 */
export function getStatus(docId) {
  return _state.statuses[docId] || 'unmarked';
}

/**
 * Reset all statuses (but keep serviceId and category).
 */
export function resetStatuses() {
  _state.statuses = {};
  _persist();
  _notify();
}

/**
 * Subscribe to state changes.
 * @param {Function} listener - called with the new state snapshot
 * @returns {Function} unsubscribe function
 */
export function subscribe(listener) {
  _listeners.add(listener);
  return () => _listeners.delete(listener);
}

function _persist() {
  try {
    const key = STORAGE_PREFIX + _state.serviceId;
    localStorage.setItem(key, JSON.stringify({
      statuses: _state.statuses,
      category: _state.category,
    }));
  } catch (_) {
    // Silently ignore storage errors
  }
}

function _notify() {
  const snapshot = getState();
  for (const listener of _listeners) {
    try {
      listener(snapshot);
    } catch (e) {
      console.error('Store listener error:', e);
    }
  }
}
