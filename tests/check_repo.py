"""Repository QA: relative links, anchors, Mermaid fences, and writing rules.

Run from the repo root:  python tests/check_repo.py
Exit code 1 on any failure, so it can run in CI next to the project tests.
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
BANNED = re.compile(
    r"\b(unlock\w*|substrate|delve\w*|pivotal|testament|tapestry|leverag(?:e|es|ed|ing)|utiliz\w*|garner\w*|"
    r"foster\w*|intricate|vibrant|enhanc\w*|showcas\w*|crucial|enduring|revolutionary|game-changing|"
    r"transformative|seamless\w*|robust|cutting-edge|supercharg\w*|skyrocket\w*)\b", re.IGNORECASE)
DASHES = re.compile("[\\u2014\\u2013]")
ALLOW_BANNED_IN = {"check_repo.py"}


def anchors(md: str) -> set[str]:
    out = set()
    for h in re.findall(r"^#{1,6}\s+(.+)$", md, re.MULTILINE):
        slug = re.sub(r"[^\w\- ]", "", h.strip().lower()).replace(" ", "-")
        out.add(slug)
    return out


def main() -> int:
    errors: list[str] = []
    md_files = sorted(p for p in ROOT.rglob("*.md") if ".git" not in p.parts)

    for path in md_files:
        text = path.read_text(encoding="utf-8")
        rel = path.relative_to(ROOT)
        no_code = re.sub(r"```.*?```", "", text, flags=re.DOTALL)

        for target in LINK.findall(no_code):
            if target.startswith(("http://", "https://", "mailto:")):
                continue
            file_part, _, anchor = target.partition("#")
            dest = (path.parent / file_part).resolve() if file_part else path
            if not dest.exists():
                errors.append(f"{rel}: broken link -> {target}")
                continue
            if anchor and dest.suffix == ".md" and anchor not in anchors(dest.read_text(encoding="utf-8")):
                errors.append(f"{rel}: missing anchor -> {target}")

        if text.count("```") % 2:
            errors.append(f"{rel}: unbalanced code fences")
        for block in re.findall(r"```mermaid\n(.*?)```", text, flags=re.DOTALL):
            first = block.strip().splitlines()[0] if block.strip() else ""
            if not re.match(r"(flowchart|graph|sequenceDiagram|erDiagram|classDiagram|stateDiagram)", first):
                errors.append(f"{rel}: mermaid block starts with unknown type: {first!r}")

    for path in sorted(ROOT.rglob("*")):
        if path.suffix not in {".md", ".py", ".json", ".sql"} or ".git" in path.parts or "results" in path.parts:
            continue
        text = path.read_text(encoding="utf-8")
        rel = path.relative_to(ROOT)
        if DASHES.search(text):
            errors.append(f"{rel}: contains an em or en dash")
        if path.name not in ALLOW_BANNED_IN and path.suffix == ".md":
            for m in BANNED.finditer(text):
                errors.append(f"{rel}: banned word '{m.group(0)}'")

    for e in errors:
        print(e)
    print(f"checked {len(md_files)} markdown files, {len(errors)} problems")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
