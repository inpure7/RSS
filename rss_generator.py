import requests
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator

BASE_URL = "https://www.pipc.go.kr"
BOARD_URL = f"{BASE_URL}/np/cop/bbs/selectBoardList.do?bbsId=BS074"

def generate_rss():
    res = requests.get(BOARD_URL)
    soup = BeautifulSoup(res.text, "html.parser")

    items = soup.select(".list_board tbody tr")
    fg = FeedGenerator()
    fg.title("개인정보위 보도자료")
    fg.link(href=BOARD_URL, rel='alternate')
    fg.description("개인정보보호위원회 보도자료 자동 생성 RSS 피드")

    for item in items[:5]:
        title_tag = item.select_one("td.subject a")
        title = title_tag.text.strip()
        href = title_tag["href"]
        link = BASE_URL + href
        date = item.select("td")[-1].text.strip()

        fe = fg.add_entry()
        fe.title(title)
        fe.link(href=link)
        fe.pubDate(date)

    fg.rss_file("rss.xml")

if __name__ == "__main__":
    generate_rss()
