import base64
import json
import time

import httplib2
import pydub
from googleapiclient import discovery
from oauth2client.service_account import ServiceAccountCredentials
from pydub import AudioSegment
from pydub.silence import split_on_silence

pydub.AudioSegment.ffmpeg = r"E:\tools\ffmpeg\bin"

class SpeechRecognizer(object):
    """
    This class is not meant to be used in real-world apps. It's created just to test speech recognition quality.
    """

    def __init__(self, key_file=''):
        self.key_file = key_file  # path to json key file generated in Google Cloud Console
        self.audio_path = ''  # path to audio file (mp3)
        self.chunks = []  # path to decoded from .mp3 .raw file


    def getservice(self):
        """
        This goes through an authentification process.
        """
        scope = ['https://www.googleapis.com/auth/cloud-platform']  # Scope where this acces point grants predefined
        # rights (default value for Google Speech API)
        try:
            credentials = ServiceAccountCredentials.from_json_keyfile_name(self.key_file, scope)
            http = credentials.authorize(httplib2.Http())
            service = discovery.build('speech', 'v1beta1', http=http)
        except Exception as ex:
            print(ex)
            return
        print(service)
        return service

    def mp3_to_raw(self):
        """
        Convert file from mp3 to *raw
        """

        if not self.audio_path:
            raise Exception(
                'Nothing to convert! Specify a path to an *.mp3 file. Use SpeechRecognizer.audio_path parameter!')
        print(self.audio_path)
        self._raw_file_path = self.audio_path[:-4]
        print(self._raw_file_path)
        audiofile = AudioSegment.from_file(self.audio_path, "mp3")
        silence_threshold = audiofile.rms
        print(silence_threshold)
        chunks = split_on_silence(audiofile,
                                  # must be silent for at least half a second
                                  min_silence_len=200,

                                  # consider it silent if quieter than -16 dBFS
                                  silence_thresh=-16
                                  )
        # print(detect_silence(audiofile,
        #                           # must be silent for at least half a second
        #                           min_silence_len=200,
        #
        #                           # consider it silent if quieter than -16 dBFS
        #                           silence_thresh=-16
        #                           ))
        print(chunks)
        for i, chunk in enumerate(chunks):
            print(i)
            self.chunks.append("{0}_{1}.raw".format(self._raw_file_path, i))
            chunk.export("{0}_{1}.raw".format(self._raw_file_path, i), format="raw")
            print(self.chunks)

    def recognize(self):

        for chunk in self.chunks:
            with open(chunk, 'rb') as speech:
                # Base64 encode the binary audio file for inclusion in the request.
                speech_content = base64.b64encode(speech.read())

            service = self.getservice()

            service_request = service.speech().asyncrecognize(
                body={
                    'config': {
                        # There are a bunch of config options you can specify. See
                        # https://goo.gl/KPZn97 for the full list.
                        'encoding': 'LINEAR16',  # raw 16-bit signed LE samples
                        'sampleRate': 16000,  # 16 khz
                        # See http://g.co/cloud/speech/docs/languages for a list of
                        # supported languages.
                        'languageCode': 'ru-RU',  # a BCP-47 language tag
                    },
                    'audio': {
                        'content': speech_content.decode('UTF-8')
                    }
                }
            )
            response = service_request.execute()
            print(json.dumps(response))
            name = response['name']
            service_request = service.operations().get(name=name)

            while True:
                # Give the server a few seconds to process.
                print('Waiting for server processing...')
                time.sleep(1)
                # Get the long running operation with response.
                response = service_request.execute()
                print(response)
                if 'done' in response and response['done']:
                    break

            print(json.dumps(response['response']))

            with open(chunk[:-3] + '.json', 'w') as f:
                print(chunk[:-3] + '.json')
                f.write(json.dumps(response))


if __name__=="__main__":
    key_file = 'try-apis-b81f9aa58144.json'
    sr = SpeechRecognizer(key_file)
    sr.audio_path = r'audio\1.mp3'
    sr.mp3_to_raw()
    sr.recognize()
    # print(getservice(key_file))
