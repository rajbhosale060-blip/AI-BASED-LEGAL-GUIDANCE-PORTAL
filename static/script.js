/**
 * AI Legal Aid Portal — Global JavaScript Utilities
 */

// ── Auto-dismiss flash messages ────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  const flashes = document.querySelectorAll('.flash-alert');
  flashes.forEach(el => {
    setTimeout(() => {
      el.style.transition = 'opacity .4s';
      el.style.opacity = '0';
      setTimeout(() => el.remove(), 400);
    }, 5000);
  });

  // Active nav link highlight
  const path = window.location.pathname;
  document.querySelectorAll('.nav-links a').forEach(a => {
    if (a.getAttribute('href') === path) a.classList.add('active');
  });

  // Animate stat numbers
  document.querySelectorAll('.stat-num').forEach(el => {
    const target = parseInt(el.textContent) || 0;
    if (target === 0) return;
    let current = 0;
    const step = Math.ceil(target / 30);
    const timer = setInterval(() => {
      current = Math.min(current + step, target);
      el.textContent = current;
      if (current >= target) clearInterval(timer);
    }, 40);
  });
});

// ── Utility: format file size ─────────────────────────────────────────────────
function formatBytes(bytes) {
  if (bytes < 1024) return bytes + ' B';
  if (bytes < 1048576) return (bytes / 1024).toFixed(1) + ' KB';
  return (bytes / 1048576).toFixed(1) + ' MB';
}

// ── Utility: copy to clipboard ────────────────────────────────────────────────
function copyToClipboard(text) {
  navigator.clipboard.writeText(text).then(() => {
    showToast('Copied to clipboard!', 'success');
  });
}

// ── Mini toast notification ───────────────────────────────────────────────────
function showToast(message, type = 'info') {
  const toast = document.createElement('div');
  toast.style.cssText = `
    position:fixed;bottom:1.5rem;right:1.5rem;z-index:9999;
    background:rgba(15,12,29,0.95);backdrop-filter:blur(16px);
    border-radius:10px;padding:.75rem 1.25rem;
    border-left:3px solid ${type === 'success' ? '#10b981' : type === 'danger' ? '#ef4444' : '#7c3aed'};
    color:#f1f0ff;font-size:.85rem;box-shadow:0 8px 32px rgba(0,0,0,0.4);
    animation:slideIn .3s ease;
  `;
  toast.textContent = message;
  document.body.appendChild(toast);
  setTimeout(() => { toast.style.opacity = '0'; toast.style.transition = 'opacity .4s'; setTimeout(() => toast.remove(), 400); }, 3000);
}

// ── Smooth scroll to element ──────────────────────────────────────────────────
function scrollTo(id) {
  const el = document.getElementById(id);
  if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

// ── Keyboard shortcut: Ctrl+K → focus search ─────────────────────────────────
document.addEventListener('keydown', e => {
  if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
    e.preventDefault();
    const search = document.getElementById('searchInput');
    if (search) search.focus();
  }
});
