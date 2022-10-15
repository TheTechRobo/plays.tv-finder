from flask import *
import requests, subprocess, json, re

app = Flask(__name__)

@app.route("/")
async def start():
    return """
    <form action="/get">
        <input name="username" id="username">
        <label for="username">Username</label>
    </form>
    """

@app.route("/get")
async def getRender():
    id = request.args.get("username") or abort(400)
    video_list = requests.get("https://recoverplays.tv/GetUserInfo.php?username=Natopotato&sort=date").json()
    video_ids = []
    for video in video_list[1]:
        #rawdll = requests.get(f"https://web.archive.org/web/20191210043532/https://plays.tv/video/{id}").text
        #matched_lines = [line for line in rawdll.split('\n') if "720.mp4" in line]
        #assert len(matched_lines) == 1
        #p = Popen(["grep", "-Po", 'src="\k[^"]+/720\.mp4(?=")'], stdin=PIPE, stdout=PIPE)
        #dll = p.communicate(input=matched_lines[0])[0]
        video_ids.append({'id': video['id'], 'title': f"{video['name']}, {video['date']}"})
    return render_template("render.html", ids=video_ids, len=len)

@app.route("/get/<videoid>")
async def get(videoid):
    rawdll = requests.get(f"http://web.archive.org/web/20191210043532id_/https://plays.tv/video/{videoid}").text
    matched_lines = [line for line in rawdll.split('\n') if "720.mp4" in line]
    assert len(matched_lines) == 1
    dll = re.sub(
           "^//",
           "https://",
           re.search('src=\"([^\"]+/720\.mp4)(?=\")', matched_lines[0]).group(1)
    )
    return {"lien": dll, "isOk": True}
