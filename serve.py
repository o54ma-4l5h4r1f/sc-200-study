#!/usr/bin/env python3
"""Local server for the SC-200 study site so page notes auto-save to disk.

Stdlib only, no internet. Serves site/ at http://localhost:8000 and persists the
annotations added with the on-page notes tool (notes.js) to progress/notes.json via
GET/POST /__notes. Opening the site this way makes notes save to a real file by
default; the plain file:// double-click still works with the localStorage fallback.

    python3 build.py      # (re)generate site/
    python3 serve.py      # then open http://localhost:8000
    python3 serve.py 9000 # custom port

Binds 127.0.0.1 only — reachable from this machine, not the network.
"""
import functools
import json
import sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SITE = ROOT / "site"
NOTES = ROOT / "progress" / "notes.json"


class Handler(SimpleHTTPRequestHandler):
    def _json(self, obj, code=200):
        body = json.dumps(obj).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path.split("?")[0] == "/__notes":
            try:
                data = json.loads(NOTES.read_text(encoding="utf-8")) if NOTES.exists() else {}
            except Exception:
                data = {}
            return self._json(data)
        return super().do_GET()

    def do_POST(self):
        if self.path.split("?")[0] == "/__notes":
            length = int(self.headers.get("Content-Length", 0) or 0)
            raw = self.rfile.read(length) if length else b"{}"
            try:
                data = json.loads(raw.decode("utf-8"))
                if not isinstance(data, dict):
                    raise ValueError
            except Exception:
                return self._json({"error": "bad json"}, 400)
            NOTES.parent.mkdir(parents=True, exist_ok=True)
            tmp = NOTES.with_name(NOTES.name + ".tmp")
            tmp.write_text(json.dumps(data, indent=2), encoding="utf-8")
            tmp.replace(NOTES)  # atomic
            return self._json({"ok": True, "pages": len(data)})
        self.send_error(405, "POST only supported for /__notes")

    def log_message(self, *args):  # keep the console quiet
        pass


def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    if not SITE.exists():
        print("site/ not found — run `python3 build.py` first.", file=sys.stderr)
        return 1
    handler = functools.partial(Handler, directory=str(SITE))
    httpd = ThreadingHTTPServer(("127.0.0.1", port), handler)
    print(f"SC-200 site  →  http://localhost:{port}")
    print(f"notes auto-save to  {NOTES.relative_to(ROOT)}")
    print("Ctrl+C to stop.")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nstopped.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
