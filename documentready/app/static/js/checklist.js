/**
 * checklist.js — Render checklist, handle toggle, progress, and any_of groups.
 * Runs on the service page.
 */
import { apiGet } from './api.js';
import { getState, setStatus, setCategory, subscribe, initStore, resetStatuses } from './store.js';
import { showToast, announce } from './ui.js';
import { t, onLocaleChange, tDoc, tDocNote, tKind, tCategory, tSvc } from './i18n.js';
import { getSelectedState, getSelectedStateName } from './state-selector.js';

const serviceId = window.__SERVICE_ID__;
const categories = window.__SERVICE_CATEGORIES__ || [];

if (!serviceId) {
  console.error('No service ID found.');
} else {
  initChecklist();
  document.addEventListener('statechange', async () => {
    await loadChecklist();
  });
  onLocaleChange(() => {
    renderCategorySelector();
    if (_serviceData?.application_info) renderAppInfo(_serviceData.application_info);
    _updateStateInfoBanner();
    if (_resolvedItems.length) renderChecklist(_resolvedItems, getState());
  });
}

// Module-level resolved items (set after loading)
let _resolvedItems = [];
let _serviceData = null;

async function initChecklist() {
  const savedState = (() => {
    // Peek at stored category before initStore resets
    try {
      const raw = localStorage.getItem(`documentready:v1:${serviceId}`);
      return raw ? JSON.parse(raw) : null;
    } catch (_) { return null; }
  })();

  initStore(serviceId, savedState?.category || null);

  // Render category selector
  renderCategorySelector();

  // Load checklist
  await loadChecklist();

  // Subscribe to state changes for live progress
  subscribe(state => {
    updateProgress(state);
    clearReadinessBanner();
  });

  // Reset button
  const resetBtn = document.getElementById('reset-btn');
  if (resetBtn) {
    resetBtn.addEventListener('click', () => {
      resetStatuses();
      showToast(t('toast_reset'), 'info');
      announce(t('toast_reset'));
      renderChecklist(_resolvedItems, getState());
    });
  }
}

// ── Category selector ────────────────────────────────────────────────────────

function renderCategorySelector() {
  const section = document.getElementById('category-section');
  const selectorEl = document.getElementById('category-selector');
  if (!selectorEl || !categories.length) return;

  section.style.display = 'block';
  selectorEl.innerHTML = '';

  const state = getState();

  // "Any" button
  const anyBtn = document.createElement('button');
  anyBtn.className = `category-btn ${!state.category ? 'category-btn--active' : ''}`;
  anyBtn.textContent = t('category_any');
  anyBtn.id = 'cat-btn-any';
  anyBtn.addEventListener('click', () => selectCategory(null));
  selectorEl.appendChild(anyBtn);

  categories.forEach(cat => {
    const btn = document.createElement('button');
    btn.className = `category-btn ${state.category === cat ? 'category-btn--active' : ''}`;
    btn.textContent = tCategory(cat);
    btn.id = `cat-btn-${cat}`;
    btn.setAttribute('aria-pressed', state.category === cat ? 'true' : 'false');
    btn.addEventListener('click', () => selectCategory(cat));
    selectorEl.appendChild(btn);
  });
}

async function selectCategory(cat) {
  setCategory(cat);
  renderCategorySelector();
  await loadChecklist();
}

// ── Load checklist from API ──────────────────────────────────────────────────

async function loadChecklist() {
  const checklistEl = document.getElementById('checklist');
  const appInfoPanel = document.getElementById('app-info-panel');

  checklistEl.innerHTML = `
    <div class="skeleton skeleton-line" style="height:80px;"></div>
    <div class="skeleton skeleton-line" style="height:80px;"></div>
    <div class="skeleton skeleton-line" style="height:80px;"></div>
  `;

  try {
    const state = getState();
    const selectedState = getSelectedState();
    const data = await apiGet(`/services/${serviceId}`, {
      category: state.category || '',
      state: selectedState || '',
    });
    _resolvedItems = data.items || [];
    _serviceData = data;

    renderChecklist(_resolvedItems, getState());
    renderAppInfo(data.application_info);
    updateProgress(getState());
    _updateStateInfoBanner();
  } catch (e) {
    checklistEl.innerHTML = `<div class="inline-error">⚠ ${t('search_load_error')} ${e.message}. <button class="btn btn--ghost btn--sm" onclick="location.reload()">${t('retry_btn')}</button></div>`;
  }
}

// ── Render application info ──────────────────────────────────────────────────

