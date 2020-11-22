from django.conf import settings
import requests


# the Google Translate API Endpoint. Leave it, should work
TRANSLATEAPIENDPOINT = 'https://translation.googleapis.com/language/translate/v2'


# simple google translation API call
# Can be used to translate the given text from "srcLan" (ISO-Code of source Language, i.E. "de" for german)
# to dstLan (ISO-Code of destination Language)
#
# Attention: to get this working, you have to set GOOGLEAPIKEY in settings.py or better in settings_local.py
# (see settings_local_template.py)
#
# If there is an error, this method returns None
def simpleGoogleTranslate(text, srcLan, dstLan):
    if srcLan == dstLan:
        # translate from same language to same langage ==> do nothing, just return given text
        return text

    # check if text is useful (i.E. not empty and not None)
    if text == None:
        return None

    # remove unnecessary whitespaces in front of or at end of text
    text = text.strip()
    if text == "":
        return None

    # fill data as required form google-translate-rest-api-call
    data = {'q': text, 'source': srcLan, 'target': dstLan, 'format': 'text'}

    # call api
    r = requests.post(TRANSLATEAPIENDPOINT + '?key=' + settings.GOOGLEAPIKEY, json=data)

    # parse result and check if result was ok
    result = r.json()
    if result['data'] and result['data']['translations'] and result['data']['translations'][0] and result['data']['translations'][0]['translatedText']:
        return result['data']['translations'][0]['translatedText']

    # no good result returned from api
    return None



