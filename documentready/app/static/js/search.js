/**
 * search.js — Search box with debounce, AbortController, keyboard navigation.
 * Runs on the home page.
 */
import { apiGet, ApiError } from './api.js';
import { showToast } from './ui.js';
import { t, onLocaleChange, tSvc, tSvcDesc, tDoc, tKind } from './i18n.js';
import { getSelectedState, getSelectedStateName } from './state-selector.js';

const searchInput = document.getElementById('search-input');
const suggestionsEl = document.getElementById('search-suggestions');
const servicesGrid = document.getElementById('services-grid');
const popularChips = document.getElementById('popular-chips');

if (searchInput) {
  initSearch();
}

if (servicesGrid) {
  loadServicesGrid();
  onLocaleChange(() => loadServicesGrid());
  document.addEventListener('statechange', () => loadServicesGrid());
}

// ── Load services grid ──────────────────────────────────────────────────────

async function loadServicesGrid() {
  try {
    const selectedState = getSelectedState();
    const services = await apiGet('/services', { state: selectedState || '' });
    if (!Array.isArray(services)) return;

    // Populate popular chips
    if (popularChips) {
      popularChips.innerHTML = '';
      services.slice(0, 6).forEach(svc => {
        const chip = document.createElement('a');
        chip.className = 'popular-chip';
        chip.href = `/service/${svc.id}`;
        chip.textContent = tSvc(svc.id, svc.name);
        popularChips.appendChild(chip);
      });
    }

    // Populate grid
    servicesGrid.innerHTML = '';
    services.forEach(svc => {
      const card = createServiceCard(svc);
      servicesGrid.appendChild(card);
    });
  } catch (e) {
    servicesGrid.innerHTML = `<div class="inline-error">⚠ ${t('search_load_error')}</div>`;
  }
}

function createServiceCard(svc) {
  const card = document.createElement('a');
  card.href = `/service/${svc.id}`;
  card.className = 'card card--elevated';
  card.style.cssText = 'display:block; text-decoration:none; transition:box-shadow 180ms, transform 180ms; cursor:pointer;';
  card.setAttribute('aria-label', `${t('view_req_for')} ${tSvc(svc.id, svc.name)}`);

  card.addEventListener('mouseenter', () => {
    card.style.boxShadow = 'var(--shadow-lg)';
    card.style.transform = 'translateY(-2px)';
  });
  card.addEventListener('mouseleave', () => {
    card.style.boxShadow = '';
    card.style.transform = '';
  });

  const badge = !svc.verified
    ? `<span class="badge badge--unverified">${t('unverified_badge')}</span>`
    : `<span class="badge badge--verified" style="background:#2E8B57; color:#fff; font-weight:600;">${t('verified_badge')}</span>`;

  const stateName = getSelectedStateName();
  const stateBadge = stateName
    ? `<span class="badge" style="background:rgba(26,54,93,0.08); color:var(--navy); font-size:11px;">📍 ${esc(stateName)}</span>`
    : `<span class="badge" style="background:rgba(0,0,0,0.05); color:var(--grey); font-size:11px;">📍 ${t('all_states')}</span>`;

  const typeEl = document.createElement('div');
  typeEl.style.cssText = 'display:flex; align-items:center; justify-content:space-between; margin-bottom:var(--space-3); flex-wrap:wrap; gap:4px;';
  typeEl.innerHTML = `<div style="display:flex; align-items:center; gap:4px;"><span class="badge badge--kind">${esc(tKind(svc.type))}</span>${stateBadge}</div>${badge}`;

  const title = document.createElement('h3');
  title.style.cssText = 'color:var(--navy); margin-bottom:var(--space-2); font-size:var(--font-size-base);';
  title.textContent = tSvc(svc.id, svc.name);

  const desc = document.createElement('p');
  desc.style.cssText = 'font-size:var(--font-size-sm); color:var(--grey); margin:0; line-height:1.4;';
  const fullDesc = tSvcDesc(svc.id, svc.description);
  desc.textContent = fullDesc ? fullDesc.slice(0, 100) + '…' : '';

  const arrow = document.createElement('div');
  arrow.style.cssText = 'margin-top:var(--space-3); color:var(--teal); font-size:var(--font-size-sm); font-weight:600;';
  arrow.textContent = t('check_requirements');

  card.appendChild(typeEl);
  card.appendChild(title);
  card.appendChild(desc);
  card.appendChild(arrow);
  return card;
}

// ── Search box ──────────────────────────────────────────────────────────────

