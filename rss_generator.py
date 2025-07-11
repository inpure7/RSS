def generate_rss():
    fg = FeedGenerator()
    fg.title("개인정보위 통합 RSS")
    fg.link(href=BASE_URL, rel='alternate')
    fg.description("보도자료 + 공지사항 게시판 자동 RSS")

    has_items = False  # ← 항목 추가 여부 추적

    for name, url in BOARDS.items():
        try:
            print(f"📥 {name} 수집 중... ({url})")
            res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
            res.raise_for_status()
            soup = BeautifulSoup(res.text, "html.parser")

            rows = soup.select("table.list_board tbody tr")
            print(f"🔎 {name}에서 {len(rows)}개의 글 감지")

            for row in rows[:5]:
                title_tag = row.select_one("td.subject a")
                if not title_tag:
                    print(f"⚠️ {name} - 제목 없음, 건너뜀")
                    continue

                cols = row.select("td")
                if len(cols) < 4:
                    print(f"⚠️ {name} - td 개수 부족, 건너뜀")
                    continue

                title = title_tag.text.strip()
                href = title_tag.get("href", "")
                link = BASE_URL + href if href else BASE_URL
                date = cols[-1].text.strip()

                print(f"📝 {name} 항목 추가됨: {title} ({date})")

                fe = fg.add_entry()
                fe.title(f"[{name}] {title}")
                fe.link(href=link)
                fe.pubDate(date)

                has_items = True  # ✅ 실제 항목 추가됨 표시

        except Exception as e:
            print(f"❗ [{name}] 오류 발생: {e}")

    # ✅ try-except 블록을 빠져나온 뒤 테스트 항목 조건부 추가
    if not has_items:
        print("⚠️ 실제 항목이 없어 테스트 항목 추가")
        fe = fg.add_entry()
        fe.title("[테스트] 새 글이 없어 자동 생성된 항목입니다.")
        fe.link(href="https://example.com")
        fe.pubDate("Wed, 09 Jul 2025 00:00:00 +0000")

    fg.rss_file("rss.xml")
    print("✅ rss.xml 생성 완료")
