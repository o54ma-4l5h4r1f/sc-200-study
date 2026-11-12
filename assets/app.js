/* SC-200 — shared runtime: theme, search, progress store, export/import.
   Classic script on purpose. No ES modules, no fetch — both are blocked over file:// in Chrome. */

(function () {
  'use strict';

  var AB = (window.SC200 = window.SC200 || {});
  var KEY = 'sc200.progress.v1';

  /* ------------------------------------------------------------------ store */

  function blank() {
    return { attempts: [], objectiveStats: {}, examSessions: [], labStatus: {}, labNotes: {} };
  }

  var memoryOnly = false;

  function load() {
    try {
      var raw = localStorage.getItem(KEY);
      if (raw) return Object.assign(blank(), JSON.parse(raw));
    } catch (e) {
      memoryOnly = true;
    }
    // localStorage empty or unavailable (a real risk over file://) — fall back to the
    // snapshot build.py baked in from progress/progress-export.json.
    var baked = (AB.data && AB.data.progressFallback) || null;
    if (baked && (baked.attempts || baked.objectiveStats)) {
      return Object.assign(blank(), baked);
    }
    return blank();
  }

  var state = load();

  function save() {
    try {
      localStorage.setItem(KEY, JSON.stringify(state));
    } catch (e) {
      if (!memoryOnly) {
        memoryOnly = true;
        toast('Progress could not be saved to this browser. Export it before you close the tab.');
      }
    }
  }

  var store = {
    get: function () { return state; },
    memoryOnly: function () { return memoryOnly; },

    /* One record per scored part. Problem/solution sets log three of these. */
    recordAttempt: function (rec) {
      rec.ts = new Date().toISOString();
      state.attempts.push(rec);
      (rec.objective_ids || []).forEach(function (oid) {
        var s = state.objectiveStats[oid] || { correct: 0, total: 0, recent: [], intervalDays: 1, lastSeen: null };
        var got = rec.score || 0;
        var max = rec.max_score || 1;
        s.correct += got;
        s.total += max;
        s.recent.push(got / max);
        if (s.recent.length > 5) s.recent.shift();
        s.lastSeen = rec.ts;
        s.intervalDays = nextInterval(s);
        state.objectiveStats[oid] = s;
      });
      save();
    },

    recordExam: function (rec) {
      rec.ts = new Date().toISOString();
      state.examSessions.push(rec);
      save();
    },

    setLab: function (id, status) { state.labStatus[id] = status; save(); },
    setLabNotes: function (id, text) { state.labNotes[id] = text; save(); },

    /* Rolling accuracy over the last 5 attempts. null = never attempted. */
    accuracy: function (oid) {
      var s = state.objectiveStats[oid];
      if (!s || !s.recent.length) return null;
      return s.recent.reduce(function (a, b) { return a + b; }, 0) / s.recent.length;
    },

    isDue: function (oid) {
      var s = state.objectiveStats[oid];
      if (!s || !s.lastSeen) return true;
      var days = (Date.now() - new Date(s.lastSeen).getTime()) / 86400000;
      return days >= (s.intervalDays || 1);
    },

    reset: function () { state = blank(); save(); }
  };

  /* Objective-level spacing, not per-question — memorising a finite pool is the failure mode. */
  function nextInterval(s) {
    var acc = s.recent.reduce(function (a, b) { return a + b; }, 0) / s.recent.length;
    var cur = s.intervalDays || 1;
    if (acc >= 0.8) return Math.min(21, Math.round(cur * 1.8) || 2);
    if (acc >= 0.5) return Math.min(21, Math.round(cur * 1.2) || 1);
    return 1;
  }

  AB.store = store;

  /* ------------------------------------------------------------------ theme */

  var toggle = document.getElementById('theme-toggle');
  if (toggle) {
    toggle.addEventListener('click', function () {
      var next = document.documentElement.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
      document.documentElement.setAttribute('data-theme', next);
      try { localStorage.setItem('sc200.theme', next); } catch (e) { /* session-only */ }
    });
  }

  /* ----------------------------------------------------------------- search */

  var STOP = ' the and for are but not you all can with this that from they have been will your what when which their would there about into than them then these some more only also such must each other ';

  function tokenize(s) {
    return (s.toLowerCase().match(/[a-z0-9]+/g) || []).filter(function (w) {
      return w.length >= 3 && STOP.indexOf(' ' + w + ' ') === -1;
    });
  }

  function search(query) {
    var idx = AB.searchIndex;
    if (!idx) return [];
    var toks = tokenize(query);
    if (!toks.length) return [];
    var scores = {};
    toks.forEach(function (tok) {
      // exact token, then prefix matches so partial typing still finds things
      var keys = idx.postings[tok] ? [tok] : Object.keys(idx.postings).filter(function (k) {
        return k.indexOf(tok) === 0;
      }).slice(0, 12);
      keys.forEach(function (k) {
        var penalty = k === tok ? 1 : 0.5;
        idx.postings[k].forEach(function (pair) {
          scores[pair[0]] = (scores[pair[0]] || 0) + pair[1] * penalty;
        });
      });
    });
    return Object.keys(scores)
      .map(function (id) { return { id: id, score: scores[id], doc: idx.docs[id] }; })
      .filter(function (r) { return r.doc; })
      .sort(function (a, b) { return b.score - a.score; })
      .slice(0, 25);
  }

  AB.search = search;

  var input = document.getElementById('q');
  var results = document.getElementById('results');
  if (input && results) {
    var depth = (document.querySelector('link[rel=stylesheet]') || {}).getAttribute
      ? document.querySelector('link[rel=stylesheet]').getAttribute('href').replace('style.css', '')
      : '';
    var timer = null;
    var sel = -1;

    function render(rows) {
      if (!rows.length) {
        results.innerHTML = '<div class="empty-msg">Nothing found.</div>';
      } else {
        results.innerHTML = rows.map(function (r, i) {
          return '<a href="' + depth + r.doc.u + '" data-i="' + i + '">' +
            '<span class="r-title">' + esc(r.doc.t) + '<span class="r-kind">' + r.doc.k + '</span></span>' +
            '<span class="r-snip">' + esc(r.doc.s) + '</span></a>';
        }).join('');
      }
      results.hidden = false;
      sel = -1;
    }

    input.addEventListener('input', function () {
      clearTimeout(timer);
      var v = input.value.trim();
      if (!v) { results.hidden = true; return; }
      timer = setTimeout(function () { render(search(v)); }, 150);
    });

    input.addEventListener('keydown', function (e) {
      var links = results.querySelectorAll('a');
      if (e.key === 'Escape') { results.hidden = true; input.blur(); return; }
      if (!links.length || results.hidden) return;
      if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {
        e.preventDefault();
        sel = Math.max(0, Math.min(links.length - 1, sel + (e.key === 'ArrowDown' ? 1 : -1)));
        links.forEach(function (a) { a.classList.remove('sel'); });
        links[sel].classList.add('sel');
        links[sel].scrollIntoView({ block: 'nearest' });
      } else if (e.key === 'Enter' && sel >= 0) {
        e.preventDefault();
        links[sel].click();
      }
    });

    document.addEventListener('click', function (e) {
      if (!results.contains(e.target) && e.target !== input) results.hidden = true;
    });

    // "/" focuses search, the way every docs site works
    document.addEventListener('keydown', function (e) {
      if (e.key === '/' && document.activeElement !== input &&
          ['INPUT', 'TEXTAREA', 'SELECT'].indexOf(document.activeElement.tagName) === -1) {
        e.preventDefault();
        input.focus();
      }
    });
  }

  /* ---------------------------------------------------------- export/import */

  var exportBtn = document.getElementById('export-progress');
  if (exportBtn) {
    exportBtn.addEventListener('click', function () {
      var blob = new Blob([JSON.stringify(state, null, 2)], { type: 'application/json' });
      var a = document.createElement('a');
      a.href = URL.createObjectURL(blob);
      a.download = 'sc200-progress-' + new Date().toISOString().slice(0, 10) + '.json';
      a.click();
      setTimeout(function () { URL.revokeObjectURL(a.href); }, 1000);
      toast('Exported. Save it to progress/progress-export.json so the build picks it up.');
    });
  }

  var importInput = document.getElementById('import-progress');
  if (importInput) {
    importInput.addEventListener('change', function () {
      var file = importInput.files && importInput.files[0];
      if (!file) return;
      var reader = new FileReader();
      reader.onload = function () {
        try {
          var incoming = JSON.parse(String(reader.result));
          state = Object.assign(blank(), incoming);
          save();
          toast('Progress imported.');
          setTimeout(function () { location.reload(); }, 600);
        } catch (e) {
          toast('That file is not valid progress JSON.');
        }
      };
      reader.readAsText(file);
    });
  }

  /* ------------------------------------------------------------- utilities */

  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"]/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c];
    });
  }

  function toast(msg) {
    var el = document.createElement('div');
    el.className = 'toast';
    el.textContent = msg;
    document.body.appendChild(el);
    setTimeout(function () { el.remove(); }, 4200);
  }

  function qs(name) {
    var m = new RegExp('[?&]' + name + '=([^&]*)').exec(location.search);
    return m ? decodeURIComponent(m[1]) : null;
  }

  AB.util = { esc: esc, toast: toast, qs: qs };

  /* copy buttons on code blocks */
  document.addEventListener('click', function (e) {
    if (!e.target.classList.contains('copy-btn')) return;
    var code = e.target.parentElement.querySelector('code');
    if (!code) return;
    var text = code.textContent;
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(function () { flash(e.target); }, function () { legacy(text, e.target); });
    } else {
      legacy(text, e.target);
    }
  });

  function legacy(text, btn) {
    // Clipboard API needs a secure context; file:// often is not one.
    var ta = document.createElement('textarea');
    ta.value = text;
    ta.style.position = 'fixed';
    ta.style.opacity = '0';
    document.body.appendChild(ta);
    ta.select();
    try { document.execCommand('copy'); flash(btn); } catch (e) { toast('Copy failed — select manually.'); }
    ta.remove();
  }

  function flash(btn) {
    var old = btn.textContent;
    btn.textContent = 'copied';
    setTimeout(function () { btn.textContent = old; }, 1200);
  }

  if (memoryOnly) {
    toast('This browser blocks storage on file:// — progress lives in memory only this session. Export before closing.');
  }
})();

/* Arrow-key paging between objective pages. Skipped while typing in a field so it never
   fights the search box or a lab notes textarea. */
(function () {
  'use strict';
  document.addEventListener('keydown', function (e) {
    if (e.metaKey || e.ctrlKey || e.altKey) return;
    var t = document.activeElement;
    if (t && ['INPUT', 'TEXTAREA', 'SELECT'].indexOf(t.tagName) !== -1) return;
    var dir = e.key === 'ArrowLeft' ? 'prev' : e.key === 'ArrowRight' ? 'next' : null;
    if (!dir) return;
    var link = document.querySelector('.pager-slot[data-pager="' + dir + '"]');
    if (link) { e.preventDefault(); location.href = link.getAttribute('href'); }
  });
})();
