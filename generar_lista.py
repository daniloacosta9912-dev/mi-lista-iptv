import subprocess
import urllib.request
import re
from datetime import datetime

# 1. TUS CANALES DE YOUTUBE (Prioridad local)
CANALES_YOUTUBE = [
    {"nombre": "ElTrece", "grupo": "AR - Aire", "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6e/El_Trece_logo.svg/200px-El_Trece_logo.svg.png", "url": "https://www.youtube.com/@eltrece/live"},
    {"nombre": "Telefe", "grupo": "AR - Aire", "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3c/Telefe_2019.svg/200px-Telefe_2019.svg.png", "url": "https://www.youtube.com/@Telefe/live"},
    {"nombre": "TN", "grupo": "AR - Noticias", "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1f/TN-Todo-Noticias-2018.svg/200px-TN-Todo-Noticias-2018.svg.png", "url": "https://www.youtube.com/@todonoticias/live"},
]

# 2. FUENTES EXTERNAS
FUENTES_M3U = [
    # === ARGENTINA ===
    "https://iptv-org.github.io/iptv/countries/ar.m3u",

    # === LISTAS CON CABLE EN ESPAÑOL ===
    "https://raw.githubusercontent.com/Tundrak/IPTV-Iberico-Plus/main/ibericoptv.m3u",
    "https://raw.githubusercontent.com/LaQuay/TDTChannels/master/exports/tdt.m3u",
    "https://raw.githubusercontent.com/davidmuma/Canales_PlutoTV/master/channels.m3u",
    "https://raw.githubusercontent.com/FunctionError/PiratesIPTV/main/combinedList.m3u",

    # === DEPORTES ===
    "https://iptv-org.github.io/iptv/categories/sports.m3u",

    # === ENTRETENIMIENTO / PELÍCULAS ===
    "https://iptv-org.github.io/iptv/categories/entertainment.m3u",
    "https://iptv-org.github.io/iptv/categories/movies.m3u",

    # === INFANTILES ===
    "https://iptv-org.github.io/iptv/categories/kids.m3u",
]
def obtener_stream_youtube(url):
    try:
        resultado = subprocess.check_output(['yt-dlp', '-g', '-f', 'best', url]).decode('utf-8').strip()
        return resultado.split('\n')[0]
    except: return None

def main():
    print(f"🚀 Generando lista Master: {datetime.now()}")
    entradas = []

    # Procesar YouTube
    for c in CANALES_YOUTUBE:
        stream = obtener_stream_youtube(c['url'])
        if stream:
            entradas.append(f'#EXTINF:-1 tvg-logo="{c["logo"]}" group-title="{c["grupo"]}",{c["nombre"]}\n{stream}')

    # Procesar Fuentes M3U Externas
    for url_fuente in FUENTES_M3U:
        try:
            print(f"🌐 Extrayendo de: {url_fuente}")
            with urllib.request.urlopen(url_fuente, timeout=10) as r:
                contenido = r.read().decode('utf-8')
                # Quitamos la cabecera #EXTM3U de cada lista para no duplicarla
                limpio = contenido.replace("#EXTM3U", "").strip()
                if limpio: entradas.append(limpio)
        except: print(f"⚠️ Error en fuente: {url_fuente}")

    # Escribir archivo final con EPG UNIFICADA
    # Esta URL de EPG de iptv-org es global
    epg_url = 'https://iptv-org.github.io/epg/guides/ar.xml,https://iptv-org.github.io/epg/guides/mx.xml,https://iptv-org.github.io/epg/guides/es.xml'
    
    with open("lista.m3u", "w", encoding="utf-8") as f:
        f.write(f'#EXTM3U x-tvg-url="{epg_url}"\n' + "\n".join(entradas))
    
    print(f"✅ ¡Lista Master generada!")

if __name__ == "__main__":
    main()
