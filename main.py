"""Synthesizes speech from the input string of text or ssml.

Note: ssml must be well-formed according to:
    https://www.w3.org/TR/speech-synthesis/
"""
from google.cloud import texttospeech
"""Synthesizes speech from the input string of text or ssml.

Note: ssml must be well-formed according to:
    https://www.w3.org/TR/speech-synthesis/
"""
# Imports the Google Cloud client library
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
from google.cloud import texttospeech
import os
import argparse
import io
from textblob import TextBlob
from gensim.summarization import summarize

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:/Users/Stanley/Desktop/Crazedwish-70948e48553e.json"

# Imports the Google Cloud client library
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types

# Instantiates a client
client = speech.SpeechClient()

# The name of the audio file to transcribe
file_name = os.path.join(
    os.path.dirname(__file__),
    'C:/Users/Stanley/Desktop/HardHacks2019/Not Everyone Should Code.flac')

# Loads the audio into memory
# with io.open(file_name, 'rb') as audio_file:
#     content = audio_file.read()
#     audio = types.RecognitionAudio(content=content)

# config = types.RecognitionConfig(
#     encoding=enums.RecognitionConfig.AudioEncoding.FLAC,
#     language_code='en-US',
#     enable_automatic_punctuation=True)


def transcribe_gcs(gcs_uri):
    """Asynchronously transcribes the audio file specified by the gcs_uri."""
    from google.cloud import speech
    from google.cloud.speech import enums
    from google.cloud.speech import types
    client = speech.SpeechClient()

    audio = types.RecognitionAudio(uri=gcs_uri)
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.FLAC,
        enable_automatic_punctuation=True,
        language_code='en-US')

    operation = client.long_running_recognize(config, audio)

    print('Waiting for operation to complete...')
    response = operation.result(timeout=600)

    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.
    total = ""
    for result in response.results:
        # The first alternative is the most likely one for this portion.
        print(u'Transcript: {}'.format(result.alternatives[0].transcript))
        print('Confidence: {}'.format(result.alternatives[0].confidence))
        total += format(result.alternatives[0].transcript)
    return total
    # [END speech_python_migration_async_response]
# [END speech_transcribe_async]


# # Detects speech in the audio file
# response = client.recognize(config, audio)
total = transcribe_gcs('gs://hardhacks/Not Everyone Should Code1.flac')

sentiment = TextBlob(total)
score = sentiment.sentiment.polarity

total = summarize(total)

# Instantiates a client
client = texttospeech.TextToSpeechClient()

# Set the text input to be synthesized
if score < .2:
    score = 'Very Objective'
elif score < .4:
    score = 'Objective'
elif score < .6:
    score = 'Neutral'
elif score < .8:
    score = 'Subjective'
else:
    score = 'Very Subjective'

synthesis_input = texttospeech.types.SynthesisInput(text="Sentiment Subjectivity Analysis." + score + "." + "NLP Summary Codensed by 33%." + total)

# Build the voice request, select the language code ("en-US") and the ssml
# voice gender ("neutral")
voice = texttospeech.types.VoiceSelectionParams(
    language_code='en-US',
    ssml_gender=texttospeech.enums.SsmlVoiceGender.NEUTRAL)

# Select the type of audio file you want returned
audio_config = texttospeech.types.AudioConfig(
    audio_encoding=texttospeech.enums.AudioEncoding.MP3)

# Perform the text-to-speech request on the text input with the selected
# voice parameters and audio file type
response = client.synthesize_speech(synthesis_input, voice, audio_config)

# The response's audio_content is binary.
with open('output.mp3', 'wb') as out:
    # Write the response to the output file.
    out.write(response.audio_content)
    print('Audio content written to file "output.mp3"')
os.system("C:/Users/Stanley/Desktop/HardHacks2019/output.mp3")
