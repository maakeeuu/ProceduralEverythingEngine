from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
required_root = {"AI_RULES.md", "CURRENT_STATE.md", "DECISIONS.md", "DEVELOPMENT_LOG.md", "MASTER_CONTEXT.md", "PROJECT_BRIEF.md", "TASKS.md"}
required_research = {"README.md", "ARCHITECTURE_PROPOSAL.md", "TECHNOLOGY_COMPARISON.md", "RISK_REGISTER.md", "EXPERIMENT_PLAN.md", "DEVELOPMENT_ROADMAP.md", "OPEN_QUESTIONS.md", "OPUS_REVIEW_BRIEF.md", "HANDOFF.md", "SOURCES.md", "VALIDATION_REPORT.md"}
research = ROOT / "docs/research/gpt"
files = [ROOT / name for name in sorted(required_root)] + [research / name for name in sorted(required_research)]
sources = set(re.findall(r"^### (S\d+) ", (research / "SOURCES.md").read_text(encoding="utf-8"), re.M))
issues = []
links = 0
for path in files:
    if not path.is_file():
        issues.append(f"Missing required file: {path.relative_to(ROOT)}")
        continue
    text = path.read_text(encoding="utf-8")
    if not text.startswith("# ") or "\x00" in text or "{{@" in text:
        issues.append(f"Invalid document: {path.relative_to(ROOT)}")
    for destination in re.findall(r"\]\(([^)]+)\)", text):
        if re.match(r"^[a-z]+:", destination) or destination.startswith("#"):
            continue
        links += 1
        if not (path.parent / destination.split("#")[0]).is_file():
            issues.append(f"Broken link: {path.relative_to(ROOT)} -> {destination}")
    for source in re.findall(r"\bS\d{2}\b", text):
        if source not in sources:
            issues.append(f"Undefined source: {source} in {path.relative_to(ROOT)}")
    for pattern in [r"github_pat_[A-Za-z0-9_]{20,}", r"gh[pousr]_[A-Za-z0-9]{20,}", r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"]:
        if re.search(pattern, text):
            issues.append(f"Possible secret in {path.relative_to(ROOT)}")
if issues:
    raise SystemExit("\n".join(issues))
print(f"PASS: {len(files)} required Markdown files; {links} local links; {len(sources)} source records; basic secret-pattern scan")
print("Application builds, algorithm/UI/GPU/security tests and benchmarks: NOT RUN (documentation-only change)")
