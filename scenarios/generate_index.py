#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path

ALLOWED_TAGS = [
    "advent2025",
    "apache",
    "bash",
    "c",
    "caddy",
    "clickhouse",
    "csv",
    "data processing",
    "disk volumes",
    "dns",
    "docker",
    "envoy",
    "etcd",
    "git",
    "golang",
    "gunicorn",
    "hack",
    "haproxy",
    "harbor",
    "hashicorp vault",
    "helm",
    "java",
    "jenkins",
    "json",
    "kubernetes",
    "linux-other",
    "mysql",
    "nginx",
    "node.js",
    "php",
    "podman",
    "postgres",
    "prometheus",
    "python",
    "rabbitmq",
    "redis",
    "sql",
    "sqlite",
    "ssh",
    "ssl",
    "supervisord",
    "systemd",
    "realistic",
    "interviews",
    "new",
    "pro",
    "business",
]
ALLOWED_SET = {tag.lower(): tag for tag in ALLOWED_TAGS}


ROOT = Path(__file__).resolve().parent
OUTPUT_FILE = ROOT / "scenario-index.json"


def extract_title(text: str) -> str:
    match = re.search(r"^#\s+(.*)", text, flags=re.MULTILINE)
    return match.group(1).strip() if match else "Untitled"


def extract_description(text: str) -> str:
    match = re.search(
        r"##\s+Description[: ]*\n+(.*?)(?:\n##|\Z)",
        text,
        flags=re.DOTALL | re.IGNORECASE,
    )
    if match:
        description = match.group(1)
    else:
        fallback = re.search(r"^#.*?\n+(.*?)(?:\n##|\Z)", text, flags=re.DOTALL | re.MULTILINE)
        description = fallback.group(1) if fallback else ""
    description = re.sub(r"`([^`]*)`", r"\1", description)
    description = re.sub(r"\s+", " ", description)
    return description.strip()


def extract_meta(text: str, label: str) -> str:
    pattern = rf"(?mi)^[>\*\s-]*{label}\s*:?\s*([^\n<]+)"
    inline = re.search(pattern, text)
    if inline:
        return inline.group(1).strip()
    bold = re.search(rf"(?i){label}\s*</?b>:\s*([^<\n]+)", text)
    if bold:
        return bold.group(1).strip()
    return ""


def extract_tags(text: str, slug: str, title: str) -> list[str]:
    tags: list[str] = []
    heading = re.search(
        r"##\s+Tags\s*\n+(.*?)(?:\n##|\Z)", text, flags=re.DOTALL | re.IGNORECASE
    )
    if heading:
        for line in heading.group(1).splitlines():
            line = line.strip(" -*\t")
            if line:
                tags.append(line)
    else:
        line = re.search(r"^tags?:\s*(.+)$", text, flags=re.MULTILINE | re.IGNORECASE)
        if line:
            raw = line.group(1)
            tags.extend([part.strip() for part in re.split(r"[;,]", raw) if part.strip()])
    blob = f"{slug} {title} {text}".lower()
    keyword_map = [
        (["advent"], "advent2025"),
        (["apache"], "apache"),
        ([" bash", "shell", "command"], "bash"),
        ([" c "], "c"),
        (["caddy"], "caddy"),
        (["clickhouse"], "clickhouse"),
        (["csv"], "csv"),
        (["data", "processing"], "data processing"),
        (["disk", "volume", "lvm"], "disk volumes"),
        (["dns"], "dns"),
        (["docker", "container", "compose"], "docker"),
        (["envoy"], "envoy"),
        (["etcd"], "etcd"),
        (["git"], "git"),
        ([" golang", " go "], "golang"),
        (["gunicorn"], "gunicorn"),
        (["hack", "ctf", "exploit"], "hack"),
        (["haproxy"], "haproxy"),
        (["harbor"], "harbor"),
        (["vault"], "hashicorp vault"),
        (["helm"], "helm"),
        (["java"], "java"),
        (["jenkins"], "jenkins"),
        (["json"], "json"),
        (["kubernetes", "k8s", "kubectl", "namespace"], "kubernetes"),
        (["linux", "bash", "shell"], "linux-other"),
        (["mysql"], "mysql"),
        (["nginx"], "nginx"),
        (["node.js", "nodejs", "node "], "node.js"),
        (["php"], "php"),
        (["podman"], "podman"),
        (["postgres", "postgresql"], "postgres"),
        (["prometheus"], "prometheus"),
        (["python"], "python"),
        (["rabbitmq"], "rabbitmq"),
        (["redis"], "redis"),
        ([" sql", "query"], "sql"),
        (["sqlite"], "sqlite"),
        (["ssh"], "ssh"),
        ([" tls", "ssl"], "ssl"),
        (["supervisor"], "supervisord"),
        (["systemd"], "systemd"),
        (["interview"], "interviews"),
        (["realistic"], "realistic"),
        ([" new "], "new"),
        (["pro"], "pro"),
        (["business"], "business"),
    ]
    for keywords, mapped in keyword_map:
        if any(word in blob for word in keywords):
            tags.append(mapped)
    seen = set()
    deduped = []
    for tag in tags:
        key = tag.lower()
        if key not in seen:
            seen.add(key)
            deduped.append(tag)
    filtered: list[str] = []
    for tag in deduped:
        canonical = ALLOWED_SET.get(tag.lower())
        if canonical and canonical not in filtered:
            filtered.append(canonical)
    priority = [tag for tag in ALLOWED_TAGS if tag in filtered]
    return priority[:3]


def to_excerpt(text: str, limit: int = 220) -> str:
    if len(text) <= limit:
        return text
    truncated = text[:limit].rsplit(" ", 1)[0].rstrip()
    return f"{truncated}..."


def build_index() -> list[dict]:
    entries: list[dict] = []
    for readme in sorted(ROOT.glob("*/README.md")):
        slug = readme.parent.name
        text = readme.read_text(encoding="utf-8")
        title = extract_title(text)
        description = extract_description(text)
        tags = extract_tags(text, slug, title)
        level = extract_meta(text, "Level")
        scenario_type = extract_meta(text, "Type")
        access = extract_meta(text, "Access")
        time_to_solve = extract_meta(text, "Time to Solve") or extract_meta(text, "Time")
        entries.append(
            {
                "slug": slug,
                "title": title,
                "description": description,
                "excerpt": to_excerpt(description),
                "tags": tags,
                "level": level,
                "type": scenario_type,
                "access": access,
                "time": time_to_solve,
                "readme": f"{slug}/README.md",
            }
        )
    return entries


def main() -> None:
    entries = build_index()
    OUTPUT_FILE.write_text(json.dumps(entries, indent=2), encoding="utf-8")
    print(f"Wrote {len(entries)} entries to {OUTPUT_FILE.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
