import subprocess
import urllib.request
import re
from datetime import datetime

# 1. TUS CANALES DE YOUTUBE (Prioridad local)
CANALES_YOUTUBE = [
    # === AR - AIRE ===
    {"nombre": "ElTrece", "grupo": "AR - Aire", "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6e/El_Trece_logo.svg/200px-El_Trece_logo.svg.png", "url": "https://www.youtube.com/@eltrece/live"},
    {"nombre": "Telefe", "grupo": "AR - Aire", "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3c/Telefe_2019.svg/200px-Telefe_2019.svg.png", "url": "https://www.youtube.com/@Telefe/live"},
    {"nombre": "América TV", "grupo": "AR - Aire", "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b3/Am%C3%A9rica_TV_2019_logo.svg/200px-Am%C3%A9rica_TV_2019_logo.svg.png", "url": "https://www.youtube.com/@americaenvivo/live"},

    # === AR - NOTICIAS ===
    {"nombre": "TN - Todo Noticias", "grupo": "AR - Noticias", "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1f/TN-Todo-Noticias-2018.svg/200px-TN-Todo-Noticias-2018.svg.png", "url": "https://www.youtube.com/@todonoticias/live"},
    {"nombre": "A24", "grupo": "AR - Noticias", "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5e/A24_logo.svg/200px-A24_logo.svg.png", "url": "https://www.youtube.com/@A24com/live"},
    {"nombre": "C5N", "grupo": "AR - Noticias", "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d2/C5N_logo.svg/200px-C5N_logo.svg.png", "url": "https://www.youtube.com/@c5n/live"},
    {"nombre": "LN+", "grupo": "AR - Noticias", "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a2/LN%2B_logo.svg/200px-LN%2B_logo.svg.png", "url": "https://www.youtube.com/@lanacionmas/live"},
    {"nombre": "Crónica TV", "grupo": "AR - Noticias", "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9d/Cr%C3%B3nica_TV_logo.svg/200px-Cr%C3%B3nica_TV_logo.svg.png", "url": "https://www.youtube.com/@cronicatv/live"},

    # === AR - CÓRDOBA ===
    {"nombre": "El Doce", "grupo": "AR - Córdoba", "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/El_Doce_logo.svg/200px-El_Doce_logo.svg.png", "url": "https://www.youtube.com/@eldoce/live"},
    {"nombre": "Canal 10 Córdoba", "grupo": "AR - Córdoba", "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Canal_10_C%C3%B3rdoba_logo.svg/200px-Canal_10_C%C3%B3rdoba_logo.svg.png", "url": "https://www.youtube.com/@canal10cordoba/live"},
    {"nombre": "Cadena 3", "grupo": "AR - Córdoba", "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7e/Cadena_3_logo.svg/200px-Cadena_3_logo.svg.png", "url": "https://www.youtube.com/@cadena3argentina/live"},
]

# 2. FUENTES EXTERNAS
FUENTES_M3U = [
    "https://iptv-org.github.io/iptv/countries/ar.m3u",
    "https://raw.githubusercontent.com/dmelendez11/lista-canales-m3u/main/channels.m3u",
    "https://raw.githubusercontent.com/jsosao/m3u/main/test.m3u8",
    "https://raw.githubusercontent.com/Tundrak/IPTV-Iberico-Plus/main/ibericoptv.m3u",
    "https://raw.githubusercontent.com/LaQuay/TDTChannels/master/exports/tdt.m3u",
    "https://raw.githubusercontent.com/davidmuma/Canales_PlutoTV/master/channels.m3u",
    "https://raw.githubusercontent.com/FunctionError/PiratesIPTV/main/combinedList.m3u",
    "https://iptv-org.github.io/iptv/categories/sports.m3u",
    "https://iptv-org.github.io/iptv/categories/entertainment.m3u",
    "https://iptv-org.github.io/iptv/categories/movies.m3u",
    "https://iptv-org.github.io/iptv/categories/kids.m3u",
]

