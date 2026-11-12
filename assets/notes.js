/* SC-200 page annotations — click to drop a sticky note on any study page.
 * Notes live in localStorage (per page, keyed by pathname) and export/import as JSON
 * so they survive a cleared browser. file:// localStorage is unreliable, so every
 * read/write is guarded and the user is nudged to Export to keep a real file.
 * Vanilla, classic script (no modules) to satisfy the offline/file:// constraints. */
(function () {
  "use strict";
  var KEY = "sc200.notes";
  var page = location.pathname.split("/").slice(-2).join("/"); // stable-ish per-page key
  var addMode = false;
  var store = load();
  // Served by serve.py on localhost → notes persist to a real file on disk.
  // file:// (double-click) or a hosted site (GitHub Pages) → localStorage + Export/Import.
  var SERVER = /^https?:$/.test(location.protocol) && /^(localhost|127\.0\.0\.1|\[::1\])$/.test(location.hostname);

  function load() { try { return JSON.parse(localStorage.getItem(KEY) || "{}"); } catch (e) { return {}; } }
  var saveTimer = null;
  function save() {
    try { localStorage.setItem(KEY, JSON.stringify(store)); } catch (e) {}
    if (SERVER) {
      clearTimeout(saveTimer);
      saveTimer = setTimeout(function () {
        try { fetch("/__notes", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(store) }); } catch (e) {}
      }, 250);
    }
  }
  function list() { return store[page] || (store[page] = []); }
  function total() { var n = 0; for (var k in store) if (store.hasOwnProperty(k)) n += store[k].length; return n; }
  function uid() { return Date.now().toString(36) + Math.random().toString(36).slice(2, 7); }
  function anchor() { return document.querySelector("main") || document.body; }
  function anchorBox() {
    var r = anchor().getBoundingClientRect();
    return { left: r.left + window.scrollX, top: r.top + window.scrollY };
  }

  // ---- floating control ------------------------------------------------
  var fab = document.createElement("div");
  fab.className = "az-fab az-skip";
  fab.innerHTML =
    '<button type="button" class="az-fab-main" title="Add a note (click the page)">📝<span class="az-fab-count"></span></button>' +
    '<div class="az-fab-menu">' +
      '<button type="button" data-act="export" title="Export notes to a file">⭳</button>' +
      '<label title="Import notes from a file">⭱<input type="file" accept="application/json" hidden></label>' +
    "</div>";
  document.body.appendChild(fab);
  var mainBtn = fab.querySelector(".az-fab-main");
  var countEl = fab.querySelector(".az-fab-count");

  mainBtn.addEventListener("click", function () { setAdd(!addMode); });
  fab.querySelector('[data-act="export"]').addEventListener("click", exportNotes);
  fab.querySelector('input[type="file"]').addEventListener("change", importNotes);

  function setAdd(on) {
    addMode = on;
    document.body.classList.toggle("az-adding", on);
    mainBtn.classList.toggle("az-active", on);
    mainBtn.title = on ? "Click anywhere on the page to drop a note (Esc to cancel)" : "Add a note (click the page)";
  }

  document.addEventListener("keydown", function (e) { if (e.key === "Escape" && addMode) setAdd(false); });

  // ---- placing a note --------------------------------------------------
  document.addEventListener("click", function (e) {
    if (!addMode) return;
    if (e.target.closest(".az-skip")) return; // ignore clicks on our own UI
    e.preventDefault(); e.stopPropagation();
    var b = anchorBox();
    var note = { id: uid(), mx: Math.round(e.pageX - b.left), my: Math.round(e.pageY - b.top), text: "", ts: Date.now() };
    list().push(note); save(); setAdd(false); render();
    openEditor(note, true);
  }, true); // capture so links don't fire while adding

  // ---- rendering pins --------------------------------------------------
  function render() {
    var old = document.querySelectorAll(".az-pin"); for (var i = 0; i < old.length; i++) old[i].remove();
    var b = anchorBox();
    list().forEach(function (note) {
      var pin = document.createElement("button");
      pin.type = "button";
      pin.className = "az-pin az-skip" + (note.text ? "" : " az-empty");
      pin.style.left = (b.left + note.mx) + "px";
      pin.style.top = (b.top + note.my) + "px";
      pin.textContent = "📝";
      pin.title = note.text ? note.text.slice(0, 120) : "(empty note)";
      pin.addEventListener("click", function (ev) { ev.stopPropagation(); openEditor(note, false); });
      document.body.appendChild(pin);
    });
    countEl.textContent = total() ? String(total()) : "";
  }

  // ---- editor popover --------------------------------------------------
  var pop = null;
  function closeEditor() { if (pop) { pop.remove(); pop = null; } }
  function openEditor(note, isNew) {
    closeEditor();
    var b = anchorBox();
    pop = document.createElement("div");
    pop.className = "az-pop az-skip";
    pop.style.left = Math.min(b.left + note.mx, window.scrollX + document.documentElement.clientWidth - 300) + "px";
    pop.style.top = (b.top + note.my + 22) + "px";
    pop.innerHTML =
      '<textarea placeholder="Write a note…">' + escapeHtml(note.text) + "</textarea>" +
      '<div class="az-pop-row">' +
        '<button type="button" data-act="del" class="az-del">Delete</button>' +
        '<span class="az-spacer"></span>' +
        '<button type="button" data-act="save" class="az-save">Save</button>' +
      "</div>";
    document.body.appendChild(pop);
    var ta = pop.querySelector("textarea");
    ta.focus(); ta.setSelectionRange(ta.value.length, ta.value.length);
    pop.querySelector('[data-act="save"]').addEventListener("click", function () {
      note.text = ta.value.trim(); note.ts = Date.now();
      if (!note.text && isNew) removeNote(note); else save();
      closeEditor(); render();
    });
    pop.querySelector('[data-act="del"]').addEventListener("click", function () {
      removeNote(note); save(); closeEditor(); render();
    });
    ta.addEventListener("keydown", function (e) {
      if (e.key === "Escape") { if (!note.text && isNew) { removeNote(note); render(); } closeEditor(); }
      if ((e.ctrlKey || e.metaKey) && e.key === "Enter") pop.querySelector('[data-act="save"]').click();
    });
  }
  function removeNote(note) { var a = list(); var i = a.indexOf(note); if (i >= 0) a.splice(i, 1); }

  // close popover when clicking elsewhere
  document.addEventListener("mousedown", function (e) {
    if (pop && !e.target.closest(".az-pop") && !e.target.closest(".az-pin")) closeEditor();
  });

  // ---- export / import -------------------------------------------------
  function exportNotes() {
    var blob = new Blob([JSON.stringify(store, null, 2)], { type: "application/json" });
    var a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = "sc200-notes.json";
    document.body.appendChild(a); a.click(); a.remove();
    setTimeout(function () { URL.revokeObjectURL(a.href); }, 1000);
  }
  function importNotes(e) {
    var f = e.target.files && e.target.files[0]; if (!f) return;
    var reader = new FileReader();
    reader.onload = function () {
      try {
        var incoming = JSON.parse(reader.result);
        for (var k in incoming) if (incoming.hasOwnProperty(k)) {
          var have = store[k] || (store[k] = []);
          var ids = {}; have.forEach(function (n) { ids[n.id] = 1; });
          incoming[k].forEach(function (n) { if (!ids[n.id]) have.push(n); });
        }
        save(); render();
      } catch (err) { alert("Could not read that notes file."); }
    };
    reader.readAsText(f);
    e.target.value = "";
  }

  function escapeHtml(s) { return (s || "").replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }

  window.addEventListener("resize", render);
  render();

  // Served over http (serve.py): notes live in a file on disk — load them and re-render.
  if (SERVER) {
    try {
      fetch("/__notes").then(function (r) { return r.json(); }).then(function (d) {
        if (d && typeof d === "object") { store = d; render(); }
      }).catch(function () {});
    } catch (e) {}
  }
})();
