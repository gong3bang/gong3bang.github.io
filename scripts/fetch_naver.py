#!/usr/bin/env python3
"""네이버 블로그 RSS를 읽어 _posts/ 에 공공공부 글 파일을 만든다.

- 표준 라이브러리만 쓴다 (GitHub Actions 에서 바로 돈다)
- 파일명: _posts/YYYY-MM-DD-naver-<logNo>.md
- front matter 의 external_url 로 네이버 원문에 연결한다
- 네이버 카테고리 이름이 _data/categories.yml 의 name 또는 aliases 와 같으면 그 분야로 넣는다

사용: python3 scripts/fetch_naver.py [RSS_URL]
"""
import html
import os
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone, timedelta
from email.utils import parsedate_to_datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RSS_URL = sys.argv[1] if len(sys.argv) > 1 else "https://rss.blog.naver.com/gong3bang.xml"
POSTS_DIR = os.path.join(ROOT, "_posts")
CATEGORIES_YML = os.path.join(ROOT, "_data", "categories.yml")
KST = timezone(timedelta(hours=9))


def load_category_map():
    """categories.yml 을 아주 단순하게 읽는다 (key / name / aliases 만)."""
    mapping = {}
    if not os.path.exists(CATEGORIES_YML):
        return mapping
    key = None
    with open(CATEGORIES_YML, encoding="utf-8") as f:
        for raw in f:
            line = raw.rstrip("\n")
            m = re.match(r"^-\s+key:\s*(\S+)", line)
            if m:
                key = m.group(1)
                mapping[key] = key
                continue
            m = re.match(r"^\s+name:\s*(.+)$", line)
            if m and key:
                mapping[m.group(1).strip()] = key
                continue
            m = re.match(r"^\s+aliases:\s*\[(.*)\]", line)
            if m and key:
                for a in m.group(1).split(","):
                    a = a.strip().strip("'\"")
                    if a:
                        mapping[a] = key
    return mapping


def strip_html(s):
    s = re.sub(r"<[^>]+>", " ", s or "")
    s = html.unescape(s)
    return re.sub(r"\s+", " ", s).strip()


def yaml_str(s):
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "gong3bang-site/1.0 (+https://gong3bang.github.io)"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()


def parse_items(xml_bytes):
    root = ET.fromstring(xml_bytes)
    items = []
    for it in root.iter("item"):
        title = (it.findtext("title") or "").strip()
        link = (it.findtext("link") or "").strip()
        desc = it.findtext("description") or ""
        pub = it.findtext("pubDate") or ""
        cats = [c.text.strip() for c in it.findall("category") if c.text]
        if not title or not link:
            continue
        m = re.search(r"/(\d+)(?:\?|$)", link) or re.search(r"logNo=(\d+)", link)
        log_no = m.group(1) if m else re.sub(r"\W+", "", link)[-16:]
        try:
            dt = parsedate_to_datetime(pub).astimezone(KST)
        except Exception:
            dt = datetime.now(KST)
        items.append({
            "title": title,
            "link": link,
            "summary": strip_html(desc)[:140],
            "date": dt,
            "categories": cats,
            "log_no": log_no,
        })
    return items


def write_post(item, cat_map):
    os.makedirs(POSTS_DIR, exist_ok=True)
    # 같은 logNo 로 만든 파일이 있으면 날짜가 달라도 그 파일을 갱신한다
    existing = [f for f in os.listdir(POSTS_DIR) if f.endswith(f"-naver-{item['log_no']}.md")]
    fname = existing[0] if existing else f"{item['date'].strftime('%Y-%m-%d')}-naver-{item['log_no']}.md"
    path = os.path.join(POSTS_DIR, fname)

    category = ""
    for c in item["categories"]:
        if c in cat_map:
            category = cat_map[c]
            break

    lines = ["---", f"title: {yaml_str(item['title'])}", f"date: {item['date'].strftime('%Y-%m-%d %H:%M:%S %z')}"]
    if category:
        lines.append(f"category: {category}")
    if item["categories"]:
        lines.append(f"naver_category: {yaml_str(item['categories'][0])}")
    lines += [
        "source: naver",
        f"external_url: {yaml_str(item['link'])}",
        f"summary: [{yaml_str(item['summary'])}]" if item["summary"] else "summary: []",
        "---",
        "",
        item["summary"] or item["title"],
        "",
    ]
    content = "\n".join(lines)

    old = open(path, encoding="utf-8").read() if os.path.exists(path) else None
    if old == content:
        return "same", fname
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return ("updated" if old else "created"), fname


def main():
    try:
        xml_bytes = fetch(RSS_URL)
    except Exception as e:
        print(f"RSS 를 받지 못했습니다: {e}", file=sys.stderr)
        sys.exit(1)
    items = parse_items(xml_bytes)
    if not items:
        print("RSS 에 항목이 없습니다. (네이버 블로그의 RSS 공개 설정을 확인하세요)")
        return
    cat_map = load_category_map()
    counts = {"created": 0, "updated": 0, "same": 0}
    for item in items:
        status, fname = write_post(item, cat_map)
        counts[status] += 1
        if status != "same":
            print(f"{status}: {fname}")
    print(f"완료: 새 글 {counts['created']}, 고친 글 {counts['updated']}, 그대로 {counts['same']} (RSS 항목 {len(items)})")


if __name__ == "__main__":
    main()