# 3. FILTROS — palabras que si aparecen en el nombre, el canal se elimina
FILTROS_NOMBRE = [
    # Geo-bloqueados
    "[geo-blocked]", "[geo-block]",
    # Canales árabes
    "alkass", "arryadia", "al jazeera", "al arabiya", "beinsports arabic",
    "sharjah", "bahrain", "oman sport", "jordan sport", "rta sport",
    "ktv sport", "kuwait", "qatar",
    # Canales asiáticos / indios
    "sony sports ten", "star sports", "dd sports", "ptv sports",
    "ten sports", "willow", "big magic", "colors", "sab tv",
    "zee ", "sony liv", "gaora", "j sports", "nittele",
    "htv", "tvri", "t sports", "udaya", "vissa",
    # Canales rusos / del este europeo
    "матч", "бокс тв", "старт", "русский", "беларусь",
    "астрахань", "gramy dalej", "qazport",
    # Canales turcos
    "trt spor", "s sport", "tabii spor", "a-plus tv",
    # Canales iraníes / persas
    "irib", "varzesh", "telewebion", "persiana",
    # Canales vietnamitas
    "đồng nai", "htv thể",
    # Canales catalanes
    "esport3", "carac",
    # Pluto TV (muchos no funcionan)
    "pluto tv",
    # Canales muy específicos que no te interesan
    "alkass", "golf network", "golf channel", "one golf", "tennis channel",
    "cycling channel", "tjk tv", "teletrak", "tvs bowling", "tvs boxing",
    "tvs classic", "tvs turbo", "tvs women", "tvs vintage", "tvs flashback",
    "tvs sports bureau", "tvs sports", "nudge sports", "more than sports",
    "unbeaten sports", "world of freesports", "vital drive", "w14dk",
    "pac 12", "bek tv", "cricket gold", "awapa", "atg live",
    "fb tv", "ftv", "game+", "gramy",
    # Canales de idiomas no deseados por nombre obvio
    "rai sport", "sport italia", "sport1", "sportitalia",
    "l'equipe", "6ter", "arte ",
    "lrt plius", "suspilne", "ct sport", "mnb sport", "m4 sport",
    "adjarasport", "rtsh sport", "san marino rtv sport",
    "smg football", "sin po", "tr sport",
]

# 4. FILTROS — grupos que se eliminan completos
FILTROS_GRUPO = [
    "undefined",
]

def canal_permitido(nombre, grupo):
    """Devuelve True si el canal debe incluirse, False si debe filtrarse."""
    nombre_lower = nombre.lower()
    grupo_lower  = grupo.lower()

    # Filtrar por palabras en el nombre
    for palabra in FILTROS_NOMBRE:
        if palabra.lower() in nombre_lower:
            return False

    # Filtrar por grupo
    for g in FILTROS_GRUPO:
        if g.lower() in grupo_lower:
            return False

    # Filtrar nombres con caracteres no latinos (árabe, cirílico, chino, etc.)
    # excepto caracteres españoles/portugueses comunes
    for char in nombre:
        if ord(char) > 1000:  # filtra árabe, chino, japonés, etc.
            return False

    return True

def obtener_stream_youtube(url):
    try:
        resultado = subprocess.check_output(['yt-dlp', '-g', '-f', 'best', url]).decode('utf-8').strip()
        return resultado.split('\n')[0]
    except:
        return None

def main():
    print(f"🚀 Generando lista Master: {datetime.now()}")
    entradas = []
    urls_vistas = set()
    filtrados = 0

    # Procesar YouTube
    for c in CANALES_YOUTUBE:
        stream = obtener_stream_youtube(c['url'])
        if stream and stream not in urls_vistas:
            urls_vistas.add(stream)
            entradas.append(f'#EXTINF:-1 tvg-logo="{c["logo"]}" group-title="{c["grupo"]}",{c["nombre"]}\n{stream}')

    # Procesar Fuentes M3U Externas
    for url_fuente in FUENTES_M3U:
        try:
            print(f"🌐 Extrayendo de: {url_fuente}")
            with urllib.request.urlopen(url_fuente, timeout=10) as r:
                contenido = r.read().decode('utf-8')

            lineas = contenido.splitlines()
            i = 0
            while i < len(lineas):
                if lineas[i].startswith('#EXTINF'):
                    extinf = lineas[i]
                    nombre_match = re.search(r',(.+)$', extinf)
                    grupo_match  = re.search(r'group-title="([^"]*)"', extinf)
                    nombre = nombre_match.group(1).strip() if nombre_match else ""
                    grupo  = grupo_match.group(1).strip()  if grupo_match  else ""

                    i += 1
                    while i < len(lineas) and not lineas[i].startswith('http'):
                        i += 1
                    if i < len(lineas):
                        url = lineas[i].strip()
                        if url and url not in urls_vistas:
                            if canal_permitido(nombre, grupo):
                                urls_vistas.add(url)
                                entradas.append(f'{extinf}\n{url}')
                            else:
                                filtrados += 1
                i += 1

        except Exception as e:
            print(f"⚠️ Error en fuente: {url_fuente} — {e}")

    epg_url = 'https://iptv-org.github.io/epg/guides/ar.xml,https://iptv-org.github.io/epg/guides/mx.xml,https://iptv-org.github.io/epg/guides/es.xml'

    with open("lista.m3u", "w", encoding="utf-8") as f:
        f.write(f'#EXTM3U x-tvg-url="{epg_url}"\n' + "\n".join(entradas))

    print(f"✅ Lista generada con {len(entradas)} canales únicos")
    print(f"🗑️ Canales filtrados: {filtrados}")

if __name__ == "__main__":
    main()
