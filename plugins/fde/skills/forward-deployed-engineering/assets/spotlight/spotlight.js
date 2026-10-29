/* FDE spotlight tour: a guided, step-by-step product tour for any HTML prototype.
   Config: a JSON script tag with id "fde-tour" (see add_spotlight.py --example).
   Each step can switch screen (location.hash), spotlights one element, explains it,
   and lets the viewer leave a note. Notes stay in the viewer's browser and can be copied back. */
(function () {
  var cfgEl = document.getElementById('fde-tour');
  if (!cfgEl) return;
  var C; try { C = JSON.parse(cfgEl.textContent); } catch (e) { console.error('fde-tour: bad JSON', e); return; }
  var S = C.steps || [], KEY = C.storageKey || 'fde-tour', i = -1, root, spot, card, notes = {};
  function store(get, k, v) { try { return get ? localStorage.getItem(KEY + k) : localStorage.setItem(KEY + k, v); } catch (e) { return null; } }
  try { notes = JSON.parse(store(true, ':notes') || '{}'); } catch (e) { notes = {}; }
  function esc(t) { return String(t == null ? '' : t).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function find(s) { try { return s.target ? document.querySelector(s.target) : null; } catch (e) { return null; } }
  function mk(tag, cls) { var e = document.createElement(tag); if (cls) e.className = cls; return e; }

  function build() {
    root = mk('div', 'fdt-root'); root.setAttribute('role', 'dialog'); root.setAttribute('aria-modal', 'true');
    root.setAttribute('aria-label', C.title || 'Guided tour');
    spot = mk('div', 'fdt-spot'); card = mk('div', 'fdt-card'); card.setAttribute('aria-live', 'polite');
    root.appendChild(spot); root.appendChild(card); document.body.appendChild(root);
    root.addEventListener('click', function (e) {
      var b = e.target.closest('[data-fdt]'); if (!b) return;
      var a = b.getAttribute('data-fdt');
      if (a === 'next') go(i + 1); else if (a === 'back') go(i - 1); else if (a === 'close') close();
      else if (a === 'start') go(0); else if (a === 'dot') go(+b.getAttribute('data-i'));
      else if (a === 'note') { var w = card.querySelector('.fdt-note'); w.hidden = !w.hidden; if (!w.hidden) w.querySelector('textarea').focus(); }
      else if (a === 'copy') copyNotes(b);
    });
    root.addEventListener('input', function (e) {
      if (e.target.matches('.fdt-note textarea')) { notes[i] = e.target.value; store(false, ':notes', JSON.stringify(notes)); }
    });
    document.addEventListener('keydown', function (e) {
      if (root.hidden || e.target.matches('textarea')) return;
      if (e.key === 'Escape') close(); else if (e.key === 'ArrowRight') go(i + 1); else if (e.key === 'ArrowLeft' && i > 0) go(i - 1);
    });
    window.addEventListener('resize', place); document.addEventListener('scroll', place, { passive: true, capture: true });
  }

  function welcome() {
    if (!root) build();
    root.hidden = false; i = -1; spot.hidden = true; card.className = 'fdt-card fdt-center';
    card.innerHTML = '<span class="fdt-kick">' + esc(C.kicker || 'Guided tour') + '</span><h2>' + esc(C.title || 'What is new') + '</h2><p>' +
      esc(C.intro || (S.length + ' stops. Each stop shows one feature.')) + '</p>' +
      (C.feedback !== false ? '<p class="fdt-hint">Leave a note on any stop. At the end you can copy all notes and send them back.</p>' : '') +
      '<div class="fdt-acts"><button type="button" class="fdt-btn" data-fdt="close">Later</button><button type="button" class="fdt-btn fdt-primary" data-fdt="start">Start the tour</button></div>';
    card.querySelector('[data-fdt="start"]').focus();
  }

  function go(n) {
    if (n < 0) return;
    if (n >= S.length) { summary(); return; }
    i = n; var s = S[i];
    if (s.screen && location.hash.slice(1) !== s.screen.replace(/^#/, '')) location.hash = s.screen.replace(/^#/, '');
    setTimeout(function () {
      var t = find(s);
      if (t) t.scrollIntoView({ block: t.getBoundingClientRect().height > innerHeight * 0.7 ? 'start' : 'center', behavior: 'instant' });
      render(s, !!t); requestAnimationFrame(place);
    }, s.screen ? 180 : 40);
  }

  function dots() {
    var d = ''; for (var k = 0; k < S.length; k++) d += '<button type="button" class="fdt-dot' + (k === i ? ' on' : '') + (notes[k] ? ' noted' : '') + '" data-fdt="dot" data-i="' + k + '" aria-label="Stop ' + (k + 1) + '"></button>';
    return '<div class="fdt-dots">' + d + '</div>';
  }

  function render(s, found) {
    spot.hidden = !found; card.className = 'fdt-card' + (found ? '' : ' fdt-center');
    card.innerHTML = '<div class="fdt-top"><span class="fdt-kick">' + (i + 1) + ' of ' + S.length + '</span><button type="button" class="fdt-x" data-fdt="close" aria-label="Close the tour">×</button></div>' +
      '<h2>' + esc(s.title) + '</h2><p>' + esc(s.body) + '</p>' + (s.tag ? '<span class="fdt-tag">' + esc(s.tag) + '</span>' : '') +
      (C.feedback !== false ? '<button type="button" class="fdt-link" data-fdt="note">' + (notes[i] ? 'Edit your note' : 'Add a note') + '</button><div class="fdt-note"' + (notes[i] ? '' : ' hidden') + '><label class="fdt-sr" for="fdt-n">Your note on this stop</label><textarea id="fdt-n" rows="3" placeholder="What works, what is missing, what would you change?">' + esc(notes[i] || '') + '</textarea></div>' : '') +
      dots() + '<div class="fdt-acts">' + (i > 0 ? '<button type="button" class="fdt-btn" data-fdt="back">Back</button>' : '<span></span>') +
      '<button type="button" class="fdt-btn fdt-primary" data-fdt="next">' + (i === S.length - 1 ? 'Finish' : 'Next') + '</button></div>';
    card.querySelector('[data-fdt="next"]').focus({ preventScroll: true });
  }

  function summary() {
    i = -1; spot.hidden = true; card.className = 'fdt-card fdt-center';
    var list = S.map(function (s, k) { return notes[k] ? '<li><b>' + esc(s.title) + '</b> ' + esc(notes[k]) + '</li>' : ''; }).join('');
    card.innerHTML = '<span class="fdt-kick">End of tour</span><h2>' + esc(C.outroTitle || 'Thank you') + '</h2><p>' + esc(C.outro || 'Tell us what to change. Copy your notes and send them back.') + '</p>' +
      (list ? '<ul class="fdt-sum">' + list + '</ul><div class="fdt-acts"><button type="button" class="fdt-btn" data-fdt="start">Tour again</button><button type="button" class="fdt-btn fdt-primary" data-fdt="copy">Copy my notes</button></div><textarea class="fdt-out" readonly hidden></textarea>'
        : '<p class="fdt-hint">No notes yet. Start again and add a note on any stop.</p><div class="fdt-acts"><button type="button" class="fdt-btn" data-fdt="close">Close</button><button type="button" class="fdt-btn fdt-primary" data-fdt="start">Tour again</button></div>');
    store(false, ':seen', '1');
  }

  function copyNotes(btn) {
    var text = (C.title || 'Tour') + ' — notes\n' + S.map(function (s, k) { return notes[k] ? '- ' + s.title + (s.tag ? ' [' + s.tag + ']' : '') + ': ' + notes[k] : ''; }).filter(Boolean).join('\n');
    var out = card.querySelector('.fdt-out');
    function fallback() { out.hidden = false; out.value = text; out.select(); btn.textContent = 'Select and copy the text'; }
    try { navigator.clipboard.writeText(text).then(function () { btn.textContent = 'Copied'; }, fallback); } catch (e) { fallback(); }
  }

  function place() {
    if (!root || root.hidden || i < 0) return;
    var t = find(S[i]); if (!t) return;
    var r = t.getBoundingClientRect(), p = 8, vh = innerHeight, vw = innerWidth;
    var top = Math.max(8, r.top - p), bot = Math.min(vh - 8, r.bottom + p);
    spot.style.left = Math.max(8, r.left - p) + 'px'; spot.style.top = top + 'px';
    spot.style.width = Math.min(vw - 16, r.width + p * 2) + 'px'; spot.style.height = Math.max(24, bot - top) + 'px';
    if (vw < 700) { card.classList.add('fdt-dock'); card.style.left = card.style.top = ''; return; }
    card.classList.remove('fdt-dock');
    var cw = card.offsetWidth, ch = card.offsetHeight, x = Math.min(Math.max(12, r.left), vw - cw - 12), y;
    if (vh - bot > ch + 16) y = bot + 12; else if (top > ch + 16) y = top - ch - 12;
    else if (r.right + cw + 24 < vw) { x = r.right + 12; y = Math.min(Math.max(12, top), vh - ch - 12); }
    else y = Math.max(12, vh - ch - 16);
    card.style.left = x + 'px'; card.style.top = y + 'px';
  }

  function close() { if (root) root.hidden = true; i = -1; store(false, ':seen', '1'); }

  var launch = mk('button', 'fdt-launch'); launch.type = 'button';
  launch.innerHTML = '<span aria-hidden="true">✦</span> ' + esc(C.launchLabel || 'Take the tour');
  launch.addEventListener('click', welcome); document.body.appendChild(launch);
  window.fdeTour = { start: welcome, go: go };
  if (C.autoStart !== false && store(true, ':seen') !== '1') setTimeout(welcome, 700);
})();
