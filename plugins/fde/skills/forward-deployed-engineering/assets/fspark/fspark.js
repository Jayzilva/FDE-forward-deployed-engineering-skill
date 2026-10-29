/* FSPARK: Feedback-based Spotlight Presentation, Assessment, Response & Knowledge.
   Presentation  - a spotlight tour, one stop per feature, switching screens as needed.
   Assessment    - a reaction on each stop (looks right, needs changes, not needed, not sure).
   Response      - an optional note per stop, plus closing questions.
   Knowledge     - a Markdown feedback file the viewer previews, edits, downloads or copies,
                   with a team-response table for the next round.
   Config: a JSON script tag with id "fspark" (see add_fspark.py --example).
   Works in a normal window, in a Claude artifact (downloads capability) and in viewers
   that size the frame to the whole page. */
(function () {
  var cfgEl = document.getElementById('fspark') || document.getElementById('fde-tour');
  if (!cfgEl) return;
  var C; try { C = JSON.parse(cfgEl.textContent); } catch (e) { console.error('FSPARK: bad JSON', e); return; }
  var S = C.steps || [], KEY = 'fspark:' + (C.storageKey || C.title || 'tour');
  var REACT = C.reactions || [['right', 'Looks right'], ['change', 'Needs changes'], ['notneeded', 'Not needed'], ['unsure', 'Not sure']];
  var Q = C.questions || ['What is missing that you need?', 'Overall, would this help your team? Why?'];
  var LABEL = {}; REACT.forEach(function (r) { LABEL[r[0]] = r[1]; });
  var st = { name: '', role: '', fb: {}, ans: {} }, i = -1, root, spot, card, sheet, md = '', placedScroll = false;
  try { var saved = JSON.parse(localStorage.getItem(KEY) || 'null'); if (saved) st = Object.assign(st, saved); } catch (e) {}
  function save() { try { localStorage.setItem(KEY, JSON.stringify(st)); } catch (e) {} }
  function esc(t) { return String(t == null ? '' : t).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function el(tag, cls) { var e = document.createElement(tag); if (cls) e.className = cls; return e; }
  function target(s) { try { return s.target ? document.querySelector(s.target) : null; } catch (e) { return null; } }
  function fb(k) { return st.fb[k] || (st.fb[k] = { r: '', n: '' }); }
  function reviewed() { var n = 0; for (var k = 0; k < S.length; k++) { var f = st.fb[k]; if (f && (f.r || f.n)) n++; } return n; }

  /* ---- visible band: the part of the page the viewer can see ---- */
  var band = { top: 0, h: innerHeight }, STRIP = 20, strips = null, io = null, vis = {};
  function tall() { var sh = (window.screen && screen.availHeight) || 900; return innerHeight > sh + 80; }
  function setBand(top, h) { band = { top: Math.max(0, top), h: Math.max(320, h) }; relayout(); }
  function buildStrips() {
    if (!('IntersectionObserver' in window)) return;
    var H = Math.max(document.documentElement.scrollHeight, document.body.scrollHeight);
    if (strips && strips.H === H) return;
    if (strips) { io.disconnect(); strips.el.remove(); }
    var box = el('div'); box.setAttribute('aria-hidden', 'true');
    box.style.cssText = 'position:absolute;left:0;top:0;width:1px;height:' + H + 'px;pointer-events:none;visibility:hidden;z-index:-1';
    vis = {};
    io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { var k = +e.target.dataset.k; if (e.intersectionRatio >= 0.99) vis[k] = 1; else delete vis[k]; });
      var ks = Object.keys(vis).map(Number); if (!ks.length || !tall()) return;
      var lo = Math.min.apply(0, ks), hi = Math.max.apply(0, ks); setBand(lo * STRIP, (hi - lo + 1) * STRIP);
    }, { threshold: [0, 0.99] });
    for (var k = 0; k * STRIP < H; k++) { var d = el('i'); d.dataset.k = k; d.style.cssText = 'position:absolute;left:0;width:1px;height:' + STRIP + 'px;top:' + (k * STRIP) + 'px'; box.appendChild(d); io.observe(d); }
    document.body.appendChild(box); strips = { el: box, H: H };
  }
  setTimeout(function () { if (tall()) buildStrips(); }, 300);
  addEventListener('resize', function () { if (!tall()) setBand(0, innerHeight); else place(); });
  function relayout() { if (!root || root.hidden) return; if (!sheet.hidden) fitSheet(); if (i < 0 && !card.hidden) center(); else place(); }
  function center() { card.style.left = '50%'; card.style.top = (band.top + band.h / 2) + 'px'; }
  function fitSheet() {
    sheet.style.top = band.top + 'px'; sheet.style.height = band.h + 'px';
    var pn = sheet.querySelector('.fsp-panel'); if (pn) pn.style.maxHeight = (band.h - 48) + 'px';
    [].forEach.call(sheet.querySelectorAll('.fsp-preview,.fsp-md'), function (x) { x.style.maxHeight = Math.round(band.h * .5) + 'px'; if (x.classList.contains('fsp-md')) x.style.minHeight = Math.round(band.h * .4) + 'px'; });
  }

  function build() {
    root = el('div', 'fsp-root'); root.setAttribute('role', 'dialog'); root.setAttribute('aria-modal', 'true'); root.setAttribute('aria-label', C.title || 'Feedback tour');
    spot = el('div', 'fsp-spot'); card = el('div', 'fsp-card'); card.setAttribute('aria-live', 'polite');
    sheet = el('div', 'fsp-sheet'); sheet.hidden = true;
    root.appendChild(spot); root.appendChild(card); root.appendChild(sheet); document.body.appendChild(root);
    root.addEventListener('click', onClick); root.addEventListener('input', onInput);
    document.addEventListener('keydown', function (e) {
      if (!root || root.hidden || /TEXTAREA|INPUT/.test(e.target.tagName)) return;
      if (e.key === 'Escape') close(); else if (e.key === 'ArrowRight' && i >= 0) go(i + 1); else if (e.key === 'ArrowLeft' && i > 0) go(i - 1);
    });
    addEventListener('scroll', place, { passive: true });
  }

  function onClick(e) {
    var b = e.target.closest('[data-a]'); if (!b) return; var a = b.getAttribute('data-a');
    if (a === 'next') go(i + 1); else if (a === 'back') go(i - 1); else if (a === 'close') close();
    else if (a === 'start') go(0); else if (a === 'dot' || a === 'edit-stop') go(+b.getAttribute('data-i'));
    else if (a === 'react') { var f = fb(i); f.r = (f.r === b.getAttribute('data-r')) ? '' : b.getAttribute('data-r'); save(); render(S[i], !!target(S[i])); requestAnimationFrame(place); }
    else if (a === 'review') review(); else if (a === 'make') makeFile(); else if (a === 'tab') tab(b.getAttribute('data-t'));
    else if (a === 'download') download(b); else if (a === 'copy') copy(b);
  }
  function onInput(e) {
    var t = e.target, f = t.getAttribute('data-f'); if (!f) return;
    if (f === 'note') fb(i).n = t.value; else if (f === 'md') { md = t.value; return; }
    else if (f.indexOf('q') === 0) st.ans[f] = t.value; else st[f] = t.value;
    save();
  }

  function welcome() {
    if (!root) build();
    root.hidden = false; sheet.hidden = true; card.hidden = false; i = -1; spot.hidden = true; card.className = 'fsp-card fsp-center'; center();
    card.innerHTML = '<span class="fsp-kick">' + esc(C.kicker || 'Feedback tour') + '</span><h2>' + esc(C.title || 'Tell us what you think') + '</h2>' +
      '<p>' + esc(C.intro || (S.length + ' stops. Each stop shows one feature. Pick a reaction and add a note if you like. At the end you get a feedback file to send back.')) + '</p>' +
      '<div class="fsp-who"><label>Your name<input data-f="name" value="' + esc(st.name) + '" placeholder="Optional" autocomplete="name"></label>' +
      '<label>Your role<input data-f="role" value="' + esc(st.role) + '" placeholder="For example Finance lead"></label></div>' +
      '<p class="fsp-hint">' + esc(C.privacy || 'Your answers stay in this browser until you download or copy the file.') + '</p>' +
      '<div class="fsp-acts">' + (reviewed() ? '<button class="fsp-btn" type="button" data-a="review">Review my feedback</button>' : '<button class="fsp-btn" type="button" data-a="close">Later</button>') +
      '<button class="fsp-btn fsp-primary" type="button" data-a="start">' + (reviewed() ? 'Continue the tour' : 'Start the tour') + '</button></div>';
    card.querySelector('[data-a="start"]').focus({ preventScroll: true });
  }

  function go(n) {
    if (n < 0) return;
    if (n >= S.length) { review(); return; }
    sheet.hidden = true; card.hidden = false; i = n; placedScroll = false; var s = S[i];
    if (s.screen && location.hash.slice(1) !== s.screen.replace(/^#/, '')) location.hash = s.screen.replace(/^#/, '');
    setTimeout(function () {
      if (tall()) buildStrips();
      var t = target(s);
      if (t) t.scrollIntoView({ block: t.getBoundingClientRect().height > band.h * .6 ? 'start' : 'center', behavior: 'instant' });
      render(s, !!t); requestAnimationFrame(place);
    }, s.screen ? 180 : 40);
  }

  function render(s, found) {
    spot.hidden = !found; var f = st.fb[i] || { r: '', n: '' };
    var dots = ''; for (var k = 0; k < S.length; k++) { var d = st.fb[k]; dots += '<button type="button" class="fsp-dot' + (k === i ? ' on' : '') + (d && d.r ? ' done' : '') + '" data-a="dot" data-i="' + k + '" aria-label="Stop ' + (k + 1) + '"></button>'; }
    var chips = REACT.map(function (r) { return '<button type="button" class="fsp-chip fsp-' + r[0] + '" data-a="react" data-r="' + r[0] + '" aria-pressed="' + (f.r === r[0]) + '">' + esc(r[1]) + '</button>'; }).join('');
    card.className = 'fsp-card' + (found ? '' : ' fsp-center'); card.style.left = ''; card.style.top = '';
    card.innerHTML = '<div class="fsp-top"><span class="fsp-kick">' + (i + 1) + ' of ' + S.length + '</span><button class="fsp-x" type="button" data-a="close" aria-label="Close the tour">×</button></div>' +
      '<h2>' + esc(s.title) + '</h2><p>' + esc(s.body) + '</p>' + (s.tag ? '<span class="fsp-tag">' + esc(s.tag) + '</span>' : '') +
      '<div class="fsp-q">' + esc(s.question || C.stopQuestion || 'Does this fit how you work?') + '</div><div class="fsp-chips" role="group" aria-label="Your reaction">' + chips + '</div>' +
      '<label class="fsp-note"><span>Note (optional)</span><textarea data-f="note" rows="2" placeholder="What works, what is missing, what would you change?">' + esc(f.n) + '</textarea></label>' +
      '<div class="fsp-dots">' + dots + '</div><div class="fsp-acts">' + (i > 0 ? '<button class="fsp-btn" type="button" data-a="back">Back</button>' : '<span></span>') +
      '<button class="fsp-btn fsp-primary" type="button" data-a="next">' + (i === S.length - 1 ? 'Review feedback' : 'Next') + '</button></div>';
    if (!found) center();
    card.querySelector('[data-a="next"]').focus({ preventScroll: true });
  }

  function place() {
    if (!root || root.hidden || i < 0 || card.hidden) return;
    var t = target(S[i]); if (!t) { center(); return; }
    var R = t.getBoundingClientRect(), pad = 8, vh = band.h, vw = innerWidth, B = band.top;
    var r = { top: R.top - B, bottom: R.bottom - B, left: R.left, right: R.right, width: R.width, height: R.height };
    var top = Math.max(8, r.top - pad), bot = Math.min(vh - 8, r.bottom + pad);
    spot.style.left = Math.max(8, r.left - pad) + 'px'; spot.style.top = (B + top) + 'px';
    spot.style.width = Math.min(vw - 16, r.width + pad * 2) + 'px'; spot.style.height = Math.max(24, bot - top) + 'px';
    if (vw < 760) { card.classList.add('fsp-dock'); card.style.left = ''; card.style.top = (B + vh - card.offsetHeight - 16) + 'px'; return; }
    card.classList.remove('fsp-dock');
    var cw = card.offsetWidth, ch = card.offsetHeight, x = Math.min(Math.max(12, r.left), vw - cw - 12), y;
    if (vh - bot > ch + 16) y = bot + 12; else if (top > ch + 16) y = top - ch - 12;
    else if (r.right + cw + 24 < vw) { x = r.right + 12; y = Math.min(Math.max(12, top), vh - ch - 12); }
    else if (r.left - cw - 24 > 0) { x = r.left - cw - 12; y = Math.min(Math.max(12, top), vh - ch - 12); }
    else if (!placedScroll && r.height + ch + 60 < vh) { placedScroll = true; t.scrollIntoView({ block: 'start', behavior: 'instant' }); if (!tall()) scrollBy(0, -24); return; }
    else y = Math.max(12, vh - ch - 16);
    card.style.left = x + 'px'; card.style.top = (B + y) + 'px';
  }

  /* ---- assessment summary, response and the knowledge file ---- */
  function counts() { var c = { none: 0 }; REACT.forEach(function (r) { c[r[0]] = 0; }); for (var k = 0; k < S.length; k++) { var f = st.fb[k]; if (f && f.r) c[f.r]++; else c.none++; } return c; }

  function review() {
    if (!root) build(); root.hidden = false; i = -1; spot.hidden = true; card.hidden = true; sheet.hidden = false;
    var c = counts();
    var tiles = REACT.map(function (r) { return '<div><b>' + c[r[0]] + '</b><span>' + esc(r[1]) + '</span></div>'; }).join('') + '<div><b>' + c.none + '</b><span>Not reviewed</span></div>';
    var rows = S.map(function (s, k) { var f = st.fb[k] || {}; return '<tr><td>' + (k + 1) + '</td><td><b>' + esc(s.title) + '</b>' + (s.tag ? '<small>' + esc(s.tag) + '</small>' : '') + '</td><td>' + (f.r ? '<span class="fsp-chip fsp-' + f.r + '" aria-pressed="true">' + esc(LABEL[f.r]) + '</span>' : '<span class="fsp-none">Not reviewed</span>') + '</td><td class="fsp-n">' + esc(f.n || '') + '</td><td><button type="button" class="fsp-btn fsp-sm" data-a="edit-stop" data-i="' + k + '">Edit</button></td></tr>'; }).join('');
    var qs = Q.map(function (q, n) { return '<label class="fsp-note"><span>' + esc(q) + '</span><textarea data-f="q' + n + '" rows="3">' + esc(st.ans['q' + n] || '') + '</textarea></label>'; }).join('');
    sheet.innerHTML = '<div class="fsp-panel" role="document"><div class="fsp-top"><span class="fsp-kick">Your feedback · ' + reviewed() + ' of ' + S.length + ' stops</span><button class="fsp-x" type="button" data-a="close" aria-label="Close">×</button></div>' +
      '<h2>Review your feedback</h2><div class="fsp-sum">' + tiles + '</div>' +
      '<div class="fsp-table"><table><thead><tr><th>#</th><th>Feature</th><th>Reaction</th><th>Note</th><th></th></tr></thead><tbody>' + rows + '</tbody></table></div>' + qs +
      '<div class="fsp-acts"><button class="fsp-btn" type="button" data-a="start">Back to the tour</button><button class="fsp-btn fsp-primary" type="button" data-a="make">Create feedback file</button></div></div>';
    fitSheet(); sheet.querySelector('[data-a="make"]').focus({ preventScroll: true });
  }

  function buildMd() {
    var c = counts(), d = new Date(), date = d.getFullYear() + '-' + String(d.getMonth() + 1).padStart(2, '0') + '-' + String(d.getDate()).padStart(2, '0'), L = [];
    L.push('# Feedback: ' + (C.product || C.title || 'Prototype'), '');
    L.push('- **Reviewer:** ' + (st.name || 'Not given') + (st.role ? ' (' + st.role + ')' : ''));
    L.push('- **Date:** ' + date);
    if (C.prototypeUrl) L.push('- **Prototype:** ' + C.prototypeUrl + (C.version ? ' (version ' + C.version + ')' : ''));
    L.push('- **Stops reviewed:** ' + reviewed() + ' of ' + S.length, '');
    L.push('## Summary', '', '| Reaction | Count |', '|---|---|');
    REACT.forEach(function (r) { L.push('| ' + r[1] + ' | ' + c[r[0]] + ' |'); }); L.push('| Not reviewed | ' + c.none + ' |', '');
    L.push('## Feedback by feature', '');
    S.forEach(function (s, k) { var f = st.fb[k] || {};
      L.push('### ' + (k + 1) + '. ' + s.title, '');
      if (s.tag) L.push('- **Requirement:** ' + s.tag);
      L.push('- **Reaction:** ' + (f.r ? LABEL[f.r] : 'Not reviewed'));
      L.push('- **Note:** ' + ((f.n || '').trim() ? f.n.trim().replace(/\n+/g, ' ') : '—'), ''); });
    Q.forEach(function (q, n) { L.push('## ' + q, '', (st.ans['q' + n] || '').trim() || '—', ''); });
    L.push('## Delivery team response', '', '_Filled in by the delivery team and sent back with the next version._', '');
    L.push('| # | Feature | Reaction | Team response | Status |', '|---|---|---|---|---|');
    S.forEach(function (s, k) { var f = st.fb[k] || {}; if ((f.r && f.r !== REACT[0][0]) || (f.n || '').trim()) L.push('| ' + (k + 1) + ' | ' + s.title + ' | ' + (f.r ? LABEL[f.r] : 'Note only') + ' |  | Open |'); });
    L.push(''); return L.join('\n');
  }

  function makeFile() {
    md = buildMd();
    sheet.innerHTML = '<div class="fsp-panel" role="document"><div class="fsp-top"><span class="fsp-kick">Feedback file</span><button class="fsp-x" type="button" data-a="close" aria-label="Close">×</button></div>' +
      '<h2>Check and send your feedback</h2><p>' + esc(C.outro || 'Edit anything you like, then download the file or copy the text and send it to your delivery lead.') + '</p>' +
      '<div class="fsp-tabs" role="tablist"><button type="button" role="tab" data-a="tab" data-t="preview" aria-pressed="true">Preview</button><button type="button" role="tab" data-a="tab" data-t="edit" aria-pressed="false">Edit</button></div>' +
      '<div class="fsp-preview" id="fspPreview"></div><textarea class="fsp-md" id="fspMd" data-f="md" hidden spellcheck="true"></textarea><p class="fsp-status" id="fspStatus" role="status"></p>' +
      '<div class="fsp-acts"><button class="fsp-btn" type="button" data-a="review">Back</button><span class="fsp-right"><button class="fsp-btn" type="button" data-a="copy">Copy text</button><button class="fsp-btn fsp-primary" type="button" data-a="download">Download .md</button></span></div></div>';
    document.getElementById('fspMd').value = md; tab('preview'); fitSheet();
  }
  function tab(t) {
    var area = document.getElementById('fspMd'), pv = document.getElementById('fspPreview'); if (!area) return;
    if (t === 'preview') { md = area.value; pv.innerHTML = renderMd(md); }
    area.hidden = (t !== 'edit'); pv.hidden = (t !== 'preview');
    [].forEach.call(sheet.querySelectorAll('.fsp-tabs button'), function (b) { b.setAttribute('aria-pressed', String(b.getAttribute('data-t') === t)); });
    if (t === 'edit') area.focus({ preventScroll: true });
  }
  function inline(s) { return esc(s).replace(/\*\*(.+?)\*\*/g, '<b>$1</b>').replace(/(^|\s)_(.+?)_(?=\s|$)/g, '$1<i>$2</i>').replace(/(https?:\/\/[^\s|)]+)/g, '<a href="$1" target="_blank" rel="noopener">$1</a>'); }
  function renderMd(src) {
    var out = [], ls = src.split('\n'), k = 0, cells = function (r) { return r.replace(/^\||\|$/g, '').split('|').map(function (c) { return c.trim(); }); };
    while (k < ls.length) { var ln = ls[k];
      if (/^### /.test(ln)) { out.push('<h4>' + inline(ln.slice(4)) + '</h4>'); k++; continue; }
      if (/^## /.test(ln)) { out.push('<h3>' + inline(ln.slice(3)) + '</h3>'); k++; continue; }
      if (/^# /.test(ln)) { out.push('<h2>' + inline(ln.slice(2)) + '</h2>'); k++; continue; }
      if (/^\|/.test(ln)) { var rows = []; while (k < ls.length && /^\|/.test(ls[k])) { rows.push(ls[k]); k++; }
        out.push('<table><thead><tr>' + cells(rows[0]).map(function (c) { return '<th>' + inline(c) + '</th>'; }).join('') + '</tr></thead><tbody>' + rows.slice(2).map(function (r) { return '<tr>' + cells(r).map(function (c) { return '<td>' + inline(c) + '</td>'; }).join('') + '</tr>'; }).join('') + '</tbody></table>'); continue; }
      if (/^- /.test(ln)) { var it = []; while (k < ls.length && /^- /.test(ls[k])) { it.push('<li>' + inline(ls[k].slice(2)) + '</li>'); k++; } out.push('<ul>' + it.join('') + '</ul>'); continue; }
      if (ln.trim() === '') { k++; continue; }
      out.push('<p>' + inline(ln) + '</p>'); k++; }
    return out.join('');
  }
  function current() { var a = document.getElementById('fspMd'); return a ? a.value : md; }
  function fileName() { var n = (st.name || 'reviewer').toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '') || 'reviewer'; return (C.fileName || 'feedback') + '-' + n + '.md'; }
  function status(t) { var s = document.getElementById('fspStatus'); if (s) s.textContent = t; }
  function download(btn) {
    var text = current(), name = fileName();
    function plain() {
      try { var url = URL.createObjectURL(new Blob([text], { type: 'text/markdown' })), a = el('a'); a.href = url; a.download = name; document.body.appendChild(a); a.click(); a.remove(); setTimeout(function () { URL.revokeObjectURL(url); }, 2000); status('Downloaded ' + name + '. Send it to your delivery lead.'); }
      catch (e) { status('Download is not available here. Use Copy text and paste it into an email.'); }
    }
    if (!(window.claude && window.claude.use)) { plain(); return; }
    btn.disabled = true;
    window.claude.use('downloads').then(function (dl) {
      if (!dl) { status('Download is not available in this view. Use Copy text and paste it into an email.'); return; }
      return dl.save({ filename: name, data: text }).then(function () { status('Saved ' + name + '. Send it to your delivery lead.'); },
        function (e) { status(e && e.code === 'declined' ? 'Download cancelled. Try again or use Copy text.' : 'Download is not available here. Use Copy text instead.'); });
    }).catch(function () { status('Download is not available here. Use Copy text instead.'); }).then(function () { btn.disabled = false; });
  }
  function copy(btn) {
    var text = current();
    function fallback() { tab('edit'); var a = document.getElementById('fspMd'); a.focus(); a.select(); status('Text selected. Press Ctrl+C (or Cmd+C) to copy.'); }
    try { navigator.clipboard.writeText(text).then(function () { btn.textContent = 'Copied'; status('Copied. Paste it into an email or chat to your delivery lead.'); }, fallback); } catch (e) { fallback(); }
  }
  function close() { if (root) root.hidden = true; i = -1; try { localStorage.setItem(KEY + ':seen', '1'); } catch (e) {} }

  var label = '<span aria-hidden="true">✦</span> ' + esc(C.launchLabel || 'Tour and feedback');
  var launch = el('button', 'fsp-launch'); launch.type = 'button'; launch.innerHTML = label; launch.addEventListener('click', welcome); document.body.appendChild(launch);
  if (C.mount) { var m = document.querySelector(C.mount); if (m) { var b2 = el('button', 'fsp-btn fsp-primary fsp-inline'); b2.type = 'button'; b2.innerHTML = label; b2.addEventListener('click', welcome); m.appendChild(b2); } }
  window.fspark = { start: welcome, go: go, review: review, file: function () { review(); makeFile(); } };
  var seen = false; try { seen = localStorage.getItem(KEY + ':seen') === '1'; } catch (e) {}
  if (C.autoStart !== false && !seen) setTimeout(welcome, 700);
})();
