import yt_dlp
import re

def baixar_video(url):
    try:
        ydl_opts = {
            'format': 'best',
            'outtmpl': '01-videos/%(title)s.%(ext)s',
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
        print("Deu um erro:", e)

# Download single videos.
urls = ["https://www.youtube.com/watch?v=HNV3vSOUkew"]

# Download multiple videos.    
# urls = [
#     "https://youtu.be/bSR-iWChMhs?si=mT-VYygghXPonIIB",
#     "https://www.youtube.com/live/WtVI5mLHjtE",
#     "https://www.youtube.com/watch?v=AjwjN3xFDr8"
# ]

for url in urls:
    baixar_video(url)
 
# test url video below
# https://www.youtube.com/watch?v=EF889gHjZu8