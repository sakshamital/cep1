/**
 * readiness.js — Verify button, readiness result rendering, obtain plan display.
 * All UI strings go through t() for full internationalisation.
 */
import { apiPost } from './api.js';
import { getState } from './store.js';
import { announce, showToast, scrollAndFocus } from './ui.js';
import { openGuide } from './guide.js';
import { t, tDoc, onLocaleChange } from './i18n.js';

const verifyBtn = document.getElementById('verify-btn');
const serviceId = window.__SERVICE_ID__;

if (verifyBtn && serviceId) {
  verifyBtn.addEventListener('click', handleVerify);
}

// Re-render last result on locale change
let _lastResult = null;
onLocaleChange(() => {
  if (_lastResult) renderReadinessResult(_lastResult);
});

async function handleVerify() {
  const state = getState();
  verifyBtn.disabled = true;
  verifyBtn.textContent = t('checking_status');

  try {
    const result = await apiPost(`/services/${serviceId}/readiness`, {
      statuses: state.statuses,
      applicant_category: state.category || null,
    });

    _lastResult = result;
    renderReadinessResult(result);

    if (result.ready) {
      announce(t('ready_to_apply'));
      showToast(t('ready_to_apply'), 'success', 4000);
    } else {
      announce(result.message);
    }
  } catch (e) {
    showToast(`${t('search_failed')}: ${e.message}`, 'error');
  } finally {
    verifyBtn.disabled = false;
    verifyBtn.textContent = `✓ ${t('verify_btn')}`;
  }
}