function renderAppInfo(info) {
  const panel = document.getElementById('app-info-panel');
  if (!panel || !info) return;
  panel.innerHTML = '';

  const fields = [
    { label: t('where_to_apply'), value: t(`svc_${serviceId}_where`) || info.where },
    { label: t('mode_label'), value: t(`svc_${serviceId}_mode`) || info.mode },
    { label: t('fee_label'), value: t(`svc_${serviceId}_fee`) || info.fee_note },
  ];

  fields.forEach(({ label, value }) => {
    if (!value) return;
    const row = document.createElement('div');
    row.style.marginBottom = 'var(--space-3)';
    const dt = document.createElement('dt');
    dt.style.cssText = 'font-size:var(--font-size-xs); color:var(--grey); text-transform:uppercase; letter-spacing:0.5px; margin-bottom:2px;';
    dt.textContent = label;
    const dd = document.createElement('dd');
    dd.style.cssText = 'font-size:var(--font-size-sm); font-weight:500;';
    dd.textContent = value;
    row.appendChild(dt);
    row.appendChild(dd);
    panel.appendChild(row);
  });

  if (info.steps?.length) {
    const stepsTitle = document.createElement('h4');
    stepsTitle.style.cssText = 'margin-top:var(--space-4); margin-bottom:var(--space-3); color:var(--navy);';
    stepsTitle.textContent = t('application_steps');
    panel.appendChild(stepsTitle);

    const stepsEl = document.createElement('div');
    stepsEl.className = 'app-steps';
    info.steps.forEach((step, i) => {
      const stepEl = document.createElement('div');
      stepEl.className = 'app-step';
      stepEl.innerHTML = `<div class="app-step__num">${i + 1}</div><div class="app-step__text"></div>`;
      stepEl.querySelector('.app-step__text').textContent = t(`svc_${serviceId}_step_${i + 1}`) || step;
      stepsEl.appendChild(stepEl);
    });
    panel.appendChild(stepsEl);
  }
}

// ── Render checklist ─────────────────────────────────────────────────────────

export function renderChecklist(items, state) {
  const checklistEl = document.getElementById('checklist');
  if (!checklistEl) return;
  checklistEl.innerHTML = '';

  if (!items || items.length === 0) {
    checklistEl.innerHTML = `<p style="color:var(--grey);">${t('no_results')}</p>`;
    return;
  }

  items.forEach(item => {
    if (item.type === 'document') {
      const el = createDocumentItem(item, state);
      checklistEl.appendChild(el);
    } else if (item.type === 'any_of') {
      const el = createAnyOfGroup(item, state);
      checklistEl.appendChild(el);
    }
  });
}

function createDocumentItem(item, state) {
  const doc = item.document;
  const docId = item.document_id;
  const status = state.statuses[docId] || 'unmarked';
  const isOptional = item.necessity === 'optional';

  const el = document.createElement('div');
  el.className = `checklist-item ${status === 'available' ? 'checklist-item--available' : status === 'missing' ? 'checklist-item--missing' : ''} ${isOptional ? 'checklist-item--optional' : ''}`;
  el.setAttribute('role', 'listitem');
  el.id = `item-${docId}`;

  const info = document.createElement('div');
  info.className = 'checklist-item__info';

  // Header row: name + badges
  const header = document.createElement('div');
  header.className = 'checklist-item__header';

  const nameEl = document.createElement('span');
  nameEl.className = 'checklist-item__name';
  nameEl.textContent = tDoc(docId, doc?.name);
  header.appendChild(nameEl);

  if (isOptional) {
    const optBadge = document.createElement('span');
    optBadge.className = 'badge badge--optional';
    optBadge.textContent = t('optional_badge');
    header.appendChild(optBadge);
  }

  if (doc && !doc.verified) {
    const uvBadge = document.createElement('span');
    uvBadge.className = 'badge badge--unverified';
    uvBadge.textContent = t('pending_review') || 'Pending Review';
    header.appendChild(uvBadge);
  }

  if (doc?.kind) {
    const kindBadge = document.createElement('span');
    kindBadge.className = 'badge badge--kind';
    kindBadge.textContent = tKind(doc.kind);
    header.appendChild(kindBadge);
  }

  if (item.is_state_specific) {
    const stateBadge = document.createElement('span');
    stateBadge.className = 'badge';
    stateBadge.style.cssText = 'background:var(--navy); color:#fff; font-size:11px; font-weight:600; padding:2px 8px; border-radius:12px;';
    stateBadge.textContent = `📍 ${item.state_name || getSelectedStateName() || 'State'} ${t('state_requirement_badge') || 'Requirement'}`;
    header.appendChild(stateBadge);
  }

  info.appendChild(header);

  if (item.note) {
    const note = document.createElement('div');
    note.className = 'checklist-item__note';
    note.textContent = tDocNote(docId, item.note);
    info.appendChild(note);
  }

  // Actions column
  const actions = document.createElement('div');
  actions.className = 'checklist-item__actions';

  // 3-state toggle
  const toggle = createStatusToggle(docId, status);
  actions.appendChild(toggle);

  // "How to obtain?" button (shown when missing and has guide)
  if (doc?.has_guide) {
    const guideBtn = document.createElement('button');
    guideBtn.className = 'btn btn--ghost btn--sm';
    guideBtn.id = `guide-btn-${docId}`;
    guideBtn.setAttribute('aria-label', `${t('how_to_obtain_title')} ${tDoc(docId, doc.name)}`);
    guideBtn.textContent = t('how_to_obtain');
    guideBtn.dataset.docId = docId;
    guideBtn.dataset.docName = doc.name;
    guideBtn.addEventListener('click', () => {
      import('./guide.js').then(m => m.openGuide(docId, doc.name, [docId]));
    });
    actions.appendChild(guideBtn);
  }

  el.appendChild(info);
  el.appendChild(actions);
  return el;
}

