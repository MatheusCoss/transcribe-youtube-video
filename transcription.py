import whisper
import torch
from cleantext import clean
import translators

def transcribe_video(path,device,model):
    
    
    if torch.cuda.is_available():
        print(f"+ Carregando o modelo {model} com Cuda..")
        modelo = whisper.load_model(model, device=device)
        print("+ Modelo carregado, transcrevendo..")
        resposta = modelo.transcribe(path)
        print("+ Transcrição feita.")
        return resposta['text']
    else:
        print("Cuda não está disponível")
        return False

def save_to_flie(path, text):
    with open(path,'w', encoding="utf-8") as f:
        f.write(text)

def translate_text(text,translator = "google",from_language = "en",to_language = "pt"):
    text = translators.translate_text(text,translator,from_language,to_language)
    return text

def get_text_from_path(path):
    print("+ Pegando o texto bruto da transcrição")
    with open(path, "r") as f:
        text = f.read()
        return text


def format_text(raw, translate = False):
    text = ""
    print("+ Separando o texto por setenças.")
    raw_text = raw.split(". ")
    len_text = len(raw_text)
    cont = 0
    for sentence in raw_text:
        try:
            sentence = clean(sentence, fix_unicode=True, to_ascii=True)
            if not translate:
                text += f"{sentence}.\n"
                text += "\n"
            else:
                if sentence != None:
                    text += f"{translate_text(sentence)}.\n"
                    text += "\n"
            cont += 1
            print(f"+ {cont}/{len_text} setenças feitas..")
        except Exception as e:
            print(f"- Erro na setença: {sentence}, indo para a próxima..")

    return text


