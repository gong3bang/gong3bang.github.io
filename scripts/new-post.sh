#!/usr/bin/env bash
# 공공공부 초안 틀을 _drafts/ (Drive 초안 폴더)에 만든다.
# 사용: scripts/new-post.sh "제목" [분야] [연재] [호수]
#   분야: policy | law | business | case | tech | security  (기본 law)
#   연재: haedo | gongbaek  (없으면 생략)
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TITLE="${1:?제목을 적어 주세요}"
CATEGORY="${2:-law}"
SERIES="${3:-}"
ISSUE="${4:-}"

# 파일명은 ascii slug. 한글 제목이면 날짜+시각으로.
SLUG="$(printf '%s' "$TITLE" | tr '[:upper:]' '[:lower:]' | sed -E 's/[^a-z0-9]+/-/g; s/^-+|-+$//g')"
if [ -z "$SLUG" ]; then SLUG="draft-$(date +%Y%m%d-%H%M)"; fi
FILE="$ROOT/_drafts/$SLUG.md"

if [ -e "$FILE" ]; then echo "이미 있습니다: $FILE" >&2; exit 1; fi

SERIES_LINES=""
if [ -n "$SERIES" ]; then
  SERIES_LINES="series: $SERIES"
  if [ -n "$ISSUE" ]; then SERIES_LINES="$SERIES_LINES
issue: $ISSUE"; fi
fi

cat > "$FILE" <<EOF
---
title: $TITLE
category: $CATEGORY
$SERIES_LINES
version: v1.0
summary:
  -
  -
history:
  - { version: v1.0, date: $(date +%Y-%m-%d), note: 첫 발행 }
---

## 장면

<!-- 내가 본 것, 부딪힌 것. 3문장 이내 -->

## 본문

<!-- 근거 → 정리 → 표나 그림 하나 -->

## 그래서 담당자는

<!-- 무엇을 하면 되나 -->

## 붙임

<!-- 체크리스트, 코드, 원문 링크. 없으면 이 절을 지운다 -->
EOF

echo "초안: $FILE"
