from flask import Flask, render_template
import datetime

app = Flask(__name__)

@app.route("/")
def index():
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return render_template("result.html", result="이곳에 추천 게임 결과가 표시됩니다!", time=now)

if __name__ == "__main__":
    app.run()
