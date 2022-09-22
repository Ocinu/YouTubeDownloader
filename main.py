import youtube_dl
import string


def read_url_list():
    with open('video_url_list.txt', 'r') as f:
        for line in f.readlines():
            print(line)


def download_video(video_url: str) -> None:
    video_info = youtube_dl.YoutubeDL().extract_info(
        url=video_url,
        download=False
    )
    filename = prepare_filename(video_info["title"])
    options = {
        'format': 'bestaudio/best',
        'keepvideo': True,
        'outtmpl': filename
    }

    with youtube_dl.YoutubeDL(options) as ydl:
        ydl.download([video_info['webpage_url']])

    print(f'Download {filename} complete.')


def prepare_filename(text: str) -> str:
    symbols = string.punctuation + string.whitespace
    for _ in range(len(text)):
        if text[0] not in string.punctuation:
            break
        text = text[1:]
    filename = ''.join(list(map(lambda x: x if x not in symbols else '_', text)))
    return f'{filename}.mp3'


if __name__ == '__main__':
    url = '!@##$%&^&&(&(https://www.youtube.com/watch?v=78PTvj2wYH8&ab_channel=selfedu'
    #download_video(url)
    read_url_list()