function renderReadinessResult(result) {
  const banner = document.getElementById('readiness-banner');
  if (!banner) return;

  banner.innerHTML = '';
  banner.hidden = false;

  if (result.ready) {
    renderReadyBanner(banner, result);
  } else {
    renderNotReadyBanner(banner, result);
  }

  // Scroll to banner
  banner.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

function renderReadyBanner(banner, result) {
  banner.className = 'readiness-banner readiness-banner--ready';

  const title = document.createElement('div');
  title.className = 'readiness-banner__title';

  const icon = document.createElement('span');
  icon.setAttribute('aria-hidden', 'true');
  icon.textContent = '✓';
  icon.style.cssText = 'background:var(--green); color:white; border-radius:50%; width:36px; height:36px; display:flex; align-items:center; justify-content:center; font-size:18px; flex-shrink:0;';

  const msg = document.createElement('span');
  msg.textContent = result.message || t('ready_to_apply_msg');

  title.appendChild(icon);
  title.appendChild(msg);
  banner.appendChild(title);

  // Application info steps from the service data
  const appInfoPanel = document.getElementById('app-info-panel');
  if (appInfoPanel) {
    const note = document.createElement('p');
    note.style.fontSize = 'var(--font-size-sm)';
    note.textContent = t('review_how_to_apply');
    banner.appendChild(note);
  }

  // Disclaimer reminder
  const disc = document.createElement('div');
  disc.className = 'unverified-notice';
  disc.style.cssText = 'margin-top:var(--space-4); background:rgba(200,112,26,0.08);';
  disc.innerHTML = `<svg aria-hidden="true" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>`;
  const discText = document.createElement('span');
  discText.textContent = t('disclaimer_reminder');
  discText.style.fontSize = 'var(--font-size-xs)';
  disc.appendChild(discText);
  banner.appendChild(disc);
}

function renderNotReadyBanner(banner, result) {
  banner.className = 'readiness-banner readiness-banner--not-ready';

  const title = document.createElement('div');
  title.className = 'readiness-banner__title';

  const icon = document.createElement('span');
  icon.setAttribute('aria-hidden', 'true');
  icon.textContent = '!';
  icon.style.cssText = 'background:var(--amber); color:white; border-radius:50%; width:36px; height:36px; display:flex; align-items:center; justify-content:center; font-size:18px; font-weight:700; flex-shrink:0;';

  const msg = document.createElement('span');
  msg.textContent = result.message;

  title.appendChild(icon);
  title.appendChild(msg);
  banner.appendChild(title);

  // Blockers
  if (result.blockers?.length) {
    const blockersTitle = document.createElement('h3');
    blockersTitle.style.cssText = 'font-size:var(--font-size-sm); text-transform:uppercase; letter-spacing:0.5px; color:var(--amber); margin-bottom:var(--space-3);';
    blockersTitle.textContent = t('docs_blocking_title');
    banner.appendChild(blockersTitle);

    const blockerList = document.createElement('div');
    blockerList.className = 'blocker-list';

    result.blockers.forEach(blocker => {
      const el = document.createElement('div');
      el.className = 'blocker-item';

      const name = document.createElement('div');
      name.className = 'blocker-item__name';
      const warnIcon = document.createElement('span');
      warnIcon.setAttribute('aria-hidden', 'true');
      warnIcon.textContent = '✗';
      warnIcon.style.color = 'var(--amber)';
      name.appendChild(warnIcon);
      const nameText = document.createElement('span');
      nameText.textContent = tDoc(blocker.document_id, blocker.name);
      name.appendChild(nameText);
      el.appendChild(name);

      // Obtain first chain
      if (blocker.obtain_first?.length) {
        const chainLabel = document.createElement('div');
        chainLabel.style.cssText = 'font-size:var(--font-size-xs); color:var(--grey); margin-bottom:var(--space-2);';
        chainLabel.textContent = t('get_these_first');
        el.appendChild(chainLabel);

        const chain = document.createElement('div');
        chain.className = 'obtain-chain';

        blocker.obtain_first.forEach((dep, i) => {
          const chip = document.createElement('span');
          chip.className = 'obtain-chip';
          chip.textContent = tDoc(dep.document_id, dep.name);
          chain.appendChild(chip);
          if (i < blocker.obtain_first.length - 1) {
            const arrow = document.createElement('span');
            arrow.className = 'obtain-arrow';
            arrow.setAttribute('aria-hidden', 'true');
            arrow.textContent = '→';
            chain.appendChild(arrow);
          }
        });

        el.appendChild(chain);
      }

      // How to obtain button
      if (blocker.document_id) {
        const guideBtn = document.createElement('button');
        guideBtn.className = 'btn btn--outline btn--sm';
        guideBtn.style.marginTop = 'var(--space-3)';
        guideBtn.textContent = t('how_to_obtain');
        guideBtn.addEventListener('click', () => {
          openGuide(blocker.document_id, tDoc(blocker.document_id, blocker.name), [blocker.document_id], guideBtn);
        });
        el.appendChild(guideBtn);
      }

      blockerList.appendChild(el);
    });

    banner.appendChild(blockerList);
  }

  // Unverified items
  if (result.unverified?.length) {
    const uvTitle = document.createElement('h3');
    uvTitle.style.cssText = 'font-size:var(--font-size-sm); text-transform:uppercase; letter-spacing:0.5px; color:var(--grey); margin-top:var(--space-5); margin-bottom:var(--space-3);';
    uvTitle.textContent = t('not_yet_checked');
    banner.appendChild(uvTitle);

    const uvList = document.createElement('div');
    uvList.style.cssText = 'display:flex; flex-direction:column; gap:var(--space-2);';

    result.unverified.forEach(item => {
      const row = document.createElement('div');
      row.style.cssText = 'display:flex; align-items:center; gap:var(--space-3); padding:var(--space-2) var(--space-3); background:var(--white); border-radius:var(--radius-sm); border:1px solid var(--line);';

      const indicator = document.createElement('span');
      indicator.textContent = '○';
      indicator.style.color = 'var(--grey-light)';
      indicator.setAttribute('aria-hidden', 'true');

      const nameEl = document.createElement('span');
      nameEl.style.cssText = 'font-size:var(--font-size-sm); flex:1;';
      nameEl.textContent = tDoc(item.document_id, item.name);

      const markBtn = document.createElement('button');
      markBtn.className = 'btn btn--ghost btn--sm';
      markBtn.textContent = t('mark_now');
      if (item.document_id) {
        markBtn.addEventListener('click', () => {
          const target = document.getElementById(`item-${item.document_id}`);
          if (target) scrollAndFocus(target);
        });
      }

      row.appendChild(indicator);
      row.appendChild(nameEl);
      row.appendChild(markBtn);
      uvList.appendChild(row);
    });

    banner.appendChild(uvList);
  }

  // Obtain plan (ordered steps)
  if (result.obtain_plan?.length) {
    const planTitle = document.createElement('h3');
    planTitle.style.cssText = 'font-size:var(--font-size-sm); text-transform:uppercase; letter-spacing:0.5px; color:var(--navy); margin-top:var(--space-5); margin-bottom:var(--space-3);';
    planTitle.textContent = t('recommended_order');

    const planDesc = document.createElement('p');
    planDesc.style.cssText = 'font-size:var(--font-size-xs); color:var(--grey); margin-bottom:var(--space-3);';
    planDesc.textContent = t('recommended_order_desc');

    banner.appendChild(planTitle);
    banner.appendChild(planDesc);

    const planChain = document.createElement('div');
    planChain.className = 'obtain-chain';
    planChain.style.flexWrap = 'wrap';

    result.obtain_plan.forEach((docId, i) => {
      const chip = document.createElement('span');
      chip.className = 'obtain-chip';
      // Use tDoc for translation, fallback to formatted ID
      chip.textContent = tDoc(docId, docId.replace(/_/g, ' '));
      chip.style.cursor = 'default';
      planChain.appendChild(chip);

      if (i < result.obtain_plan.length - 1) {
        const arrow = document.createElement('span');
        arrow.className = 'obtain-arrow';
        arrow.setAttribute('aria-hidden', 'true');
        arrow.textContent = '→';
        planChain.appendChild(arrow);
      }
    });

    banner.appendChild(planChain);
  }

  // Ignored IDs warning
  if (result.ignored_ids?.length) {
    const warn = document.createElement('p');
    warn.style.cssText = 'font-size:var(--font-size-xs); color:var(--grey); margin-top:var(--space-4);';
    warn.textContent = `${t('pending_review')}: ${result.ignored_ids.join(', ')}`;
    banner.appendChild(warn);
  }
}