function createStatusToggle(docId, currentStatus) {
  const toggle = document.createElement('div');
  toggle.className = 'status-toggle';
  toggle.setAttribute('role', 'group');
  toggle.setAttribute('aria-label', t('status_label'));

  const buttons = [
    { label: t('status_unmarked'), value: 'unmarked', short: '—' },
    { label: t('status_available'), value: 'available', short: t('status_available') },
    { label: t('status_missing'), value: 'missing', short: t('status_missing') },
  ];

  buttons.forEach(({ label, value, short }) => {
    const btn = document.createElement('button');
    btn.className = `status-toggle__btn`;
    btn.setAttribute('aria-label', label);
    btn.setAttribute('aria-pressed', String(currentStatus === value || (value === 'unmarked' && currentStatus === 'unmarked')));
    btn.textContent = short;
    btn.id = `toggle-${docId}-${value}`;

    if (currentStatus === value || (value === 'unmarked' && !currentStatus)) {
      if (value === 'available') btn.classList.add('status-toggle__btn--active-available');
      if (value === 'missing') btn.classList.add('status-toggle__btn--active-missing');
    }

    btn.addEventListener('click', () => {
      const newStatus = value === 'unmarked' ? null : value;
      setStatus(docId, newStatus);
      // Re-render the item
      const state = getState();
      const parentList = document.getElementById('checklist');
      const oldItem = document.getElementById(`item-${docId}`);
      if (oldItem && parentList) {
        const itemData = _resolvedItems.find(i => i.document_id === docId);
        if (itemData) {
          const newItem = createDocumentItem(itemData, state);
          parentList.replaceChild(newItem, oldItem);
          // Re-focus the same toggle button
          const newBtn = document.getElementById(`toggle-${docId}-${value}`);
          if (newBtn) newBtn.focus();
        }
      }
      announce(`${t('status_label')}: ${value === 'unmarked' ? t('status_unmarked') : value === 'available' ? t('status_available') : t('status_missing')}`);

    });

    toggle.appendChild(btn);
  });

  return toggle;
}

function createAnyOfGroup(item, state) {
  const anyAvailable = item.options.some(opt => {
    const id = opt.document_id || opt;
    return state.statuses[id] === 'available';
  });

  const group = document.createElement('div');
  group.className = `anyof-group ${anyAvailable ? 'anyof-group--satisfied' : ''}`;
  group.setAttribute('role', 'group');
  group.setAttribute('aria-label', `${t('provide_any_one')} ${item.group}`);
  group.id = `anyof-${item.group}`;

  const title = document.createElement('div');
  title.className = 'anyof-group__title';

  const icon = document.createElement('span');
  icon.setAttribute('aria-hidden', 'true');
  icon.textContent = anyAvailable ? '✓' : '○';
  title.appendChild(icon);

  const titleText = document.createElement('span');
  titleText.textContent = t('provide_any_one');
  title.appendChild(titleText);

  if (item.note) {
    const noteEl = document.createElement('span');
    noteEl.style.cssText = 'font-weight:400; color:var(--grey); font-size:var(--font-size-xs);';
    noteEl.textContent = ` — ${item.note}`;
    title.appendChild(noteEl);
  }

  group.appendChild(title);

  const optsList = document.createElement('div');
  optsList.className = 'anyof-group__options';
  optsList.setAttribute('role', 'list');

  item.options.forEach(opt => {
    const optId = opt.document_id || opt;
    const optName = opt.name || optId;
    const status = state.statuses[optId] || 'unmarked';

    const optEl = document.createElement('div');
    optEl.className = `anyof-option ${status === 'available' ? 'anyof-option--available' : ''}`;
    optEl.setAttribute('role', 'listitem');
    optEl.id = `anyof-opt-${optId}`;

    const nameEl = document.createElement('span');
    nameEl.className = 'anyof-option__name';
    nameEl.textContent = tDoc(optId, optName);

    const toggle = createStatusToggle(optId, status);
    toggle.style.transform = 'scale(0.9)';

    optEl.appendChild(nameEl);
    optEl.appendChild(toggle);
    optsList.appendChild(optEl);
  });

  group.appendChild(optsList);
  return group;
}

