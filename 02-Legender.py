import os
import glob
import re
import unicodedata
import whisper

def slugify(value):
    """
    Aqui é pra transformar uma string em um formato amigável pros nomes dos arquivos.
    Antes dava erro então agr remove acentos, símbolos, espaços e deixa tudo em minúsculas, separando por hífens.
    """
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^a-zA-Z0-9\s-]', '', value)
    value = value.lower()
    value = re.sub(r'[\s]+', '-', value)
    value = re.sub(r'-+', '-', value)
    value = value.strip('-')
    return value

def seconds_to_timestamp(seconds):
    """
    Converter segundos pra Timestamp SRT: HH:MM:SS,mmm.
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    milliseconds = int((seconds - int(seconds)) * 1000)
    return f"{hours:02}:{minutes:02}:{secs:02},{milliseconds:03}"

def generate_subtitles(segments, max_words):
    """
    Aqui é pra gera a lista de legendas a partir dos segmentos do Whisper.
    No caso, cada segmento é subdividido em blocos com no máximo 'max_words' palavras.
    Os timestamps de cada bloco são calculados de forma proporcional dentro do segmento.
    
    Daí retorna uma lista de tuplas: (index, start_time, end_time, text)
    """
    subtitles = []
    index = 1
    for seg in segments:
        seg_start = seg.get("start", 0)
        seg_end = seg.get("end", 0)
        seg_text = seg.get("text", "").strip()
        if not seg_text:
            continue
        words = seg_text.split()
        n_chunks = (len(words) + max_words - 1) // max_words
        duration = seg_end - seg_start
        chunk_duration = duration / n_chunks if n_chunks > 0 else duration
        for i in range(n_chunks):
            chunk_words = words[i * max_words : (i + 1) * max_words]
            chunk_text = " ".join(chunk_words)
            chunk_start = seg_start + i * chunk_duration
            chunk_end = seg_start + (i + 1) * chunk_duration
            subtitles.append((index, chunk_start, chunk_end, chunk_text))
            index += 1
    return subtitles

def print_ascii_examples():
    example_sm = (
        "SM - Small (máximo 5 palavras por entrada):\n"
        "  +-----------------------------------------+\n"
        "  | 1                                       |\n"
        "  | 00:00:00,000 --> 00:00:02,000           |\n"
        "  | Iai galerinha, beleza?                  |\n"
        "  +-----------------------------------------+\n"
    )
    example_md = (
        "MD - Medium (máximo 10 palavras por entrada):\n"
        "  +-----------------------------------------+\n"
        "  | 1                                       |\n"
        "  | 00:00:00,000 --> 00:00:04,000           |\n"
        "  | Iai galerinha, aqui é um ex de legenda  |\n"
        "  +-----------------------------------------+\n"
    )
    example_lg = (
        "LG - Large (máximo 15 palavras por entrada):\n"
        "  +--------------------------------------------------+\n"
        "  | 1                                                |\n"
        "  | 00:00:00,000 --> 00:00:06,000                    |\n"
        "  | Inhai galerinha, blz? Esse aqui é um exemplo     |\n"
        "  | longo de legenda, com mais detalhes e palavras.  |\n"
        "  +--------------------------------------------------+\n"
    )
    print("Escolha o estilo das legendas:")
    print(example_sm)
    print(example_md)
    print(example_lg)

def process_videos():
    """
    Nessa parte o script processa todos os vídeos MP4 na pasta 'videos/'.
    01 - Pergunta ao usuário qual o estilo de legenda (SM, MD ou LG).
    02 - Transcreve o vídeo usando o Whisper e gera legendas no formato SRT.
    03 - Cada entrada de legenda vai ter no máximo o número de palavras definido pela opção escolhida.
    04 - O arquivo SRT é salvo na pasta 'legendas/' com o mesmo nome do vídeo (slugificado).
    """
    videos_folder = "01-videos"
    subtitles_folder = "02-legendas"
    
    if not os.path.exists(subtitles_folder):
        os.makedirs(subtitles_folder)
    
    print_ascii_examples()
    option = input("Escolha a opção desejada (SM/MD/LG): ").strip().upper()
    if option == "SM":
        max_words = 5
    elif option == "MD":
        max_words = 10
    elif option == "LG":
        max_words = 15
    else:
        print("Daí tu é cego, vou usar SM como padrão pq tu digitou besteira ai.")
        max_words = 5
    print(f"Estilo de legenda escolhido: {option} (máximo {max_words} palavras por entrada)")
    
    print("Carregando o tal do Whisper... aqui pode demorar na primeira execução (da pra passar um cafezinho por enquanto).")
    try:
        model = whisper.load_model("small")
    except Exception as e:
        print(f"Erro ao carregar o modelo Whisper: {e}. Verifique sua instalação e conexão com a internet.")
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
            output_filename = f"{slug_name}.srt"
            output_path = os.path.join(subtitles_folder, output_filename)
            
            result = model.transcribe(video_path)
            segments = result.get("segments", [])
            if not segments:
                print(f"Nenhum segmento encontrado pro {video_filename}.")
                continue
            
            subtitles = generate_subtitles(segments, max_words)
            
            with open(output_path, "w", encoding="utf-8") as f:
                for idx, start, end, text in subtitles:
                    f.write(f"{idx}\n")
                    f.write(f"{seconds_to_timestamp(start)} --> {seconds_to_timestamp(end)}\n")
                    f.write(f"{text}\n\n")
            
            print(f"Deu bom! Legenda gerada com sucesso: {output_filename}")
        except Exception as e:
            print(f"Erro ao processar {video_filename}: {e}. Da uma olhada se o FFmpeg tá instalado, se o arquivo tá corrompido ou se deu problema no Whisper. Se não for nd disso, abre uma issue que eu conserto.")

if __name__ == "__main__":
    process_videos()
