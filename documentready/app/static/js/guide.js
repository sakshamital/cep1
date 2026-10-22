/**
 * guide.js — Guide modal with navigation stack, breadcrumb, focus trap, Esc to close.
 */
import { apiGet } from './api.js';
import { getStatus, setStatus } from './store.js';
import { trapFocus, onEscape, announce, showToast } from './ui.js';

const backdrop = document.getElementById('guide-modal-backdrop');
const modal = document.getElementById('guide-modal');

// Navigation stack: array of { docId, docName }
let _stack = [];
let _currentDocId = null;
let _releaseFocusTrap = null;
let _releaseEscape = null;
let _triggerButton = null; // The button that opened the modal

/**
 * Open the guide modal for a document.
 * @param {string} docId
 * @param {string} docName
 * @param {string[]} stackPath - breadcrumb history
 * @param {HTMLElement|null} trigger
 */
export async function openGuide(docId, docName, stackPath = [], trigger = null) {
  if (!backdrop || !modal) return;

  if (trigger) _triggerButton = trigger;
  _stack = stackPath.map((id, i) => ({ docId: id, docName: id })); // will be filled after load

  await _loadGuide(docId, docName);
}

async function _loadGuide(docId, docName) {
  _currentDocId = docId;

  // Show backdrop
  backdrop.hidden = false;
  backdrop.setAttribute('aria-label', `How to obtain: ${docName}`);

  // Show loading state
  modal.innerHTML = `
    <div class="modal__header">
      <h2 class="modal__title" id="guide-modal-title">Loading…</h2>
      <button class="modal__close" aria-label="Close guide" id="modal-close-btn">✕</button>
    </div>
    <div class="modal__body">
      <div class="skeleton skeleton-line" style="height:60px;"></div>
      <div class="skeleton skeleton-line"></div>
      <div class="skeleton skeleton-line" style="width:80%;"></div>
    </div>
  `;

  document.getElementById('modal-close-btn')?.addEventListener('click', closeModal);

  // Set up focus trap
  if (_releaseFocusTrap) _releaseFocusTrap();
  _releaseFocusTrap = trapFocus(modal);

  // Set up escape
  if (_releaseEscape) _releaseEscape();
  _releaseEscape = onEscape(closeModal);

  try {
    const data = await apiGet(`/documents/${docId}/guide`);
    const guide = data.guide;
    const doc = data.document;
    const prereqLinks = data.prerequisite_links || [];

    // Update stack name
    if (_stack.length > 0) {
      _stack[_stack.length - 1] = { docId, docName: doc.name };
    } else {
      _stack = [{ docId, docName: doc.name }];
    }

    renderGuideModal(guide, doc, prereqLinks, data.dependency_tree);

    // Re-setup focus after render
    if (_releaseFocusTrap) _releaseFocusTrap();
    _releaseFocusTrap = trapFocus(modal);

    announce(`Guide opened: How to obtain ${doc.name}`);
  } catch (e) {
    modal.innerHTML = `
      <div class="modal__header">
        <h2 class="modal__title" id="guide-modal-title">Guide Not Available</h2>
        <button class="modal__close" aria-label="Close guide" id="modal-close-btn">✕</button>
      </div>
      <div class="modal__body">
        <div class="inline-error">⚠ Could not load guide: ${e.message}</div>
      </div>
      <div class="modal__footer">
        <button class="btn btn--outline" id="modal-close-btn2">Close</button>
      </div>
    `;
    document.getElementById('modal-close-btn')?.addEventListener('click', closeModal);
    document.getElementById('modal-close-btn2')?.addEventListener('click', closeModal);
  }
}

