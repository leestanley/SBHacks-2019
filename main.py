import datascience
from ytcc.download import Download
from textblob import TextBlob
from clarifai.errors import ApiError
from clarifai.rest import ClarifaiApp

myApi = '32256d518ae94e9597fe852eb356250a'
app = ClarifaiApp(api_key=myApi)

video_id = 'G1NCwU4advo'
download = Download()
captions = download.get_captions(video_id)
sentiment = TextBlob(captions)
print("Sentiment Score: ", sentiment.sentiment.polarity)

# m = app.public_models.general_model

# try:
#     response = m.predict_by_url('https://samples.clarifai.com/beer.mp4',
#                                 is_video=True,
#                                 sample_ms=1000)
# except ApiError as e:
#     print('Error status code: %d' % e.error_code)
#     print('Error description: %s' % e.error_desc)
#     if e.error_details:
#         print('Error details: %s' % e.error_details)
#     exit(1)

# frames = response['outputs'][0]['data']['frames']
# for frame in frames:
#     print('Concepts in frame at time: %d ms' % frame['frame_info']['time'])
#     for concept in frame['data']['concepts']:
#         print(' %s %f' % (concept['name'], concept['value']))
