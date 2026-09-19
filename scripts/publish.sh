#!/usr/bin/env bash
# 초안을 _posts/ 로 옮기며 날짜를 붙인다.
# 사용: scripts/publish.sh _drafts/slug.md [YYYY-MM-DD]
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SRC="${1:?초안 파일을 적어 주세요}"
DATE="${2:-$(date +%Y-%m-%d)}"

case "$SRC" in
  /*) ;;
  *) SRC="$ROOT/$SRC" ;;
esac
[ -f "$SRC" ] || { echo "파일이 없습니다: $SRC" >&2; exit 1; }

NAME="$(basename "$SRC" .md)"
DEST="$ROOT/_posts/$DATE-$NAME.md"
[ -e "$DEST" ] && { echo "이미 있습니다: $DEST" >&2; exit 1; }

mkdir -p "$ROOT/_posts"
# front matter 에 date 가 없으면 넣는다
if grep -q '^date:' "$SRC"; then
  cp "$SRC" "$DEST"
else
  awk -v d="$DATE" 'NR==1{print; print "date: " d; next} {print}' "$SRC" > "$DEST"
fi
rm "$SRC"

echo "발행: $DEST"
echo "확인 후: git add _posts && git commit -m \"글: $NAME\" && git push"