function renderGuideModal(guide, doc, prereqLinks, depTree) {
  modal.innerHTML = '';

  // Header
  const header = document.createElement('div');
  header.className = 'modal__header';

  const title = document.createElement('h2');
  title.className = 'modal__title';
  title.id = 'guide-modal-title';
  title.textContent = `How to obtain: ${doc.name}`;

  const closeBtn = document.createElement('button');
  closeBtn.className = 'modal__close';
  closeBtn.setAttribute('aria-label', 'Close guide');
  closeBtn.textContent = '✕';
  closeBtn.addEventListener('click', closeModal);

  header.appendChild(title);
  header.appendChild(closeBtn);
  modal.appendChild(header);

  // Breadcrumb (if stack > 1)
  if (_stack.length > 1) {
    const breadcrumb = document.createElement('div');
    breadcrumb.className = 'modal__breadcrumb';
    breadcrumb.setAttribute('aria-label', 'Navigation breadcrumb');

    _stack.forEach((entry, i) => {
      if (i > 0) {
        const sep = document.createElement('span');
        sep.className = 'sep';
        sep.textContent = '›';
        breadcrumb.appendChild(sep);
      }
      if (i < _stack.length - 1) {
        const link = document.createElement('button');
        link.className = 'btn btn--ghost btn--sm';
        link.style.padding = '0 2px';
        link.textContent = entry.docName;
        const targetIndex = i;
        link.addEventListener('click', () => {
          const target = _stack[targetIndex];
          _stack = _stack.slice(0, targetIndex + 1);
          _loadGuide(target.docId, target.docName);
        });
        breadcrumb.appendChild(link);
      } else {
        const current = document.createElement('span');
        current.textContent = entry.docName;
        breadcrumb.appendChild(current);
      }
    });

    modal.appendChild(breadcrumb);
  }

  // Body
  const body = document.createElement('div');
  body.className = 'modal__body';

  // Status chip in body if available/missing
  const status = getStatus(doc.id);
  if (status !== 'unmarked') {
    const statusBadge = document.createElement('div');
    statusBadge.style.cssText = `display:inline-flex; align-items:center; gap:var(--space-2); padding:var(--space-2) var(--space-4); border-radius:999px; font-size:var(--font-size-sm); font-weight:600; background:${status === 'available' ? 'var(--green-tint)' : 'var(--amber-tint)'}; color:${status === 'available' ? 'var(--green)' : 'var(--amber)'};`;
    statusBadge.textContent = status === 'available' ? '✓ You have this document' : '✗ Marked as missing';
    body.appendChild(statusBadge);
  }

  // What it is
  if (guide.what_it_is) {
    const sect = createSection('What it is');
    const p = document.createElement('p');
    p.textContent = guide.what_it_is;
    p.style.fontSize = 'var(--font-size-sm)';
    sect.appendChild(p);
    body.appendChild(sect);
  }

  // Prerequisite documents (clickable!)
  if (prereqLinks.length) {
    const sect = createSection('Prerequisites (obtain these first)');
    const list = document.createElement('div');
    list.className = 'modal__prereq-list';

    prereqLinks.forEach(prereq => {
      const chip = document.createElement('button');
      chip.className = 'prereq-chip';
      chip.setAttribute('aria-label', `View guide for ${prereq.name}`);

      const nameEl = document.createElement('span');
      nameEl.className = 'prereq-chip__name';
      nameEl.textContent = prereq.name;

      const statusEl = document.createElement('span');
      statusEl.className = 'prereq-chip__status';
      const prereqStatus = getStatus(prereq.document_id);
      statusEl.textContent = prereqStatus === 'available' ? '✓ Have it' : prereqStatus === 'missing' ? '✗ Missing' : '○ Unset';
      statusEl.style.color = prereqStatus === 'available' ? 'var(--green)' : prereqStatus === 'missing' ? 'var(--amber)' : 'var(--grey)';

      chip.appendChild(nameEl);
      chip.appendChild(statusEl);

      chip.addEventListener('click', () => {
        if (prereq.has_guide) {
          _stack.push({ docId: prereq.document_id, docName: prereq.name });
          _loadGuide(prereq.document_id, prereq.name);
        }
      });

      list.appendChild(chip);
    });

    sect.appendChild(list);
    body.appendChild(sect);
  }

  // Documents required (display list)
  if (guide.documents_required?.length) {
    const sect = createSection('Documents You Need');
    const ul = document.createElement('ul');
    ul.style.cssText = 'list-style:disc; padding-left:var(--space-5); display:flex; flex-direction:column; gap:var(--space-2);';
    guide.documents_required.forEach(req => {
      const li = document.createElement('li');
      li.style.fontSize = 'var(--font-size-sm)';
      li.textContent = req;
      ul.appendChild(li);
    });
    sect.appendChild(ul);
    body.appendChild(sect);
  }

  // Procedure steps
  if (guide.procedure_steps?.length) {
    const sect = createSection('Basic Procedure');
    const steps = document.createElement('div');
    steps.className = 'modal__steps';

    guide.procedure_steps.forEach((step, i) => {
      const stepEl = document.createElement('div');
      stepEl.className = 'modal__step';

      const num = document.createElement('div');
      num.className = 'modal__step-num';
      num.setAttribute('aria-hidden', 'true');
      num.textContent = String(i + 1);

      const text = document.createElement('div');
      text.style.fontSize = 'var(--font-size-sm)';
      text.textContent = step;

      stepEl.appendChild(num);
      stepEl.appendChild(text);
      steps.appendChild(stepEl);
    });

    sect.appendChild(steps);
    body.appendChild(sect);
  }

  // Where / how to apply
  if (guide.where_how_to_apply) {
    const sect = createSection('Where / How to Apply');
    const p = document.createElement('p');
    p.textContent = guide.where_how_to_apply;
    p.style.fontSize = 'var(--font-size-sm)';
    sect.appendChild(p);

    if (guide.official_link) {
      const link = document.createElement('a');
      link.href = guide.official_link;
      link.target = '_blank';
      link.rel = 'noopener noreferrer';
      link.className = 'btn btn--teal btn--sm';
      link.textContent = 'Visit Official Portal ↗';
      link.style.marginTop = 'var(--space-3)';
      sect.appendChild(link);
    }

    body.appendChild(sect);
  }

  // Precautions
  if (guide.precautions?.length) {
    const sect = createSection('Important Precautions');
    const ul = document.createElement('ul');
    ul.style.cssText = 'display:flex; flex-direction:column; gap:var(--space-2);';
    guide.precautions.forEach(p => {
      const li = document.createElement('li');
      li.style.cssText = 'display:flex; gap:var(--space-2); font-size:var(--font-size-sm); align-items:flex-start;';
      const warn = document.createElement('span');
      warn.setAttribute('aria-hidden', 'true');
      warn.textContent = '⚠';
      warn.style.color = 'var(--amber)';
      warn.style.flexShrink = '0';
      const text = document.createElement('span');
      text.textContent = p;
      li.appendChild(warn);
      li.appendChild(text);
      ul.appendChild(li);
    });
    sect.appendChild(ul);
    body.appendChild(sect);
  }

  modal.appendChild(body);

  // Footer
  const footer = document.createElement('div');
  footer.className = 'modal__footer';

  if (_stack.length > 1) {
    const backBtn = document.createElement('button');
    backBtn.className = 'btn btn--outline';
    backBtn.textContent = '← Back';
    backBtn.addEventListener('click', () => {
      _stack.pop();
      const prev = _stack[_stack.length - 1];
      _loadGuide(prev.docId, prev.docName);
    });
    footer.appendChild(backBtn);
  }

  const closeFooterBtn = document.createElement('button');
  closeFooterBtn.className = 'btn btn--ghost';
  closeFooterBtn.textContent = 'Back to Checklist';
  closeFooterBtn.addEventListener('click', closeModal);
  footer.appendChild(closeFooterBtn);

  // "I now have this" button
  const haveItBtn = document.createElement('button');
  haveItBtn.className = 'btn btn--teal';
  haveItBtn.textContent = '✓ I now have this document';
  haveItBtn.addEventListener('click', () => {
    setStatus(doc.id, 'available');
    showToast(`${doc.name} marked as Available.`, 'success');
    closeModal();
  });
  footer.appendChild(haveItBtn);

  modal.appendChild(footer);
}

function createSection(titleText) {
  const sect = document.createElement('div');
  const title = document.createElement('div');
  title.className = 'modal__section-title';
  title.textContent = titleText;
  sect.appendChild(title);
  return sect;
}

function closeModal() {
  if (!backdrop || !modal) return;
  backdrop.hidden = true;
  modal.innerHTML = '';
  _stack = [];
  _currentDocId = null;
  if (_releaseFocusTrap) { _releaseFocusTrap(); _releaseFocusTrap = null; }
  if (_releaseEscape) { _releaseEscape(); _releaseEscape = null; }
  // Return focus to trigger
  if (_triggerButton) {
    _triggerButton.focus();
    _triggerButton = null;
  }
  announce('Guide closed.');
}

// Close when clicking backdrop
backdrop?.addEventListener('click', (e) => {
  if (e.target === backdrop) closeModal();
});
