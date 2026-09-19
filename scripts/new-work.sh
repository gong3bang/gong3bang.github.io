#!/usr/bin/env bash
# 만든 것(_works/) 항목 틀을 만든다.
# 사용: scripts/new-work.sh "이름" slug [저장소URL]
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TITLE="${1:?이름을 적어 주세요}"
SLUG="${2:?slug(영문)를 적어 주세요}"
REPO="${3:-}"
FILE="$ROOT/_works/$SLUG.md"

[ -e "$FILE" ] && { echo "이미 있습니다: $FILE" >&2; exit 1; }
mkdir -p "$ROOT/_works"

cat > "$FILE" <<EOF
---
title: $TITLE
one_liner:
repo: $REPO
status: 진행중
version: v0.1
license: MIT
date: $(date +%Y-%m-%d)
history:
  - { version: v0.1, date: $(date +%Y-%m-%d), note: 처음 올림 }
---

## 무엇을 해결하나

## 30초 실행

\`\`\`bash
\`\`\`

## 한계와 주의

## 근거

<!-- 관련 법령·지침·문서 링크 -->
EOF

echo "만든 것: $FILE"
