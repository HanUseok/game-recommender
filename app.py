from flask import Flask, render_template
import datetime
import gspread
import json
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

# 구글시트 인증
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

with open("/etc/secrets/credentials.json") as f:
    creds_json = json.load(f)

creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_json, scope)
client = gspread.authorize(creds)

# 시트 ID (이미 네가 공유한 링크에서 가져온 거야)
sheet_url = "https://docs.google.com/spreadsheets/d/1hvAVXcmJJ2hY9UToV500KwHepmyrnfxH8G4aOt_48Xo"
sheet = client.open_by_url(sheet_url).worksheet("Form Responses 1")

@app.route("/")
def index():
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 최신 응답 한 줄 가져오기
    data = sheet.get_all_records()
    if not data:
        result_text = "아직 제출된 설문이 없습니다."
    else:
        latest = data[-1]
        # 간단한 조건으로 예시 추천 로직 작성
        genre = latest.get("좋아하는 게임 장르르 선택해주세요 (여러개 선택 가능)", "")
        platform = latest.get("주로 어떤 플랫폼으로 게임을 하시나요?", "")
        reason = latest.get("그 게임에서 어떤 점이 재미있었는지 간단하게 적어주세요!  (위 질문에 답하신 분만)", "")

        # 간단한 추천 결과 문자열 만들기
        result_text = f"{genre} 장르를 좋아하고 {platform} 플랫폼을 주로 사용하는 당신께 추천하는 게임은... 🎯 <br><br> ➤ '{reason}'와 비슷한 재미를 가진 게임입니다!"

    return render_template("result.html", result=result_text, time=now)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
