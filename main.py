from audio import convert_m4a_to_mp3, donwload_youtube_video_audio
from transcription import transquever_video, salvar_em_arquivo, formatar_texto, get_text_from_path




def main():
    path = "video_audio/audios"
    path_trans = "texts/"
    main_format = "m4a"
    convert_format = "mp3"
    device = "cuda"
    model = "small"
    translate = True
    while True:
        print("Transcritor de video do Youtube 1.0")
        print("Digite primeiro a URL do video")
        url = input("URL> ")
        file_name = donwload_youtube_video_audio(url,path,True)
        output_path = f"{path}/{file_name}.{convert_format}"
        convert_m4a_to_mp3(f"{path}/{file_name}.{main_format}",output_path, format_1=main_format, format_2=convert_format)
        trans_raw_path = f"{path_trans}{file_name}_raw.txt"
        resp = transquever_video(output_path,device,model)
        salvar_em_arquivo(trans_raw_path, resp)
        saida_formatada = trans_raw_path
        saida_formatada = saida_formatada.replace(".txt","_formatado.txt")
        format_text = formatar_texto(get_text_from_path(trans_raw_path),  translate=translate)
        salvar_em_arquivo(saida_formatada,format_text)


if __name__ == '__main__':
    main()