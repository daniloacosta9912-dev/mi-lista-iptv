import subprocess
import urllib.request
import re
from datetime import datetime

# 1. CONFIGURACIÓN DE CANALES YOUTUBE (Con logos y grupos)
CANALES_YOUTUBE = [
    {"nombre": "ElTrece", "grupo": "Entretenimiento", "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6e/El_Trece_logo.svg/200px-El_Trece_logo.svg.png", "url": "https://www.youtube.com/@eltrece/live"},
    {"nombre": "Telefe", "grupo": "Entretenimiento", "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3c/Telefe_2019.svg/200px-Telefe_2019.svg.png", "url": "https://www.youtube.com/@Telefe/live"},
    {"nombre": "TN - Todo Noticias", "grupo": "Noticias", "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1f/TN-Todo-Noticias-2018.svg/200px-TN-Todo-Noticias-2018.svg.png", "url": "https://www.youtube.com/@todonoticias/live"},
    {"nombre": "C5N", "grupo": "Noticias", "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d2/C5N_logo.svg/200px-C5N_logo.svg.png", "url": "https://www.youtube.com/@c5n/live"},
    {"nombre": "A24", "grupo": "Noticias", "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5e/A24_logo.svg/200px-A24_logo.svg.png", "url": "https://www.youtube.com/@A24com/live"},
    {"nombre": "LN+", "grupo": "Noticias", "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/r/r7/Logo_de_LN%2B.svg/200px-Logo_de_LN%2B.svg.png", "url": "https://www.youtube.com/@lanacion/live"}
]

IPTV_ORG_URL = "https://iptv-org.github.io/iptv/countries/ar.m3u"

def obtener_stream_youtube(url):
    """Extrae el m3u8 real usando el motor optimizado de yt-dlp."""
    try:
        # Forzamos formato de video simple para evitar errores en TV Boxes viejas
        resultado = subprocess.check_output(['yt-dlp', '-g', '-f', 'best', url]).decode('utf-8').strip()
        return resultado.split('\n')[0]
    except:
        return None

def main():
    print(f"🚀 Iniciando actualización: {datetime.now()}")
    entradas = []

    # Procesar YouTube
    for c in CANALES_YOUTUBE:
        print(f"📺 Obteniendo: {c['nombre']}")
        stream = obtener_stream_youtube(c['url'])
        if stream:
            entradas.append(f'#EXTINF:-1 tvg-logo="{c["logo"]}" group-title="{c["grupo"]}",{c["nombre"]}\n{stream}')

    # Procesar IPTV-ORG (Opcional, pero recomendado)
    try:
        print("🌐 Descargando canales adicionales de IPTV-ORG...")
        with urllib.request.urlopen(IPTV_ORG_URL, timeout=10) as r:
            extra = r.read().decode('utf-8').replace("#EXTM3U", "").strip()
            if extra: entradas.append(extra)
    except:
        print("⚠️ No se pudo conectar con IPTV-ORG, usando solo YouTube.")

    # Escribir archivo final
    with open("lista.m3u", "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n" + "\n".join(entradas))
    
    print(f"✅ Proceso finalizado. {len(entradas)} bloques de canales escritos.")

if __name__ == "__main__":
    main()
