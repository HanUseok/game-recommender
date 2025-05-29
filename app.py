from flask import Flask, render_template
import datetime
import gspread
import json
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

# 🔹 1. 구글시트 연동 (앱 시작 시 한 번만 실행)
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

with open("/etc/secrets/credentials.json") as f:
    creds_json = json.load(f)

creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_json, scope)
client = gspread.authorize(creds)

# 🔹 여기에 네 구글시트 URL 입력
sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1hvAVXcmJJ2hY9UToV500KwHepmyrnfxH8G4aOt_48Xo/edit").sheet1

# 🔹 2. 추천 알고리즘 함수
def recommend_game():
    responses = sheet.get_all_records()
    if not responses:
        return "추천 데이터를 불러올 수 없습니다."

    latest = responses[-1]  # 최근 응답 1개
    중요요소 = latest.get("게임을 선택할 때 가장 중요하게 생각하는 요소는 무엇인가요?", "")
    혼자게임 = latest.get("혼자하는 게임을 좋아하시나요?", "")
    
    # 간단한 조건 기반 예시
    if "스토리" in 중요요소 and 혼자게임 == "그렇다":
        return "Red Dead Redemption 2"
    elif "조작감" in 중요요소:
        return "Monster Hunter Rise"
    elif "그래픽" in 중요요소:
        return "Ori and the Will of the Wisps"
    else:
        return "Hades"

# 🔹 3. 웹페이지에서 결과 보여주는 부분
@app.route("/")
def index():
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    result = recommend_game()
    return render_template("result.html", result=result, time=now)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
