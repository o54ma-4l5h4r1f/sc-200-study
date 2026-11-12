/* Dashboard — overlays recorded progress onto the statically-built objective tree. */

(function () {
  'use strict';

  var AB = window.SC200;
  if (!AB || !AB.data) return;
  var store = AB.store;
  var esc = AB.util.esc;

  var objectives = AB.data.objectives || [];
  var domainWeight = {};
  (AB.data.domains || []).forEach(function (d) { domainWeight[d.id] = d.weight || 0; });

  /* per-objective accuracy chips */
  objectives.forEach(function (o) {
    var el = document.querySelector('[data-acc-for="' + o.id + '"]');
    if (!el) return;
    var acc = store.accuracy(o.id);
    if (acc === null) { el.textContent = ''; return; }
    el.textContent = Math.round(acc * 100) + '%';
    el.classList.add(acc < 0.5 ? 'weak' : acc >= 0.8 ? 'strong' : '');
    el.title = 'Rolling accuracy over your last 5 attempts';
  });

  /* readiness: domain-weighted mean accuracy, penalised for objectives never attempted.
     Deliberately conservative — an untouched objective counts as zero, not as unknown. */
  var byDomain = {};
  objectives.forEach(function (o) {
    (byDomain[o.domain] = byDomain[o.domain] || []).push(o);
  });

  var weighted = 0, weightSum = 0;
  Object.keys(byDomain).forEach(function (dom) {
    var list = byDomain[dom];
    var sum = list.reduce(function (a, o) { return a + (store.accuracy(o.id) || 0); }, 0);
    var w = domainWeight[dom] || 0;
    weighted += (sum / list.length) * w;
    weightSum += w;
  });

  var readiness = weightSum ? weighted / weightSum : 0;
  var el = document.getElementById('readiness');
  var bar = document.getElementById('readiness-bar');
  if (el) {
    var attempted = objectives.filter(function (o) { return store.accuracy(o.id) !== null; }).length;
    el.textContent = attempted ? Math.round(readiness * 100) + '%' : '—';
    el.title = attempted + ' of ' + objectives.length + ' objectives attempted';
  }
  if (bar) bar.style.width = (readiness * 100).toFixed(1) + '%';

  /* what to study next: weight x weakness x overdue, plus never-touched high-risk items */
  var ranked = objectives.map(function (o) {
    var acc = store.accuracy(o.id);
    var gap = acc === null ? (o.risk ? 0.9 : 0.6) : 1 - acc;
    var due = store.isDue(o.id) ? 1 : 0.35;
    return { o: o, score: (domainWeight[o.domain] || 0) * gap * due * (o.risk ? 1.3 : 1), acc: acc };
  }).sort(function (a, b) { return b.score - a.score; });

  var weak = ranked.filter(function (r) { return r.acc !== null && r.acc < 0.6; }).slice(0, 6);
  var box = document.getElementById('weak-areas');
  if (box && weak.length) {
    box.innerHTML = '<h3>Review these first</h3><ul>' + weak.map(function (r) {
      return '<li><a href="objective/' + r.o.id + '.html"><code>' + r.o.id + '</code> ' +
        esc(r.o.title) + '</a> — ' + Math.round(r.acc * 100) + '% ' +
        '<a href="quiz.html?objective=' + r.o.id + '">practice</a></li>';
    }).join('') + '</ul>';
  }
})();
