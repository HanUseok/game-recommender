from flask import Flask, render_template
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
import pandas as pd
import datetime

app = Flask(__name__)

# 구글 시트 연결 설정
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
with open("/etc/secrets/credentials.json") as f:
    creds_json = json.load(f)

creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_json, scope)
client = gspread.authorize(creds)

# 너의 설문 데이터가 있는 시트 URL
SPREADSHEET_URL = "https://docs.google.com/spreadsheets/d/1hvAVXcmJJ2hY9UToV500KwHepmyrnfxH8G4aOt_48Xo/edit#gid=0"
spreadsheet = client.open_by_url(SPREADSHEET_URL)
worksheet = spreadsheet.worksheet("Form Responses 1")  # 시트 이름 확인 필요

@app.route("/")
def index():
    # 최신 응답 가져오기
    data = worksheet.get_all_values()
    headers = data[0]
    latest = data[-1]
    response = dict(zip(headers, latest))

    # 간단한 로직 예시 (실제 추천 로직은 여기서 고도화)
    genre = response.get("좋아하는 게임 장르를 선택해주세요 (여러개 선택 가능)")
    playtime = response.get("평균적으로 한 번 게임할 때 몇 분 정도 플레이하시나요?")

    # 아주 간단한 추천 예시 (실제에선 dataframe 기반 추천으로 확장 가능)
    if "RPG" in genre:
        recommendations = ["드래곤 퀘스트 XI", "페르소나 5", "이스 VIII"]
    elif "FPS" in genre:
        recommendations = ["타이탄폴 2", "레인보우 식스 시즈", "메트로 엑소더스"]
    else:
        recommendations = ["언더테일", "슬레이 더 스파이어", "그림폰트"]

    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return render_template("result.html", result=recommendations, time=now)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