function initSearch() {
  let debounceTimer = null;
  let currentController = null;
  let selectedIndex = -1;
  let currentHits = [];

  searchInput.addEventListener('input', () => {
    const q = searchInput.value.trim();
    clearTimeout(debounceTimer);
    closeSuggestions();

    if (q.length < 2) return;

    debounceTimer = setTimeout(() => performSearch(q), 250);
  });

  searchInput.addEventListener('keydown', (e) => {
    const items = suggestionsEl ? Array.from(suggestionsEl.querySelectorAll('.suggestion-item')) : [];
    if (!items.length) return;

    if (e.key === 'ArrowDown') {
      e.preventDefault();
      selectedIndex = Math.min(selectedIndex + 1, items.length - 1);
      updateSelection(items);
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      selectedIndex = Math.max(selectedIndex - 1, -1);
      updateSelection(items);
    } else if (e.key === 'Enter') {
      e.preventDefault();
      if (selectedIndex >= 0 && items[selectedIndex]) {
        items[selectedIndex].click();
      }
    } else if (e.key === 'Escape') {
      closeSuggestions();
      selectedIndex = -1;
    }
  });

  document.addEventListener('click', (e) => {
    if (!searchInput.contains(e.target) && !suggestionsEl.contains(e.target)) {
      closeSuggestions();
    }
  });

  async function performSearch(q) {
    if (currentController) currentController.abort();
    currentController = new AbortController();

    try {
      const hits = await apiGet('/search', { q, limit: 10 }, currentController.signal);
      currentHits = Array.isArray(hits) ? hits : [];
      renderSuggestions(currentHits);
    } catch (err) {
      if (err.name !== 'AbortError') {
        renderError();
      }
    }
  }

  function renderSuggestions(hits) {
    suggestionsEl.innerHTML = '';
    selectedIndex = -1;

    if (hits.length === 0) {
      const empty = document.createElement('div');
      empty.className = 'search-empty';
      empty.textContent = t('no_results');
      suggestionsEl.appendChild(empty);
      openSuggestions();
      return;
    }

    // Group by kind
    const services = hits.filter(h => h.kind === 'service');
    const documents = hits.filter(h => h.kind === 'document');

    if (services.length) {
      const group = createGroup(t('search_services_group'), services, 'service');
      suggestionsEl.appendChild(group);
    }
    if (documents.length) {
      const group = createGroup(t('search_documents_group'), documents, 'document');
      suggestionsEl.appendChild(group);
    }

    openSuggestions();
  }

  function createGroup(title, hits, kind) {
    const frag = document.createDocumentFragment();

    const groupTitle = document.createElement('div');
    groupTitle.className = 'suggestion-group__title';
    groupTitle.textContent = title;
    frag.appendChild(groupTitle);

    hits.forEach(hit => {
      const item = document.createElement('div');
      item.className = 'suggestion-item';
      item.setAttribute('role', 'option');
      item.setAttribute('aria-selected', 'false');
      item.setAttribute('tabindex', '-1');

      // Icon
      const iconEl = document.createElement('div');
      iconEl.style.cssText = 'width:32px; height:32px; background:var(--tint); border-radius:var(--radius-sm); display:flex; align-items:center; justify-content:center; flex-shrink:0; color:var(--navy);';
      iconEl.setAttribute('aria-hidden', 'true');
      iconEl.textContent = kind === 'service' ? '📋' : '📄';

      const info = document.createElement('div');
      info.style.cssText = 'flex:1; min-width:0;';

      const nameEl = document.createElement('div');
      nameEl.className = 'suggestion-item__name';
      nameEl.textContent = kind === 'service' ? tSvc(hit.id, hit.name) : tDoc(hit.id, hit.name);

      const metaEl = document.createElement('div');
      metaEl.className = 'suggestion-item__meta';

      if (kind === 'document' && hit.used_by_services?.length) {
        metaEl.textContent = `${t('search_required_for')} ${hit.used_by_services.map(s => tSvc(s.id, s.name)).join(', ')}`;
      } else if (hit.type) {
        metaEl.textContent = tKind(hit.type);
      }

      info.appendChild(nameEl);
      if (metaEl.textContent) info.appendChild(metaEl);

      item.appendChild(iconEl);
      item.appendChild(info);

      item.addEventListener('click', () => {
        if (kind === 'service') {
          window.location.href = `/service/${hit.id}`;
        } else {
          window.location.href = `/guide/${hit.id}`;
        }
      });

      frag.appendChild(item);
    });

    const wrapper = document.createElement('div');
    wrapper.appendChild(frag);
    return wrapper;
  }

  function renderError() {
    suggestionsEl.innerHTML = `<div class="inline-error search-empty">${t('search_failed')}</div>`;
    openSuggestions();
  }

  function openSuggestions() {
    suggestionsEl.hidden = false;
    searchInput.setAttribute('aria-expanded', 'true');
  }

  function closeSuggestions() {
    suggestionsEl.hidden = true;
    searchInput.setAttribute('aria-expanded', 'false');
  }

  function updateSelection(items) {
    items.forEach((el, i) => {
      el.setAttribute('aria-selected', i === selectedIndex ? 'true' : 'false');
      if (i === selectedIndex) {
        el.scrollIntoView({ block: 'nearest' });
      }
    });
  }
}

function esc(str) {
  const d = document.createElement('span');
  d.textContent = str;
  return d.innerHTML;
}
