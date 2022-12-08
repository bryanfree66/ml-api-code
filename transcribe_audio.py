import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="<JSON SECURITY KEY>"

def transcribe_file(gcs_uri):
    """Transcribe the given audio file asynchronously."""
    from google.cloud import speech

    client = speech.SpeechClient()

    #with open(speech_file, "rb") as audio_file:
     #   content = audio_file.read()

    """
     Note that transcription is limited to a 60 seconds audio file.
     Use a GCS file for audio longer than 1 minute.
    """
    audio = speech.RecognitionAudio(uri=gcs_uri)

    config = speech.RecognitionConfig(
        # encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        encoding=speech.RecognitionConfig.AudioEncoding.FLAC,
        audio_channel_count=2,
        sample_rate_hertz=8000,
        enable_separate_recognition_per_channel=True,
        model="phone_call",
        language_code="es-US",
        use_enhanced=True,
        enable_automatic_punctuation=True
    )


    operation = client.long_running_recognize(config=config, audio=audio)

    print("Waiting for operation to complete...")
    response = operation.result(timeout=180)

    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.
    for result in response.results:
        # The first alternative is the most likely one for this portion.
        print(u"Transcript: {}".format(result.alternatives[0].transcript))
        print("Confidence: {}".format(result.alternatives[0].confidence))

def main():
    speech_file = 'gs://ml-apis-demo/sample_phone/audio5.flac'
    transcribe_file(speech_file)

if __name__ == "__main__":
    main()