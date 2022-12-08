# Imports the Google Cloud Translation library
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="<JSON SECURITY KEY>"
from google.cloud import translate


# Initialize Translation client
def translate_text(text, project_id):
    """Translating Text."""

    client = translate.TranslationServiceClient()

    location = "global"

    parent = f"projects/{project_id}/locations/{location}"

    # Translate text from English to French
    # Detail on supported types can be found here:
    # https://cloud.google.com/translate/docs/supported-formats
    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",  # mime types: text/plain, text/html
            "source_language_code": "en-US",
            "target_language_code": "es-MX",
        }
    )

    # Display the translation for each input text provided
    for translation in response.translations:
        print("Translated text: {}".format(translation.translated_text))

def main():
    project_id='bq-experiments-350102'
    text='Use machine translation to detect more than one hundred languages, from Afrikaans to Zulu. Build custom models in more than fifty language pairs using our no-code AutoML technology.'
    translate_text(text, project_id)

if __name__ == "__main__":
    main()