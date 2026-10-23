/**
 * state-selector.js — State/jurisdiction selector logic.
 *
 * Persists selected state in localStorage. Dispatches a custom event
 * 'statechange' on document when the state changes.
 */
import { getLocale, onLocaleChange, t } from './i18n.js';

const STORAGE_KEY = 'documentready:state';
const ALL_STATES_ID = '';

let _states = [];
let _selectedStateId = ALL_STATES_ID;

/**
 * Initialise the state selector. Loads states data and renders the dropdown.
 */
export async function initStateSelector() {
  _states = await _fetchStates();
  _selectedStateId = _readStorage();
  _renderDropdown();

  // Re-render labels when locale changes
  onLocaleChange(() => _renderDropdown());
}

/**
 * Get the currently selected state ID (empty string means "All India").
 * @returns {string}
 */
export function getSelectedState() {
  return _selectedStateId;
}

/**
 * Get the state name for the currently selected state.
 * @returns {string}
 */
export function getSelectedStateName() {
  if (!_selectedStateId) return '';
  const locale = getLocale();
  const state = _states.find(s => s.id === _selectedStateId);
  if (!state) return _selectedStateId;
  if (locale === 'hi' && state.name_hi) return state.name_hi;
  if (locale === 'mr' && state.name_mr) return state.name_mr;
  return state.name;
}

/**
 * Set the state and fire the change event.
 * @param {string} stateId
 */
export function setSelectedState(stateId) {
  _selectedStateId = stateId;
  _writeStorage(stateId);
  _updateDropdownUI();
  document.dispatchEvent(new CustomEvent('statechange', { detail: { stateId } }));
}

// ── Internals ────────────────────────────────────────────────────────────────

async function _fetchStates() {
  try {
    const resp = await fetch('/api/states');
    if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
    return await resp.json();
  } catch (e) {
    console.warn('[state-selector] Failed to load states:', e);
    return [];
  }
}

function _renderDropdown() {
  const containerIds = ['state-selector', 'home-state-select-wrap', 'service-page-state-selector'];
  const containers = containerIds.map(id => document.getElementById(id)).filter(Boolean);
  if (containers.length === 0) return;

  const locale = getLocale();

  containers.forEach(container => {
    container.innerHTML = '';

    const wrapper = document.createElement('div');
    wrapper.className = 'state-selector';

    const icon = document.createElement('span');
    icon.className = 'state-selector__icon';
    icon.setAttribute('aria-hidden', 'true');
    icon.textContent = '📍';
    wrapper.appendChild(icon);

    const select = document.createElement('select');
    select.className = 'state-selector__select';
    select.setAttribute('aria-label', t('select_state'));

    // "All India" option
    const allOpt = document.createElement('option');
    allOpt.value = '';
    allOpt.textContent = t('all_states');
    select.appendChild(allOpt);

    // State options
    _states.forEach(s => {
      const opt = document.createElement('option');
      opt.value = s.id;
      if (locale === 'hi' && s.name_hi) opt.textContent = `${s.name_hi} (${s.name})`;
      else if (locale === 'mr' && s.name_mr) opt.textContent = `${s.name_mr} (${s.name})`;
      else opt.textContent = s.name;
      if (s.id === _selectedStateId) opt.selected = true;
      select.appendChild(opt);
    });

    select.value = _selectedStateId;
    select.addEventListener('change', (e) => {
      setSelectedState(e.target.value);
    });

    wrapper.appendChild(select);
    container.appendChild(wrapper);
  });
}

function _updateDropdownUI() {
  const selects = document.querySelectorAll('.state-selector__select');
  selects.forEach(select => {
    select.value = _selectedStateId;
  });
}

function _readStorage() {
  try {
    return localStorage.getItem(STORAGE_KEY) || ALL_STATES_ID;
  } catch (_) {
    return ALL_STATES_ID;
  }
}

function _writeStorage(stateId) {
  try {
    localStorage.setItem(STORAGE_KEY, stateId);
  } catch (_) {}
}
