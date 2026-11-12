/* SC-200 quiz + mock exam engine.

   Scoring mirrors Microsoft's documented rules:
     multiple_response      -> all-or-nothing, exact set match
     drag_and_drop          -> +1 per correctly filled target
     build_list             -> +1 per correct position
     hot_area/active_screen -> +1 per correct statement/control
     problem_solution_set   -> three proposals scored independently, logged as three records
     case_study             -> each linked question scored by its own rule
   No negative marking anywhere. */

(function () {
  'use strict';

  var AB = window.SC200;
  if (!AB || !AB.data) return;
  var esc = AB.util.esc, qs = AB.util.qs, toast = AB.util.toast;

  var ALL = (AB.data.questions || []).slice();
  var OBJ = {};
  (AB.data.objectives || []).forEach(function (o) { OBJ[o.id] = o; });
  var DOMAIN_WEIGHT = {};
  (AB.data.domains || []).forEach(function (d) { DOMAIN_WEIGHT[d.id] = d.weight || 0; });

  var byId = {};
  ALL.forEach(function (q) { byId[q.id] = q; });

  /* Questions that belong to a case study are never served standalone —
     they only appear underneath their parent's background. */
  var linked = {};
  ALL.forEach(function (q) {
    if (q.format === 'case_study') (q.linked_question_ids || []).forEach(function (id) { linked[id] = q.id; });
  });
  var STANDALONE = ALL.filter(function (q) { return !linked[q.id]; });

  /* ------------------------------------------------------------- rendering */

  var RENDER = {};
  var SCORE = {};

  function optionList(q, name, type) {
    return '<ul class="options">' + (q.options || []).map(function (o) {
      return '<li><label class="opt" data-opt="' + esc(o.id) + '">' +
        '<input type="' + type + '" name="' + name + '" value="' + esc(o.id) + '">' +
        '<span>' + esc(o.text) + '</span></label></li>';
    }).join('') + '</ul>';
  }

  RENDER.multiple_choice = function (q, key) {
    return '<div class="q-stem">' + esc(q.stem) + '</div>' + optionList(q, key, 'radio');
  };

  RENDER.multiple_response = function (q, key) {
    var n = q.select_count || (q.answer || []).length;
    return '<div class="q-stem">' + esc(q.stem) + '</div>' +
      '<div class="q-hint">Select ' + n + '. Scored all-or-nothing — a near miss is worth zero.</div>' +
      optionList(q, key, 'checkbox');
  };

  RENDER.drag_and_drop = function (q, key) {
    var pool = (q.drag_items || []).map(function (it) {
      return '<div class="dnd-item" draggable="true" data-item="' + esc(it.id) + '">' + esc(it.text) + '</div>';
    }).join('');
    var targets = (q.targets || []).map(function (t) {
      return '<div class="dnd-target" data-target="' + esc(t.id) + '">' +
        '<span class="lbl">' + esc(t.label) + '</span></div>';
    }).join('');
    return '<div class="q-stem">' + esc(q.stem || '') + '</div>' +
      '<div class="q-hint">Drag each item onto a target. Partial credit per target.</div>' +
      '<div class="dnd"><div class="dnd-pool"><h4>Items</h4>' + pool + '</div>' +
      '<div class="dnd-targets"><h4>Targets</h4>' + targets + '</div></div>';
  };

  RENDER.build_list = function (q, key) {
    var items = shuffle((q.items || []).slice());
    return '<div class="q-stem">' + esc(q.stem || '') + '</div>' +
      '<div class="q-hint">Put these in the correct order. Partial credit per position.</div>' +
      '<ol class="buildlist">' + items.map(function (it) {
        return '<li data-item="' + esc(it.id) + '"><span class="move">' +
          '<button type="button" data-dir="-1">▲</button>' +
          '<button type="button" data-dir="1">▼</button></span>' +
          '<span>' + esc(it.text) + '</span></li>';
      }).join('') + '</ol>';
  };

  RENDER.hot_area = function (q, key) {
    var rows = (q.statements || []).map(function (s) {
      return '<tr><td>' + esc(s.text) + '</td>' +
        '<td class="nowrap"><label><input type="radio" name="' + key + '-' + esc(s.id) + '" value="yes"> Yes</label></td>' +
        '<td class="nowrap"><label><input type="radio" name="' + key + '-' + esc(s.id) + '" value="no"> No</label></td></tr>';
    }).join('');
    if (rows) {
      return '<div class="q-stem">' + esc(q.stem || '') + '</div>' +
        '<div class="q-hint">Partial credit per statement.</div>' +
        '<div class="tablewrap"><table><thead><tr><th>Statement</th><th>Yes</th><th>No</th></tr></thead>' +
        '<tbody>' + rows + '</tbody></table></div>';
    }
    return RENDER.active_screen(q, key);
  };

  RENDER.active_screen = function (q, key) {
    var controls = q.controls || q.regions || [];
    if (!controls.length) return unsupported(q);
    var rows = controls.map(function (c) {
      var opts = (c.options || ['Yes', 'No']).map(function (v) {
        return '<option value="' + esc(v) + '">' + esc(v) + '</option>';
      }).join('');
      return '<tr><td>' + esc(c.label || c.text || c.id) + '</td>' +
        '<td><select data-control="' + esc(c.id) + '"><option value="">—</option>' + opts + '</select></td></tr>';
    }).join('');
    return '<div class="q-stem">' + esc(q.stem || '') + '</div>' +
      '<div class="q-hint">Set each control. Partial credit per control.</div>' +
      '<div class="tablewrap"><table><thead><tr><th>Setting</th><th>Value</th></tr></thead>' +
      '<tbody>' + rows + '</tbody></table></div>';
  };

  RENDER.problem_solution_set = function (q, key) {
    return '<div class="q-stem">' + esc(q.shared_stem || q.stem || '') + '</div>' +
      '<p><strong>' + esc(q.goal_statement || 'Does this solution meet the goal?') + '</strong></p>' +
      '<div class="q-hint">Each proposal is scored independently. Answering one does not constrain the others.</div>' +
      (q.proposals || []).map(function (p, i) {
        return '<div class="ps-proposal" data-proposal="' + esc(p.id) + '">' +
          '<p><strong>Solution ' + (i + 1) + ':</strong> ' + esc(p.solution_text) + '</p>' +
          '<div class="yn">' +
          '<label><input type="radio" name="' + key + '-' + esc(p.id) + '" value="yes"> Yes, meets the goal</label>' +
          '<label><input type="radio" name="' + key + '-' + esc(p.id) + '" value="no"> No</label>' +
          '</div></div>';
      }).join('');
  };

  RENDER.case_study = function (q, key) {
    var exhibits = (q.exhibits || []).map(function (ex) {
      return '<div class="tablewrap">' + mdTable(ex.content_md || '') + '</div>';
    }).join('');
    var subs = (q.linked_question_ids || []).map(function (id, i) {
      var sub = byId[id];
      if (!sub) return '<p class="note">Missing linked question <code>' + esc(id) + '</code>.</p>';
      var r = RENDER[sub.format];
      return '<div class="sub-question" data-sub="' + esc(id) + '">' +
        '<h4>Question ' + (i + 1) + ' of ' + q.linked_question_ids.length + '</h4>' +
        (r ? r(sub, key + '-' + id) : unsupported(sub)) + '</div>';
    }).join('');
    return '<div class="case-bg"><h3>Case study background</h3><p>' +
      esc(q.background || '').replace(/\n\n/g, '</p><p>') + '</p>' + exhibits + '</div>' + subs;
  };

  function unsupported(q) {
    return '<div class="empty"><p><strong>Format <code>' + esc(q.format) +
      '</code> has no renderer yet.</strong> The question data is valid — only the UI is missing. ' +
      'This question is skipped rather than scored.</p></div>';
  }

  /* Minimal pipe-table renderer for case-study exhibits (build.py handles the rest). */
  function mdTable(md) {
    var lines = md.trim().split('\n').filter(function (l) { return l.trim().indexOf('|') === 0; });
    if (lines.length < 2) return '<pre>' + esc(md) + '</pre>';
    var cells = function (l) { return l.trim().replace(/^\||\|$/g, '').split('|').map(function (c) { return c.trim(); }); };
    var head = cells(lines[0]);
    var body = lines.slice(2).map(function (l) {
      return '<tr>' + cells(l).map(function (c) { return '<td>' + esc(c) + '</td>'; }).join('') + '</tr>';
    }).join('');
    return '<table><thead><tr>' + head.map(function (c) { return '<th>' + esc(c) + '</th>'; }).join('') +
      '</tr></thead><tbody>' + body + '</tbody></table>';
  }

  /* --------------------------------------------------------------- scoring */

  SCORE.multiple_choice = function (q, root, key) {
    var picked = root.querySelector('input[name="' + key + '"]:checked');
    var val = picked ? picked.value : null;
    var ok = (q.answer || []).indexOf(val) !== -1;
    return { score: ok ? 1 : 0, max: 1, selected: val ? [val] : [] };
  };

  SCORE.multiple_response = function (q, root, key) {
    var picked = [].slice.call(root.querySelectorAll('input[name="' + key + '"]:checked'))
      .map(function (i) { return i.value; }).sort();
    var want = (q.answer || []).slice().sort();
    var exact = picked.length === want.length && picked.every(function (v, i) { return v === want[i]; });
    return { score: exact ? 1 : 0, max: 1, selected: picked };
  };

  SCORE.drag_and_drop = function (q, root, key) {
    var got = 0, sel = {};
    (q.targets || []).forEach(function (t) {
      var cell = root.querySelector('[data-target="' + t.id + '"] .dnd-item');
      var placed = cell ? cell.getAttribute('data-item') : null;
      sel[t.id] = placed;
      if (placed === t.correct_item) got++;
    });
    return { score: got, max: (q.targets || []).length, selected: sel };
  };

  SCORE.build_list = function (q, root, key) {
    var order = [].slice.call(root.querySelectorAll('.buildlist li'))
      .map(function (li) { return li.getAttribute('data-item'); });
    var want = q.correct_order || [];
    var got = want.reduce(function (a, id, i) { return a + (order[i] === id ? 1 : 0); }, 0);
    return { score: got, max: want.length, selected: order };
  };

  SCORE.hot_area = function (q, root, key) {
    if (q.statements && q.statements.length) {
      var got = 0, sel = {};
      q.statements.forEach(function (s) {
        var picked = root.querySelector('input[name="' + key + '-' + s.id + '"]:checked');
        var val = picked ? picked.value : null;
        sel[s.id] = val;
        if (val && (val === 'yes') === !!s.correct) got++;
      });
      return { score: got, max: q.statements.length, selected: sel };
    }
    return SCORE.active_screen(q, root, key);
  };

  SCORE.active_screen = function (q, root, key) {
    var controls = q.controls || q.regions || [];
    var got = 0, sel = {};
    controls.forEach(function (c) {
      var el = root.querySelector('[data-control="' + c.id + '"]');
      var val = el ? el.value : '';
      sel[c.id] = val;
      if (val && val === c.correct) got++;
    });
    return { score: got, max: controls.length, selected: sel };
  };

  SCORE.problem_solution_set = function (q, root, key) {
    var got = 0, sel = {};
    (q.proposals || []).forEach(function (p) {
      var picked = root.querySelector('input[name="' + key + '-' + p.id + '"]:checked');
      var val = picked ? picked.value : null;
      sel[p.id] = val;
      if (val && (val === 'yes') === !!p.meets_goal) got++;
    });
    return { score: got, max: (q.proposals || []).length, selected: sel, perProposal: true };
  };

  SCORE.case_study = function (q, root, key) {
    var got = 0, max = 0, parts = [];
    (q.linked_question_ids || []).forEach(function (id) {
      var sub = byId[id];
      if (!sub || !SCORE[sub.format]) return;
      var scope = root.querySelector('[data-sub="' + id + '"]');
      if (!scope) return;
      var r = SCORE[sub.format](sub, scope, key + '-' + id);
      got += r.score; max += r.max;
      parts.push({ id: id, sub: sub, result: r });
    });
    return { score: got, max: max, selected: {}, parts: parts };
  };

  /* -------------------------------------------------------------- feedback */

  function feedback(q, result) {
    var pass = result.max > 0 && result.score === result.max;
    var partial = result.score > 0 && result.score < result.max;
    var verdict = pass ? 'Correct' : partial ? 'Partly correct' : 'Incorrect';
    var cls = pass ? 'pass' : partial ? '' : 'fail';

    var detail = '';
    if (q.options) {
      detail = '<ul class="options">' + q.options.map(function (o) {
        var chosen = (result.selected || []).indexOf(o.id) !== -1;
        var c = o.correct ? 'correct' : chosen ? 'wrong' : '';
        return '<li><div class="opt ' + c + '"><span>' + (o.correct ? '✓ ' : chosen ? '✗ ' : '') +
          esc(o.text) + (o.explanation ? '<span class="why">' + esc(o.explanation) + '</span>' : '') +
          '</span></div></li>';
      }).join('') + '</ul>';
    } else if (q.proposals) {
      detail = q.proposals.map(function (p) {
        var given = (result.selected || {})[p.id];
        var right = given && (given === 'yes') === !!p.meets_goal;
        return '<div class="opt ' + (right ? 'correct' : 'wrong') + '"><span>' +
          (p.meets_goal ? 'Yes — meets the goal. ' : 'No — does not meet the goal. ') +
          '<span class="why">' + esc(p.explanation || '') + '</span></span></div>';
      }).join('');
    } else if (q.targets) {
      detail = '<ul class="options">' + q.targets.map(function (t) {
        var placed = (result.selected || {})[t.id];
        var item = (q.drag_items || []).filter(function (d) { return d.id === t.correct_item; })[0];
        return '<li><div class="opt ' + (placed === t.correct_item ? 'correct' : 'wrong') + '"><span>' +
          esc(t.label) + ' → <strong>' + esc(item ? item.text : t.correct_item) + '</strong>' +
          (t.explanation ? '<span class="why">' + esc(t.explanation) + '</span>' : '') + '</span></div></li>';
      }).join('') + '</ul>';
    } else if (q.correct_order) {
      var lookup = {};
      (q.items || []).forEach(function (it) { lookup[it.id] = it.text; });
      detail = '<ol>' + q.correct_order.map(function (id) {
        return '<li>' + esc(lookup[id] || id) + '</li>';
      }).join('') + '</ol>';
    } else if (q.statements) {
      detail = '<ul class="options">' + q.statements.map(function (s) {
        var given = (result.selected || {})[s.id];
        var right = given && (given === 'yes') === !!s.correct;
        return '<li><div class="opt ' + (right ? 'correct' : 'wrong') + '"><span>' +
          esc(s.text) + ' → <strong>' + (s.correct ? 'Yes' : 'No') + '</strong>' +
          (s.explanation ? '<span class="why">' + esc(s.explanation) + '</span>' : '') + '</span></div></li>';
      }).join('') + '</ul>';
    }

    var cites = (q.source_urls || []).map(function (u) {
      return '<a href="' + esc(u) + '">' + esc(u) + '</a>';
    }).join('<br>');

    var objs = (q.objective_ids || []).map(function (id) {
      return '<a href="objective/' + id + '.html"><code>' + id + '</code></a>';
    }).join(' ');

    return '<div class="feedback"><span class="verdict ' + cls + '">' + verdict + '</span> — ' +
      result.score + '/' + result.max +
      (q.verified ? '' : ' <span class="unverified">unverified question</span>') +
      (q.explanation ? '<p>' + esc(q.explanation) + '</p>' : '') + detail +
      '<div class="cite">Objectives: ' + objs + (cites ? '<br>Source: ' + cites : '') + '</div></div>';
  }

  /* -------------------------------------------------------------- helpers */

  function shuffle(a) {
    for (var i = a.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1));
      var t = a[i]; a[i] = a[j]; a[j] = t;
    }
    return a;
  }

  function wireInteractions(root) {
    // build list reordering
    root.querySelectorAll('.buildlist .move button').forEach(function (btn) {
      btn.addEventListener('click', function () {
        var li = btn.closest('li');
        var dir = parseInt(btn.getAttribute('data-dir'), 10);
        var sib = dir < 0 ? li.previousElementSibling : li.nextElementSibling;
        if (!sib) return;
        if (dir < 0) li.parentNode.insertBefore(li, sib);
        else li.parentNode.insertBefore(sib, li);
      });
    });

    // drag and drop
    var dragged = null;
    root.querySelectorAll('.dnd-item').forEach(function (item) {
      item.addEventListener('dragstart', function () { dragged = item; });
      // click-to-place fallback: touch devices and anyone who dislikes dragging
      item.addEventListener('click', function () {
        dragged = dragged === item ? null : item;
        root.querySelectorAll('.dnd-item').forEach(function (i) { i.style.outline = ''; });
        if (dragged) item.style.outline = '2px solid var(--accent)';
      });
    });
    root.querySelectorAll('.dnd-target').forEach(function (t) {
      t.addEventListener('dragover', function (e) { e.preventDefault(); t.classList.add('over'); });
      t.addEventListener('dragleave', function () { t.classList.remove('over'); });
      t.addEventListener('drop', function (e) { e.preventDefault(); t.classList.remove('over'); place(t); });
      t.addEventListener('click', function () { place(t); });
    });
    function place(t) {
      if (!dragged) return;
      var existing = t.querySelector('.dnd-item');
      var pool = root.querySelector('.dnd-pool');
      if (existing) pool.appendChild(existing);
      t.appendChild(dragged);
      dragged.style.outline = '';
      dragged = null;
    }
  }

  /* --------------------------------------------------------------- session */

  function Session(items, opts) {
    this.items = items;
    this.opts = opts || {};
    this.idx = 0;
    this.answers = {};
    this.results = {};
  }

  Session.prototype.renderCurrent = function (host) {
    var q = this.items[this.idx];
    var key = 'q' + this.idx;
    var r = RENDER[q.format];
    var objs = (q.objective_ids || []).join(', ');
    var body = r ? r(q, key) : unsupported(q);

    host.innerHTML =
      '<div class="question" id="qbox">' +
      '<div class="q-head"><span class="fmt">' + esc(q.format.replace(/_/g, ' ')) + '</span>' +
      '<span>' + (this.idx + 1) + ' / ' + this.items.length + '</span>' +
      '<span>' + esc(objs) + (q.difficulty ? ' · difficulty ' + q.difficulty : '') + '</span></div>' +
      body + '</div>' +
      '<div class="qnav">' +
      (this.opts.mock ? '<button class="btn secondary" id="prev" type="button">Back</button>' : '') +
      '<button class="btn" id="submit" type="button">' +
      (this.opts.mock ? (this.idx === this.items.length - 1 ? 'Finish exam' : 'Next') : 'Check answer') +
      '</button><span class="spacer"></span>' +
      (this.opts.mock ? '<button class="btn secondary" id="finish" type="button">Finish now</button>' : '') +
      '</div>';

    wireInteractions(host);
    this.restore(host, key);

    var self = this;
    var submit = host.querySelector('#submit');
    if (submit) submit.addEventListener('click', function () { self.onSubmit(host); });
    var prev = host.querySelector('#prev');
    if (prev) prev.addEventListener('click', function () {
      self.capture(host);
      if (self.idx > 0) { self.idx--; self.renderCurrent(host); }
    });
    var fin = host.querySelector('#finish');
    if (fin) fin.addEventListener('click', function () { self.capture(host); self.finish(); });
  };

  /* Mock mode allows going back, so answers must survive a re-render. */
  Session.prototype.capture = function (host) {
    var q = this.items[this.idx];
    var key = 'q' + this.idx;
    var scorer = SCORE[q.format];
    if (!scorer) return;
    this.answers[this.idx] = scorer(q, host.querySelector('#qbox'), key);
  };

  Session.prototype.restore = function (host, key) {
    var saved = this.answers[this.idx];
    if (!saved) return;
    var box = host.querySelector('#qbox');
    var sel = saved.selected;
    if (Array.isArray(sel)) {
      sel.forEach(function (v) {
        var el = box.querySelector('input[value="' + v + '"]');
        if (el) el.checked = true;
      });
    } else if (sel && typeof sel === 'object') {
      Object.keys(sel).forEach(function (k) {
        var el = box.querySelector('[name="' + key + '-' + k + '"][value="' + sel[k] + '"]') ||
                 box.querySelector('[data-control="' + k + '"]');
        if (el && el.tagName === 'SELECT') el.value = sel[k] || '';
        else if (el) el.checked = true;
      });
    }
  };

  Session.prototype.onSubmit = function (host) {
    var q = this.items[this.idx];
    var key = 'q' + this.idx;
    var scorer = SCORE[q.format];

    if (!scorer) { this.next(host); return; }

    var result = scorer(q, host.querySelector('#qbox'), key);
    this.answers[this.idx] = result;

    if (this.opts.mock) {
      this.results[q.id] = { q: q, result: result };
      this.next(host);
      return;
    }

    var box = host.querySelector('#qbox');
    if (box.querySelector('.feedback')) { this.next(host); return; }

    box.insertAdjacentHTML('beforeend', feedback(q, result));
    this.results[q.id] = { q: q, result: result };
    record(q, result);
    box.querySelectorAll('input, select, button.move').forEach(function (i) { i.disabled = true; });
    host.querySelector('#submit').textContent =
      this.idx === this.items.length - 1 ? 'See results' : 'Next question';
  };

  Session.prototype.next = function (host) {
    if (this.idx < this.items.length - 1) { this.idx++; this.renderCurrent(host); }
    else this.finish();
  };

  Session.prototype.finish = function () {
    if (this.opts.mock) {
      var self = this;
      this.items.forEach(function (q, i) {
        var r = self.answers[i];
        if (r) { self.results[q.id] = { q: q, result: r }; record(q, r); }
      });
    }
    if (this.opts.onFinish) this.opts.onFinish(this.results);
  };

  /* Attempt records. Problem/solution sets log one record per proposal so weak-area
     tracking sees three independent data points, matching how the real exam scores them. */
  function record(q, result) {
    if (result.parts) {
      result.parts.forEach(function (p) { record(p.sub, p.result); });
      return;
    }
    if (result.perProposal && q.proposals) {
      q.proposals.forEach(function (p) {
        var given = (result.selected || {})[p.id];
        var right = given && (given === 'yes') === !!p.meets_goal;
        AB.store.recordAttempt({
          question_id: q.id + ':' + p.id, objective_ids: q.objective_ids,
          format: q.format, score: right ? 1 : 0, max_score: 1, selected: given
        });
      });
      return;
    }
    AB.store.recordAttempt({
      question_id: q.id, objective_ids: q.objective_ids, format: q.format,
      score: result.score, max_score: result.max, selected: result.selected
    });
  }

  /* --------------------------------------------------------------- results */

  function scorecard(results, opts) {
    var got = 0, max = 0;
    var perDomain = {};
    Object.keys(results).forEach(function (id) {
      var r = results[id];
      got += r.result.score; max += r.result.max;
      (r.q.objective_ids || []).forEach(function (oid) {
        var dom = oid.split('.')[0];
        var d = perDomain[dom] = perDomain[dom] || { got: 0, max: 0 };
        d.got += r.result.score; d.max += r.result.max;
      });
    });
    var pct = max ? got / max : 0;
    var scaled = Math.round(pct * 1000);
    var pass = scaled >= 700;

    var rows = Object.keys(perDomain).sort().map(function (dom) {
      var d = perDomain[dom];
      var p = d.max ? d.got / d.max : 0;
      return '<tr><td><a href="domain/' + dom + '.html">' + dom + '</a></td>' +
        '<td>' + d.got + '/' + d.max + '</td><td>' + Math.round(p * 100) + '%</td></tr>';
    }).join('');

    var wrong = Object.keys(results).filter(function (id) {
      return results[id].result.score < results[id].result.max;
    });

    var review = wrong.length
      ? '<h2>Review</h2>' + wrong.map(function (id) {
          var r = results[id];
          return '<div class="question"><div class="q-head"><span class="fmt">' +
            esc(r.q.format.replace(/_/g, ' ')) + '</span><span>' + esc((r.q.objective_ids || []).join(', ')) +
            '</span></div><div class="q-stem">' +
            esc(r.q.stem || r.q.shared_stem || r.q.background || '') + '</div>' +
            feedback(r.q, r.result) + '</div>';
        }).join('')
      : '<p class="note">Nothing missed.</p>';

    return '<div class="scorecard"><div class="big ' + (pass ? 'pass' : 'fail') + '">' + scaled + '</div>' +
      '<p>' + got + ' of ' + max + ' points · ' + Math.round(pct * 100) + '%' +
      (opts && opts.mock ? ' · pass mark 700' : '') + '</p>' +
      (opts && opts.mock
        ? '<p class="note">This 1–1000 number is a <strong>linear approximation</strong>. Microsoft\'s real ' +
          'algorithm is undisclosed and weights questions by difficulty. Track the trend across attempts, ' +
          'not the absolute value.</p>'
        : '') +
      '</div><div class="tablewrap"><table><thead><tr><th>Domain</th><th>Points</th><th>%</th></tr>' +
      '</thead><tbody>' + rows + '</tbody></table></div>' + review +
      '<div class="qnav"><a class="btn" href="' + location.pathname.split('/').pop() + '">Again</a>' +
      '<a class="btn secondary" href="index.html">Dashboard</a></div>';
  }

  /* ------------------------------------------------------------- practice */

  var setup = document.getElementById('quiz-setup');
  if (setup) {
    var scope = document.getElementById('scope');
    (AB.data.domains || []).forEach(function (d) {
      var og = document.createElement('optgroup');
      og.label = d.id + ' — ' + d.title;
      (AB.data.objectives || []).filter(function (o) { return o.domain === d.id; }).forEach(function (o) {
        var opt = document.createElement('option');
        opt.value = o.id;
        opt.textContent = o.id + ' — ' + o.title;
        og.appendChild(opt);
      });
      var domOpt = document.createElement('option');
      domOpt.value = d.id;
      domOpt.textContent = 'All of ' + d.id;
      scope.appendChild(domOpt);
      scope.appendChild(og);
    });

    var preset = qs('objective') || qs('domain');
    if (preset) scope.value = preset;

    document.getElementById('start').addEventListener('click', function () {
      var want = scope.value;
      var verifiedOnly = document.getElementById('verified-only').checked;
      var weakFirst = document.getElementById('weak-first').checked;
      var n = parseInt(document.getElementById('count').value, 10) || 10;

      var pool = STANDALONE.filter(function (q) {
        if (verifiedOnly && !q.verified) return false;
        if (want === 'all') return true;
        return (q.objective_ids || []).some(function (oid) {
          return oid === want || oid.indexOf(want + '.') === 0;
        });
      });

      if (!pool.length) { toast('No questions match that scope yet.'); return; }

      if (weakFirst) {
        pool.sort(function (a, b) { return weakness(b) - weakness(a) || Math.random() - 0.5; });
      } else {
        shuffle(pool);
      }

      run(pool.slice(0, n), { mock: false });
    });

    var qid = qs('q');
    if (qid && byId[qid]) run([byId[qid]], { mock: false });
  }

  function weakness(q) {
    var worst = 0;
    (q.objective_ids || []).forEach(function (oid) {
      var acc = AB.store.accuracy(oid);
      var gap = acc === null ? 0.7 : 1 - acc;
      if (gap > worst) worst = gap;
    });
    return worst;
  }

  function run(items, opts) {
    var setupEl = document.getElementById('quiz-setup');
    var host = document.getElementById('quiz-runner');
    var out = document.getElementById('quiz-results');
    if (setupEl) setupEl.hidden = true;
    host.hidden = false;
    var s = new Session(items, {
      mock: opts.mock,
      onFinish: function (results) {
        host.hidden = true;
        out.hidden = false;
        out.innerHTML = scorecard(results, opts);
        window.scrollTo(0, 0);
      }
    });
    s.renderCurrent(host);
  }

  /* ------------------------------------------------------------ mock exam */

  var mockSetup = document.getElementById('mock-setup');
  if (mockSetup) {
    document.getElementById('start-mock').addEventListener('click', function () {
      var items = sampleMock();
      if (items.length < 10) {
        toast('Only ' + items.length + ' questions available — build the bank up before mocking.');
        if (!items.length) return;
      }
      startMock(items);
    });
  }

  /* Weighted sampling. Case studies and problem/solution sets are single atomic units,
     which is exactly why a real mock lands anywhere in 45–55 rather than a fixed count. */
  function sampleMock() {
    var target = 50;
    var picked = [];
    (AB.data.domains || []).forEach(function (d) {
      var want = Math.round(target * (d.weight || 0));
      var pool = shuffle(STANDALONE.filter(function (q) {
        return (q.objective_ids || []).some(function (oid) { return oid.indexOf(d.id + '.') === 0; });
      }));
      picked = picked.concat(pool.slice(0, want));
    });
    return shuffle(picked);
  }

  function startMock(items) {
    var host = document.getElementById('mock-body');
    var runner = document.getElementById('mock-runner');
    var out = document.getElementById('mock-results');
    var timerEl = document.getElementById('mock-timer');
    document.getElementById('mock-setup').hidden = true;
    runner.hidden = false;

    var KEYEND = 'sc200.mock.end';
    var end;
    try {
      var saved = localStorage.getItem(KEYEND);
      end = saved && Number(saved) > Date.now() ? Number(saved) : Date.now() + 100 * 60 * 1000;
      localStorage.setItem(KEYEND, String(end));
    } catch (e) {
      end = Date.now() + 100 * 60 * 1000;
    }

    var session = new Session(items, {
      mock: true,
      onFinish: function (results) {
        clearInterval(tick);
        try { localStorage.removeItem(KEYEND); } catch (e) {}
        runner.hidden = true;
        out.hidden = false;
        var got = 0, max = 0;
        Object.keys(results).forEach(function (k) { got += results[k].result.score; max += results[k].result.max; });
        AB.store.recordExam({
          mode: 'mock_exam', question_count: items.length,
          scaled_score: max ? Math.round((got / max) * 1000) : 0
        });
        out.innerHTML = scorecard(results, { mock: true });
        window.scrollTo(0, 0);
      }
    });

    function paint() {
      var left = Math.max(0, end - Date.now());
      var m = Math.floor(left / 60000), s = Math.floor((left % 60000) / 1000);
      timerEl.innerHTML = '<span>' + m + ':' + (s < 10 ? '0' : '') + s + '</span>' +
        '<span class="sub">' + items.length + ' questions · no feedback until you finish</span>';
      timerEl.classList.toggle('low', left < 10 * 60 * 1000);
      if (left <= 0) { clearInterval(tick); session.capture(host); session.finish(); }
    }
    var tick = setInterval(paint, 1000);
    paint();

    session.renderCurrent(host);
  }
})();
