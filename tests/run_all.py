"""Run every project's tests plus the repository checks.

Run from anywhere:  python tests/run_all.py
"""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROJECTS = ["conversation-intelligence", "ai-evaluation", "gtm-ontology", "lookalike-model"]


def main() -> int:
    failed = []
    for name in PROJECTS:
        print(f"== {name}")
        r = subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-t", "."],
                           cwd=ROOT / "projects" / name)
        if r.returncode:
            failed.append(name)
    print("== repository checks")
    if subprocess.run([sys.executable, str(ROOT / "tests" / "check_repo.py")]).returncode:
        failed.append("check_repo")
    print("FAILED: " + ", ".join(failed) if failed else "ALL PASSED")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
