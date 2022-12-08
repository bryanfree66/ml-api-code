# Use dict to define document.
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="<JSON SECURITY KEY>"

from google.cloud import language

client = language.LanguageServiceClient()

document = {'gcs_content_uri': 'gs://ml-apis-demo/text/sentiment-negative.txt',
            'language':'en',
            'type_':'PLAIN_TEXT'}

response = client.analyze_sentiment(request={'document': document})

# Get overall sentiment of the input document
print(f"    Document sentiment score: {response.document_sentiment.score}")
print(f"Document sentiment magnitude: {response.document_sentiment.magnitude}\n")

# Get sentiment for all sentences in the document
for sentence in response.sentences:
    print(f"               Sentence text: '{sentence.text.content}'")
    print(f"    Sentence sentiment score: {sentence.sentiment.score}")
    print(f"Sentence sentiment magnitude: {sentence.sentiment.magnitude}")