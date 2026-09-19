# gong3bang.github.io

공공공방 공방장 공삼의 작업실. 먼저 읽고, 만들어 둡니다.

## 무엇을 해결하나

공공에서 일하며 필요해서 읽은 것, 정리한 것, 만든 것을 여기 둡니다. 공방장 공삼이 公 공공의 자리에서, 攻 파고들어 정리하고, 工 직접 만들어 둡니다.

| 공 | 뜻 | 메뉴 | 어디에 |
|---|---|---|---|
| 公 | 도메인. 공공의 자리에서 | 사이트 전체 | |
| 攻 | 태도. 파고들어 정리한 것. 분야는 정책 · 법제도 · 공공사업 · 사례 · 기술 · 보안 | 공공공부 | `_posts/` |
| 工 | 직접 만든 도구 | 공공공구 | `_works/` |
| | 내려받아 쓰는 자료 | 붙임 | `_attachments/` + `assets/files/` |

## 30초 실행

```bash
brew install ruby@3.3
export PATH="/opt/homebrew/opt/ruby@3.3/bin:$PATH"
gem install bundler
bundle install
bundle exec jekyll serve --drafts --livereload
```

http://localhost:4000 에서 확인합니다. GitHub Pages가 `main`을 자동으로 빌드하므로 배포는 push만 하면 됩니다.

글 쓰기:

```bash
scripts/new-post.sh "제목" law            # 공공공부 초안 생성 (분야: policy|law|business|case|tech|security)
scripts/publish.sh _drafts/slug.md        # _posts 로 옮기고 날짜 붙임
scripts/new-work.sh "이름" my-tool        # 공공공구 항목 생성
```

## 한계와 주의

- `_drafts/`와 `_notes/`는 저장소에 올라가지 않습니다. 초안은 발행 전까지 로컬에만 있습니다.
- 댓글은 giscus를 씁니다. `_config.yml`의 `giscus:` 값을 채우기 전까지는 나타나지 않습니다.
- 사이트 공지는 `_config.yml`의 `notice:`에서 켜고 끕니다. `text`를 비우면 사라지고, `id`를 바꾸면 닫았던 사람에게도 다시 보입니다.
- 라이트·다크 모드는 머리의 버튼으로 바꾸며, 선택은 그 브라우저에만 저장됩니다.
- 글 분야는 `_data/categories.yml`에서, 연재는 `_data/series.yml`에서 관리합니다.

## 라이선스

글은 [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/deed.ko), 코드는 [MIT](LICENSE). 모든 글은 개인 의견이며 소속 기관의 입장이 아닙니다.

끝.
