import requests
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
today = datetime.today().strftime("%Y-%m-%d")
API_KEY = os.getenv("AUTHKEY")
URL = f"https://{today}.currency-api.pages.dev/v1/currencies/krw.json"


README_PATH = "README.md"

def get_currency():
    response = requests.get(URL)
    if response.status_code == 200:
        data = response.json()['krw']
        return list(map(lambda x: f"| {x[0]} | {round(1/x[1], 2)} |", data.items()))
    else:
        return []

def update_readme():
    """README.md 파일을 업데이트 (표 형식 적용)"""
    currency_info = get_currency()
    # now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if not currency_info:
        currency_table = "환율 정보를 가져오는 데 실패했습니다."
    else:
        # 마크다운 표 헤더와 구분선 추가
        currency_table = """| 통화코드 | 환율 |
|------------|------------------|
"""
        currency_table += "\n".join(currency_info)

    readme_content = f"""
이 리포지토리는 한국수출입은행 API를 사용하여 환율 정보를 자동으로 업데이트합니다.

## 현재 환율

{currency_table}

⏳ 업데이트 날짜: {today}

---
자동 업데이트 봇에 의해 관리됩니다.
"""

    with open(README_PATH, "w", encoding="utf-8") as file:
        file.write(readme_content)

if __name__ == "__main__":
    update_readme()
