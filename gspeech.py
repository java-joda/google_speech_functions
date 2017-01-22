import httplib2
from googleapiclient import discovery
from oauth2client.service_account import ServiceAccountCredentials
from pydub import AudioSegment

class SpeechRecognizer(object):
    """
    This class is not meant to be used in real-world apps. It's created just to test speech recognition quality.
    """

    def __init__(self, key_file=''):
        self.key_file = key_file  # path to json key file generated in Google Cloud Console
        self.access_point = None  # access point to get rights to interact with API
        self.audio_path = ''  # path to audio file (mp3)
        self._raw_file_path = ''  # path to decoded from .mp3 .raw file


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
        self.access_point = service

    def mp3_to_raw(self):
        """
        Convert file from mp3 to *raw
        """
        if not self.audio_path:
            raise Exception(
                'Nothing to convert! Specify a path to an *.mp3 file. Use SpeechRecognizer.audio_path parameter!')
        self._raw_file_path = self.audio_path[:-3] + 'raw'
        audiofile = AudioSegment.from_file(self.audio_path, "mp3")
        audiofile.export(self._raw_file_path, format="raw")


if __name__=="__main__":
    key_file = 'try-apis-b81f9aa58144.json'
    # print(getservice(key_file))
