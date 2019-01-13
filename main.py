from ytcc.download import Download
from textblob import TextBlob
from clarifai.errors import ApiError
from clarifai.rest import ClarifaiApp
from pytube import YouTube
import os
from flask import Flask, url_for, render_template, request, jsonify
from flask import *

app = Flask(__name__)

SAVE_PATH = "C:/Users/Stanley/Desktop/SBHacks-2019/videos"
link = "https://www.youtube.com/watch?v=kt09W17edIk"
yt = YouTube(link)
stream = yt.streams.filter(file_extension='mp4').first()
stream.download(SAVE_PATH)
title = yt.title + ".mp4"
title = title.replace("|", "")
title = title.replace(":", "")

myApi = '32256d518ae94e9597fe852eb356250a'
app = ClarifaiApp(api_key=myApi)

arraylink = link.split("=")
video_id = arraylink[1]
download = Download()
captions = download.get_captions(video_id)
sentiment = TextBlob(captions)
captions = captions.replace("[Music]", "")
captions = captions.replace("  ", ". ")
print(captions)
print("Sentiment Score: ", sentiment.sentiment.polarity)
print(title)

m = app.public_models.general_model
try:
    response = m.predict_by_filename("C:/Users/Stanley/Desktop/SBHacks-2019/videos/" + title,
                                     is_video=True,
                                     sample_ms=10000)
except ApiError as e:
    print('Error status code: %d' % e.error_code)
    print('Error description: %s' % e.error_desc)
    if e.error_details:
        print('Error details: %s' % e.error_details)
    exit(1)

frames = response['outputs'][0]['data']['frames']
for frame in frames:
    print('Concepts in frame at time: %d ms' % frame['frame_info']['time'])
    for concept in frame['data']['concepts']:
        print(' %s %f' % (concept['name'], concept['value']))
