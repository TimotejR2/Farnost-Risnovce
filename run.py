#!/usr/bin/env python
import sys, subprocess, os, pkg_resources

required = [
    "Flask==2.2.5",
    "Werkzeug==3.0.6",
    "psycopg2-binary==2.9.9"
]

missing = []
for pkg in required:
    try:
        pkg_resources.require(pkg)
    except Exception:
        missing.append(pkg)

if missing:
    subprocess.check_call([sys.executable, "-m", "pip", "install"] + missing)
    os.execv(sys.executable, [sys.executable] + sys.argv)

from app import app

if __name__ == '__main__':
    app.run()
