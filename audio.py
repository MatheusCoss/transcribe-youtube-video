from pytubefix import YouTube
from pytubefix.cli import on_progress
from pydub import AudioSegment


def convert_m4a_to_mp3(from_file, to_file, format_1 = 'm4a', format_2 = 'mp3'):
    print("+ Convertando m4a para mp3 ")
    sound = AudioSegment.from_file(from_file, format=format_1)
    file_handle = sound.export(to_file, format=format_2)
    return file_handle



def donwload_youtube_video_audio(url, path, audio = False):
    yt = YouTube(url, on_progress_callback=on_progress)
    if not audio:
        print(f"+ Baixando {yt.title}.mp4")
        ys = yt.streams.get_highest_resolution()
        ys.download(output_path=path)
        return yt.title
    else:
        print(f"+ Baixando {yt.title}.m4a")
        ys = yt.streams.get_audio_only()
        ys.download(output_path=path)
        return yt.title

def main():
    path = "video_audio/audios"
    only_audio = True
    with True:
        print("Youtube Downloader 1.0")
        print("[1] video [2] playlist")
        msg = input("> ")
        if msg == "1":
            print("Digite primeiro a URL do video")
            url = input("URL> ")
            print("[1] video [2] audio")
            msg = input("> ")
            if msg == "1":
                only_audio = False
                file_name = donwload_youtube_video_audio(url,path,only_audio)
            else:
                only_audio = True
                file_name = donwload_youtube_video_audio(url,path,only_audio)
        else:
            print("- Não implementado")


if __name__ == '__main__':
    main()


