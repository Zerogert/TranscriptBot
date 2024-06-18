import requests
import urllib.parse
import config


def get_transcript(url):
    host = config.transcript_service_host
    params = {'url': url}
    response = requests.get(host + '/transcripts' + urllib.parse.urlencode(params))

    return response.text