// ── Progress bar ─────────────────────────────────────────────────────────────

function updateProgress(state) {
  if (!_resolvedItems.length) return;

  let total = 0;
  let satisfied = 0;

  _resolvedItems.forEach(item => {
    if (item.type === 'document' && item.necessity === 'required') {
      total++;
      if (state.statuses[item.document_id] === 'available') satisfied++;
    } else if (item.type === 'any_of') {
      total++;
      const hasAny = item.options.some(opt => {
        const id = opt.document_id || opt;
        return state.statuses[id] === 'available';
      });
      if (hasAny) satisfied++;
    }
  });

  const percent = total > 0 ? Math.round(100 * satisfied / total) : 0;

  const fill = document.getElementById('progress-fill');
  const text = document.getElementById('progress-text');
  const bar = fill?.closest('[role="progressbar"]');

  if (fill) fill.style.width = `${percent}%`;
  if (text) text.textContent = `${satisfied} / ${total}`;
  if (bar) {
    bar.setAttribute('aria-valuenow', percent);
    bar.setAttribute('aria-valuetext', `${satisfied} of ${total} required documents ready`);
  }
}

function clearReadinessBanner() {
  const banner = document.getElementById('readiness-banner');
  if (banner && !banner.hidden) {
    banner.hidden = true;
    banner.innerHTML = '';
  }
}

// ── State info banner & rules panel ──────────────────────────────────────────

function _updateStateInfoBanner() {
  const detailsEl = document.getElementById('state-rule-details');
  const banner = document.getElementById('state-info-banner');
  const nameEl = document.getElementById('state-info-name');
  const stateId = getSelectedState();
  const stateName = getSelectedStateName();
  const stateRule = _serviceData?.state_rule;

  if (banner && nameEl) {
    if (stateId && stateName) {
      nameEl.textContent = stateName;
      banner.hidden = false;
    } else {
      banner.hidden = true;
    }
  }

  if (!detailsEl) return;

  if (stateRule) {
    detailsEl.hidden = false;
    detailsEl.innerHTML = `
      <div style="display:flex; flex-direction:column; gap:var(--space-3);">
        <div style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:var(--space-2);">
          <div>
            <span style="font-size:var(--font-size-xs); color:var(--grey); text-transform:uppercase; font-weight:600; letter-spacing:0.5px;">${_esc(t('competent_authority') || 'Competent Authority')}:</span>
            <div style="font-size:var(--font-size-sm); font-weight:600; color:var(--navy); margin-top:2px;">${_esc(stateRule.authority || '')}</div>
          </div>
          ${stateRule.portal_name ? `
            <div style="text-align:right;">
              <span style="font-size:var(--font-size-xs); color:var(--grey); text-transform:uppercase; font-weight:600; letter-spacing:0.5px;">${_esc(t('official_portal') || 'Official Portal')}:</span>
              <div style="margin-top:2px;">
                ${stateRule.portal_url ? `<a href="${stateRule.portal_url}" target="_blank" rel="noopener noreferrer" class="btn btn--outline btn--sm" style="display:inline-flex; align-items:center; gap:4px; font-weight:600; font-size:var(--font-size-xs);">${_esc(stateRule.portal_name)} ↗</a>` : `<span class="badge" style="background:var(--grey-light); color:var(--navy);">${_esc(stateRule.portal_name)}</span>`}
              </div>
            </div>
          ` : ''}
        </div>
        ${stateRule.statutory_rule ? `
          <div style="background:rgba(26,54,93,0.06); border-left:3px solid var(--navy); padding:var(--space-3); border-radius:4px; font-size:var(--font-size-sm); line-height:1.5;">
            <strong style="color:var(--navy);">${_esc(t('state_statutory_rule') || 'State Rule & Statutory Cutoff')}:</strong> ${_esc(stateRule.statutory_rule)}
          </div>
        ` : ''}
        <div style="font-size:var(--font-size-xs); color:var(--grey);">
          ✓ ${_esc(stateRule.state_name || stateId)} ${t('state_incorporated_note')}
        </div>
      </div>
    `;
  } else {
    detailsEl.hidden = false;
    detailsEl.innerHTML = `
      <div style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:var(--space-2); font-size:var(--font-size-sm); color:var(--grey);">
        <span>${t('baseline_rule_note')}</span>
      </div>
    `;
  }
}

function _esc(str) {
  if (!str) return '';
  const d = document.createElement('div');
  d.textContent = str;
  return d.innerHTML;
}
