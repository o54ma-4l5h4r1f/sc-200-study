/* Lab tracker — status radios and per-lab notes, persisted through the shared store. */

(function () {
  'use strict';

  var AB = window.SC200;
  if (!AB || !AB.store) return;
  var state = AB.store.get();

  document.querySelectorAll('.lab-status').forEach(function (group) {
    var id = group.getAttribute('data-lab');
    var current = state.labStatus[id] || 'todo';
    group.querySelectorAll('input[type=radio]').forEach(function (radio) {
      if (radio.value === current) radio.checked = true;
      radio.addEventListener('change', function () {
        AB.store.setLab(id, radio.value);
        group.closest('.lab').style.opacity = radio.value === 'done' ? '0.62' : '1';
      });
    });
    if (current === 'done') group.closest('.lab').style.opacity = '0.62';
  });

  document.querySelectorAll('.lab-notes').forEach(function (ta) {
    var id = ta.getAttribute('data-lab');
    ta.value = state.labNotes[id] || '';
    var timer = null;
    ta.addEventListener('input', function () {
      clearTimeout(timer);
      timer = setTimeout(function () { AB.store.setLabNotes(id, ta.value); }, 500);
    });
  });
})();
