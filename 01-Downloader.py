import yt_dlp
import re

def baixar_video(url):
    try:
        ydl_opts = {
            'format': 'best',
            'outtmpl': 'i-videos/%(title)s.%(ext)s',
            'socket_timeout': 30,   # tempo em segundos (aumente se tiver quebrando)
            # 'retries': 3          # número de tentativas, caso continue
        }
        
        pattern = re.compile(r'https://(www\.youtube\.com|youtu\.be)/.*')
        if not pattern.search(url):
            print("Tá dando ruim aqui, põe a url direito, pô.")
            return

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        print("Download concluído!")

    except Exception as e:
        print("Deu ruim mermo:", e)

# Download vídeos únicos.
urls = ["https://www.youtube.com/live/pGrriYmvF4A"]

# Download vídeos multiplos.    
# urls = [
#     "https://youtu.be/bSR-iWChMhs?si=mT-VYygghXPonIIB",
#     "https://www.youtube.com/live/WtVI5mLHjtE",
#     "https://www.youtube.com/watch?v=AjwjN3xFDr8"
# ]

for url in urls:
    baixar_video(url)
