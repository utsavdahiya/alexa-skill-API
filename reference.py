from __future__ import unicode_literals
from flask import Flask,jsonify,request,send_file
from flask_api import status
from flask_cors import CORS
import youtube_dl
import os
import requests

def invalid_request():
    response="Invalid Request"
    return response

def fix_name(fix_this):
    fix_this=fix_this.replace("|","_")
    fix_this=fix_this.replace("/","_")
    fix_this=fix_this.replace("\\","_")
    fix_this=fix_this.replace(")","_")
    fix_this=fix_this.replace("(","_")
    fix_this=fix_this.replace(" ","_")
    fix_this=fix_this.replace(".","_")
    fix_this=fix_this.replace("$","_")
    fix_this=fix_this.replace("%","_")
    return fix_this



def youtube(vid_id,quality):
    quality=str(int(quality)-100)
    vid_id=str(vid_id)
    url="https://www.youtube.com/watch?v="+str(vid_id)
    # file_name=vid_id+"_"+str(quality)+".mp3"
    if(not os.path.exists(os.getcwd()+"/data/")):
        os.system("mkdir data")
    strin="/root/ytomp3/data/"+vid_id+".mp3"




    ydl_opts = {'outtmpl':strin,
                'format': 'bestaudio/best',
                'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': quality,
                }],}
    # print("Downloading now")
    ofilename=""
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        try:
            info_dict = ydl.extract_info(str(url), download=False)
            video_title = fix_name(info_dict.get('title', None).replace(" ", "_"))
            ofilename=str(video_title)+str(vid_id)+"_ytomp3.mp3"

            strout="/usr/share/nginx/html/downloads/"+ofilename
            if(os.path.exists(strout)):
                response="http://ytomp3.xyz/downloads/"+ofilename
                return response

            ydl.download([str(url)])
        except:
            return invalid_request()

    # print("Download done")
    # print("Converting to mp3 now")

    os.system("ffmpeg -i "+strin+" -vn -b:a "+quality+"k -f mp3 "+strout)
    # os.system("sudo cp strin strout")
    os.system("sudo rm "+strin)
    # print("conversion done at: "+quality)
    response="http://ytomp3.xyz/downloads/"+ofilename
    return response




app = Flask(__name__)
CORS(app)
@app.route("/",methods=['GET'])
def index():
    vid_id=request.args.get('id')
    if(vid_id==""):
        return invalid_request()
    quality=request.args.get('quality')
    if(quality not in ['320','192']):
        return invalid_request()
    return youtube(vid_id,quality)

# def index():
#     os.system("ffmpeg")

if __name__=="__main__":
    app.run()
