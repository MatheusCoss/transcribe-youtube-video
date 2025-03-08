from pytubefix import YouTube, Playlist
from pytubefix.cli import on_progress
from pydub import AudioSegment
import subprocess
from cleantext import clean
import os



def convert_m4a_to_mp3(from_file, to_file, format_1 = 'm4a', format_2 = 'mp3', verb=True):
    if verb:
        print("+ Convertando m4a para mp3 ")
    sound = AudioSegment.from_file(from_file, format=format_1)
    file_handle = sound.export(to_file, format=format_2)
    return file_handle


def donwload_high_video(path,yt,title):
    path += "/1080p"
    print("")
    print("+ Baixando faixa de video. ")
    if len(yt.streams.filter(res="1080p")) > 0:
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
    else:
        print(f"- Erro ao baixar {title} em alta resolução")


def donwload_youtube_video_audio(url, path, audio = False, highres = False, file_name = ""):
    yt = YouTube(url, on_progress_callback=on_progress)

    if file_name != "":
        title = clean_title_youtube(file_name)
    else:
        print("+ Limpando título.")
        title = clean_title_youtube(yt.title)

    if not audio:
        print(f"+ Baixando {yt.title}.mp4")
        if highres:
            donwload_high_video(path,yt,title)
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



def donwload_playlist(url,path,audio, playlist_folder, highres = False, convert_to_mp3 = False, main_audio_format = "m4a", convert_audio_format = "mp3"):
    folder = clean_title_youtube(playlist_folder)
    path += f"/{folder}"

    pl = Playlist(url)
    print(pl)
    videos_len = len(pl.videos)
    cont = 1
    for video in pl.videos:
        print(f"+ {cont}/{videos_len} Baixando {video.title} ")
        if audio:
            video_title = clean_title_youtube(video.title)
            ys = video.streams.get_audio_only()
            if ys != None:
                ys.download(output_path=path,filename=f"{video_title}.{main_audio_format}")

            if convert_to_mp3:
                main_path = f"{path}/{video_title}.{main_audio_format}"
                output_path = f"{path}/{video_title}.{convert_audio_format}"
                convert_m4a_to_mp3(main_path,output_path, verb=False)
                os.remove(main_path)

            
        else:
            video_title = clean_title_youtube(video.title)
            print(f"+ Baixando {video_title}")
            if highres:
                donwload_high_video(path,video,video_title)
            else:
                ys = video.streams.get_highest_resolution()
                ys.download(output_path=path, filename=f"{video_title}.mp4")

        cont += 1


def main():
    only_audio = True
    high_res = True
    convert_to_mp3 = True
    while True:
        path = "video_audio/"
        file_name = ""
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
            file_name = input("name> ") 

            if msg == "1":
                only_audio = False
                path += "videos"
                donwload_youtube_video_audio(url,path,only_audio,high_res, file_name=file_name)
            else:
                only_audio = True
                path += "audios"
                donwload_youtube_video_audio(url,path,only_audio, file_name=file_name)
        else:
            print("+ Por favor, não abuse :)")
            print("Digite a URL da Playlist.")
            url = input("URL> ")
            print("[1] Vídeo [2] Áudio")
            msg = input("> ")
            playlist_name = input("playlist_name> ") 

            
            if msg == "1":
                only_audio = False
                path += "videos"
                donwload_playlist(url,path,only_audio, playlist_folder=playlist_name, highres=high_res)
            else:
                only_audio = True
                path += "audios"
                donwload_playlist(url,path,only_audio, playlist_folder=playlist_name, convert_to_mp3=convert_to_mp3)




def combine_audio_video(path_video,path_audio,path_output):
    cmd = f'ffmpeg -y -i  {path_audio} -r 30 -i {path_video} -filter:a aresample=async=1 -c:a flac -c:v copy {path_output}'
    subprocess.call(cmd, shell=True) 



def clean_title_youtube(title):
    title = clean(title).replace(" ", "_").replace(".","").replace("/","").replace("-","").replace("&","")
    #print(f"+ titulo limpado para {title}")
    return title




if __name__ == '__main__':
    main()


