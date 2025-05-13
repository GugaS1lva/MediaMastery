import os
import glob
import re
import unicodedata
import whisper

def slugify(value):
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^a-zA-Z0-9\s-]', '', value)
    value = value.lower()
    value = re.sub(r'[\s]+', '-', value)
    value = re.sub(r'-+', '-', value)
    value = value.strip('-')
    return value

def process_videos():
    videos_folder = "i-videos"
    texts_folder = "iii-textos"
    
    if not os.path.exists(texts_folder):
        os.makedirs(texts_folder)
    
    print("Carregando o tal do Whisper... aqui pode demorar na primeira execução (da pra passar um cafezinho por enquanto).")
    try:
        model = whisper.load_model("small")
    except Exception as e:
        print(f"Erro ao carregar o Whisper: {e}. Confere a instalação e a conexão com a internet.")
        return
    
    video_files = glob.glob(os.path.join(videos_folder, "*.mp4"))
    if not video_files:
        print("Não achei nenhum vídeo na pasta 'videos'. Dá uma conferida aí, patrão!")
        return
    
    for video_path in video_files:
        video_filename = os.path.basename(video_path)
        print(f"Processando vídeo: {video_filename}")
        try:
            base_name, _ = os.path.splitext(video_filename)
            slug_name = slugify(base_name)
            output_filename = f"{slug_name}.md"
            output_path = os.path.join(texts_folder, output_filename)
            
            result = model.transcribe(video_path)
            transcript = result.get("text", "")
            
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(f"# Transcrição do vídeo: {video_filename}\n\n")
                f.write(transcript)
            
            print(f"Deu bom! Legenda gerada com sucesso: {output_filename}")
        except Exception as e:
            print(f"Erro ao processar {video_filename}: {e}. Da uma olhada se o FFmpeg tá instalado, se o arquivo tá corrompido ou se deu problema no Whisper. Se não for nd disso, abre uma issue que eu conserto.")

if __name__ == "__main__":
    process_videos()
