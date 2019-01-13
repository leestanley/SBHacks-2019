from ytcc.download import Download
from textblob import TextBlob
from clarifai.errors import ApiError
from clarifai.rest import ClarifaiApp
from pytube import YouTube
import operator
import os
from flask import Flask, url_for, render_template, request, jsonify
from flask import *

myApi = '32256d518ae94e9597fe852eb356250a'
clarifail = ClarifaiApp(api_key=myApi)
model = clarifail.public_models.general_model

app = Flask(__name__)


@app.route('/')  # home page
def home():
    return render_template('index.html')


@app.route('/results')
def results():
    link = request.args['inputname']
    SAVE_PATH = "C:/Users/Stanley/Desktop/SBHacks-2019/videos"
    yt = YouTube(link)
    stream = yt.streams.filter(file_extension='mp4').first()
    stream.download(SAVE_PATH)
    title = yt.title + ".mp4"
    title = title.replace("|", "")
    title = title.replace(":", "")

    arraylink = link.split("=")
    video_id = arraylink[1]
    download = Download()
    captions = download.get_captions(video_id)
    sentiment = TextBlob(captions)
    captions = captions.replace("[Music]", "")
    captions = captions.replace("  ", ". ")
    score = sentiment.sentiment.polarity
    score = str(score)

    m = clarifail.public_models.general_model
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

    total_concepts = {}
    frames = response['outputs'][0]['data']['frames']
    for frame in frames:
        print('Concepts in frame at time: %d ms' % frame['frame_info']['time'])
        for concept in frame['data']['concepts']:
            print(' %s %f' % (concept['name'], concept['value']))
            if concept['name'] in total_concepts.keys():
                total_concepts[concept['name']] += concept['value']
            else:
                total_concepts[concept['name']] = concept['value']

    final = sorted(total_concepts.items(), key=operator.itemgetter(1), reverse=True)

    for x in range(5):
        print(final[x])
    return render_template('results.html', content1=captions, content2=score, content3=str(final[0][0]), content4=str(final[1][0]), content5=str(final[2][0]), content6=str(final[3][0]), content7=str(final[4][0]))


if __name__ == "__main__":
    app.run(port=5036, debug=True)
