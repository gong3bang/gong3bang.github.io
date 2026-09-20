#!/usr/bin/env python3
"""GitHub 공개 저장소를 읽어 _works/ 에 공공공구 항목을 만든다.

- 표준 라이브러리만 쓴다
- 파일명: _works/<repo-name>.md  (front matter 에 source: github)
- 이 사이트 저장소(gong3bang.github.io)와 fork 는 뺀다
- 더 이상 공개 목록에 없는 github 항목 파일은 지운다 (source: github 인 것만)

사용: python3 scripts/fetch_github.py [USER]   (GITHUB_TOKEN 이 있으면 인증해서 호출)
"""
import json
import os
import re
import sys
import urllib.request
from datetime import datetime, timezone, timedelta

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
USER = sys.argv[1] if len(sys.argv) > 1 else "gong3bang"
WORKS_DIR = os.path.join(ROOT, "_works")
EXCLUDE = {f"{USER}.github.io"}
KST = timezone(timedelta(hours=9))


def api(url):
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "gong3bang-site/1.0"}
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode("utf-8"))


def fetch_repos():
    repos, page = [], 1
    while True:
        batch = api(f"https://api.github.com/users/{USER}/repos?type=owner&sort=updated&per_page=100&page={page}")
        if not batch:
            break
        repos.extend(batch)
        if len(batch) < 100:
            break
        page += 1
    out = []
    for r in repos:
        if r.get("private") or r.get("fork") or r["name"] in EXCLUDE:
            continue
        out.append(r)
    return out


def yaml_str(s):
    return '"' + (s or "").replace("\\", "\\\\").replace('"', '\\"') + '"'


def kst(iso):
    try:
        return datetime.fromisoformat(iso.replace("Z", "+00:00")).astimezone(KST)
    except Exception:
        return datetime.now(KST)


def render(r):
    created, pushed = kst(r["created_at"]), kst(r["pushed_at"])
    status = "보관" if r.get("archived") else "공개"
    lic = (r.get("license") or {}).get("spdx_id") or ""
    if lic == "NOASSERTION":
        lic = ""
    topics = [t for t in (r.get("topics") or []) if t]
    lines = [
        "---",
        f"title: {yaml_str(r['name'])}",
        f"one_liner: {yaml_str(r.get('description') or '')}",
        f"repo: {yaml_str(r['html_url'])}",
        f"status: {status}",
        f"date: {created.strftime('%Y-%m-%d')}",
        f"updated: {pushed.strftime('%Y-%m-%d')}",
        f"language: {yaml_str(r.get('language') or '')}",
        f"stars: {int(r.get('stargazers_count') or 0)}",
        f"license: {yaml_str(lic)}",
        f"homepage: {yaml_str(r.get('homepage') or '')}",
        "topics: [" + ", ".join(yaml_str(t) for t in topics) + "]",
        "source: github",
        "---",
        "",
        (r.get("description") or r["name"]).strip(),
        "",
    ]
    return "\n".join(lines)


def is_generated(path):
    try:
        with open(path, encoding="utf-8") as f:
            head = f.read(2000)
        return bool(re.search(r"^source:\s*github\s*$", head, re.M))
    except Exception:
        return False


def main():
    try:
        repos = fetch_repos()
    except Exception as e:
        print(f"GitHub API 를 읽지 못했습니다: {e}", file=sys.stderr)
        sys.exit(1)
    os.makedirs(WORKS_DIR, exist_ok=True)
    wanted = {}
    for r in repos:
        fname = re.sub(r"[^A-Za-z0-9._-]+", "-", r["name"]).strip("-").lower() + ".md"
        wanted[fname] = render(r)

    counts = {"created": 0, "updated": 0, "same": 0, "removed": 0}
    for fname, content in wanted.items():
        path = os.path.join(WORKS_DIR, fname)
        old = open(path, encoding="utf-8").read() if os.path.exists(path) else None
        if old == content:
            counts["same"] += 1
            continue
        if old is not None and not is_generated(path):
            print(f"손으로 만든 파일이라 건너뜀: {fname}")
            continue
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        counts["updated" if old else "created"] += 1
        print(f"{'updated' if old else 'created'}: {fname}")

    for fname in os.listdir(WORKS_DIR):
        path = os.path.join(WORKS_DIR, fname)
        if fname.endswith(".md") and fname not in wanted and is_generated(path):
            os.remove(path)
            counts["removed"] += 1
            print(f"removed: {fname}")

    print(f"완료: 새 항목 {counts['created']}, 고침 {counts['updated']}, 그대로 {counts['same']}, 지움 {counts['removed']} (공개 저장소 {len(repos)})")


if __name__ == "__main__":
    main()
