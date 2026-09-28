"""
run_pipeline.py — orkestrator end-to-end.

Urutan: ingest → load_db → transform → tests → alerts
Satu perintah menjalankan seluruh pipeline (reproducible).

    python src/run_pipeline.py            # pipeline penuh
    python src/run_pipeline.py --no-ingest  # pakai staging yang ada
"""

from __future__ import annotations

import argparse
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = Path(__file__).resolve().parent


def run(script: str, args: list[str] | None = None) -> bool:
    cmd = [sys.executable, str(script)] + (args or [])
    print(f"\n{'='*64}\n▶ {Path(script).name}\n{'='*64}")
    t0 = time.time()
    r = subprocess.run(cmd, cwd=str(ROOT))
    ok = r.returncode == 0
    print(f"{'✓' if ok else '✗'} {Path(script).name} "
          f"({time.time()-t0:.1f}s, exit={r.returncode})")
    return ok


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-ingest", action="store_true",
                    help="lewati ingest (pakai staging yang sudah ada)")
    ap.add_argument("--no-charts", action="store_true",
                    help="lewati pembuatan chart PNG")
    args = ap.parse_args()

    steps = []
    if not args.no_ingest:
        steps.append(SRC / "ingest.py")
    steps += [SRC / "load_db.py", SRC / "transform.py",
              SRC / "alerts.py", ROOT / "tests" / "test_data_quality.py"]
    if not args.no_charts:
        steps.append(SRC / "make_charts.py")

    for s in steps:
        if not run(s):
            print(f"\n✗ PIPELINE GAGAL di {s.name}")
            return 1
    print("\n" + "=" * 64)
    print("✓ PIPELINE SELESAI")
    print("=" * 64)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
