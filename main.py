import youtube_dl
import string
import threading
import loguru


class YoutubeVideo:
    """Asynchronous downloading video or sound series and save to mp3 files.
        args:
            - url_list_file: .txt file name of video urls
            - keepvideo: set to False if you need to download audio only.
        method:
            - start_load: Read .txt file and start loading video
            - download_video: Method to simply download video from video_url
        """

    def __init__(self, url_list_file: str = None, keep_video: bool = True) -> None:
        self.url_list_file: str = url_list_file
        self.keep_video: bool = keep_video
        self._thread_list: list = self.__create_treads_list()
        self.result: dict[str, int] = {
            'success': 0,
            'errors': 0
        }

    def start(self):
        if len(self._thread_list):
            for thread in self._thread_list:
                thread.start()
            for thread in self._thread_list:
                thread.join()

    def download_video(self, video_url: str) -> bool:
        """
        Download video or sound series and save to mp3 file
            - video_url: url for video like https://www.youtube.com/watch?v=78PTvj2wYH8&ab_channel=selfedu
        """
        try:
            video_info = youtube_dl.YoutubeDL().extract_info(
                url=video_url,
                download=False
            )
        except Exception as e:
            self.result['errors'] += 1
            loguru.logger.error(e)
            return False

        else:
            filename = self.prepare_filename(video_info["title"])
            options = {
                'format': 'bestaudio/best',
                'keepvideo': self.keep_video,
                'outtmpl': filename
            }

            with youtube_dl.YoutubeDL(options) as ydl:
                ydl.download([video_info['webpage_url']])

            loguru.logger.info(f'Download {filename} complete.')
            self.result['success'] += 1
            return True

    def __create_treads_list(self) -> list:
        if self.url_list_file is None:
            return []
        with open(self.url_list_file, 'r') as f:
            return [threading.Thread(target=self.download_video, args=(video_url,)) for video_url in f.readlines()]

    @staticmethod
    def prepare_filename(text: str) -> str:
        """Returns the name of the file without punctuation marks at the beginning of the name or '_' in the middle"""
        symbols = string.punctuation + string.whitespace
        for _ in range(len(text)):
            if text[0] not in string.punctuation:
                break
            text = text[1:]
        filename = ''.join(list(map(lambda x: x if x not in symbols else '_', text)))
        return f'{filename}.mp3'


if __name__ == '__main__':
    file = 'video_url_list.txt'
    loader = YoutubeVideo(url_list_file=file)
    loader.start()
    loguru.logger.info(f'Loaded {loader.result["success"]} video, errors: {loader.result["errors"]}')
