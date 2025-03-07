from pytubefix import YouTube
from pytubefix.cli import on_progress
from pydub import AudioSegment
import subprocess
from cleantext import clean
import os



def convert_m4a_to_mp3(from_file, to_file, format_1 = 'm4a', format_2 = 'mp3'):
    print("+ Convertando m4a para mp3 ")
    sound = AudioSegment.from_file(from_file, format=format_1)
    file_handle = sound.export(to_file, format=format_2)
    return file_handle



def donwload_youtube_video_audio(url, path, audio = False, highres = False):
    yt = YouTube(url, on_progress_callback=on_progress)
    if not audio:
        print(f"+ Baixando {yt.title}.mp4")
        if highres:
            path += "/1080p"
            
            print("+ Limpando título.")
            title = clean_title_youtube(yt.title)


            print("+ Baixando faixa de video. ")
            ys = yt.streams.filter(res="1080p")[0]
            ys.download(output_path=path, filename=f"{title}.mp4")

            print("+ Baixando faixa de audio. ")
            ys = yt.streams.get_audio_only()
            ys.download(output_path=path, filename=f"{title}.m4a")

            audio_path = f"{path}/{title}.m4a"
            video_path = f"{path}/{title}.mp4"

            

            output_path = f"{path}/{title}_1080p.mp4"
            print("+ Juntando faixa de video e audio.")
            combine_audio_video(video_path,audio_path,output_path)

            print("+ Removendo arquivo de audio.")
            os.remove(audio_path)
            print("+ Removendo arquivo de video.")
            os.remove(video_path)

            return title
        else:
            ys = yt.streams.get_highest_resolution()
            ys.download(output_path=path, filename=f"{title}.m4a")
            return title
    else:
        print(f"+ Baixando {yt.title}.m4a")
        ys = yt.streams.get_audio_only()
        title = clean_title_youtube(yt.title)
        ys.download(output_path=path, filename=f"{title}.m4a")
        return title

def main():
    path = "video_audio/"
    only_audio = True
    high_res = True
    while True:
        print("==============================")
        print("Youtube Downloader 1.5")
        print("[1] Vídeo [2] Playlist")
        print("==============================")
        msg = input("> ")
        if msg == "1":
            print("Digite primeiro a URL do vídeo.")
            url = input("URL> ")
            print("[1] Vídeo [2] Áudio")
            msg = input("> ")
            if msg == "1":
                only_audio = False
                path += "videos"
                donwload_youtube_video_audio(url,path,only_audio,high_res)
            else:
                only_audio = True
                path += "audios"
                donwload_youtube_video_audio(url,path,only_audio)
        else:
            print("- Não implementado")
            print("+ Por favor, não abuse :)")


def combine_audio_video(path_video,path_audio,path_output):
    cmd = f'ffmpeg -y -i  {path_audio} -r 30 -i {path_video} -filter:a aresample=async=1 -c:a flac -c:v copy {path_output}'
    subprocess.call(cmd, shell=True) 



def clean_title_youtube(title):
    title = clean(title).replace(" ", "_").replace(".","").replace("/","")
    return title




if __name__ == '__main__':
    main()


