import datascience
from ytcc.download import Download
from textblob import TextBlob
from clarifai.errors import ApiError
from clarifai.rest import ClarifaiApp
from pytube import YouTube

SAVE_PATH = "C:/Users/Stanley/Desktop/SBHacks-2019/videos"
link = "https://www.youtube.com/watch?v=oBuntAGseyk"
try:
    # object creation using YouTube which was imported in the beginning
    yt = YouTube(link)
    print("Success")
except:
    print("Connection Error")  # to handle exception
stream = yt.streams.filter(file_extension='mp4').first()
stream.download(SAVE_PATH)
title = yt.title

myApi = '32256d518ae94e9597fe852eb356250a'
app = ClarifaiApp(api_key=myApi)

arraylink = link.split("=")
print(arraylink)
video_id = 'oBuntAGseyk'
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
    response = m.predict_by_filename('C:/Users/Stanley/Desktop/SBHacks-2019/videos/' + title,
                                     is_video=True,
                                     sample_ms=1000)
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
