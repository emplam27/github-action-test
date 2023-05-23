import os
import openai
from datetime import datetime
from pytz import timezone
from news_scrapper import NewsScrapper
from github_utils import get_github_repo, upload_github_issue

openai.api_key = os.environ["OPENAI_API_KEY"]
news_route_url = "https://news.naver.com/main/ranking/popularDay.naver"
access_token = os.environ['MY_GITHUB_TOKEN']
repository_name = "github-action-test"


def generate_prompt(news_headline):
    return """Suggest a podcast script about '{}' as following form sheet\n"
          "제목: <br/>"
          "요약: <br/>"
          "\n\n"
          Please start writing the script.
          """.format(
        news_headline.capitalize()
    )

if __name__ == '__main__':
    news_headline = NewsScrapper(news_route_url).get_news(1)[0].title
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=generate_prompt(news_headline),
        temperature=0.7,
        n=1,
        max_tokens=256,
        stop=None,
    )

    seoul_timezone = timezone('Asia/Seoul')
    today = datetime.now(seoul_timezone)
    today_date = today.strftime("%Y년 %m월 %d일 %H시 %M분")

    issue_title = f"실시간 뉴스 요약({today_date})"
    repo = get_github_repo(access_token, repository_name)
    upload_github_issue(repo, issue_title, news_headline)
    print("Upload Github Issue Success!")

