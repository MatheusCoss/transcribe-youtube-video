from audio import convert_m4a_to_mp3, donwload_youtube_video_audio
from transcription import transcribe_video, save_to_flie, format_text, get_text_from_path
import torch



def main():
    path = "video_audio/audios"
    path_trans = "texts/"
    main_format = "m4a"
    convert_format = "mp3"
    device = "cuda"
    model = "small"
    translate = False
    only_audio = True

    if torch.cuda.is_available():
        while True:
            print("Transcritor de video do Youtube 1.0")
            print("Digite primeiro a URL do video")
            url = input("URL> ")
            file_name = donwload_youtube_video_audio(url,path,only_audio)
            output_path = f"{path}/{file_name}.{convert_format}"
            convert_m4a_to_mp3(f"{path}/{file_name}.{main_format}",output_path, format_1=main_format, format_2=convert_format)
            trans_raw_path = f"{path_trans}{file_name}_raw.txt"
            resp = transcribe_video(output_path,device,model)
            save_to_flie(trans_raw_path, resp)
            saida_formatada = trans_raw_path
            saida_formatada = saida_formatada.replace(".txt","_formatado.txt")
            final_text= format_text(get_text_from_path(trans_raw_path),  translate=translate)
            save_to_flie(saida_formatada,final_text)
    else:
        print("- Cuda não está disponivel")


if __name__ == '__main__':
    main()