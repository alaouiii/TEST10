from flask import Flask, request, render_template
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def extract_media(instagram_url):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    try:
        res = requests.get(instagram_url, headers=headers)
        soup = BeautifulSoup(res.text, "html.parser")

        media_url = None
        is_video = False

        # Check for video first
        video_tag = soup.find("meta", property="og:video")
        if video_tag:
            media_url = video_tag["content"]
            is_video = True
        else:
            image_tag = soup.find("meta", property="og:image")
            if image_tag:
                media_url = image_tag["content"]

        return media_url, is_video
    except Exception as e:
        return None, False

@app.route("/", methods=["GET", "POST"])
def index():
    media_url = None
    is_video = False
    if request.method == "POST":
        ig_url = request.form.get("ig_url")
        media_url, is_video = extract_media(ig_url)
    return render_template("index.html", media_url=media_url, is_video=is_video)

if __name__ == "__main__":
    app.run(debug=True)
