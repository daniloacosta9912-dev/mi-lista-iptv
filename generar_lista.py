import urllib.request
import re
from datetime import datetime

# FUENTES EXTERNAS
FUENTES_M3U = [
    # === ARGENTINA ===
    "https://iptv-org.github.io/iptv/countries/ar.m3u",

    # === LATINOAMÉRICA ===
    "https://iptv-org.github.io/iptv/countries/mx.m3u",
    "https://iptv-org.github.io/iptv/countries/cl.m3u",
    "https://iptv-org.github.io/iptv/countries/co.m3u",
    "https://iptv-org.github.io/iptv/countries/ve.m3u",
    "https://iptv-org.github.io/iptv/countries/pe.m3u",
    "https://iptv-org.github.io/iptv/countries/uy.m3u",
    "https://iptv-org.github.io/iptv/countries/py.m3u",
    "https://iptv-org.github.io/iptv/countries/bo.m3u",

    # === POR CATEGORÍA ===
    "https://iptv-org.github.io/iptv/categories/sports.m3u",
    "https://iptv-org.github.io/iptv/categories/entertainment.m3u",
    "https://iptv-org.github.io/iptv/categories/movies.m3u",
    "https://iptv-org.github.io/iptv/categories/news.m3u",
]

# FILTROS POR NOMBRE
FILTROS_NOMBRE = [
    # Geo-bloqueados
    "[geo-blocked]", "[geo-block]",
    # Árabes
    "alkass", "arryadia", "al jazeera", "al arabiya", "beinsports arabic",
    "sharjah", "bahrain", "oman sport", "jordan sport", "rta sport",
    "ktv sport", "kuwait", "qatar",
    # Asiáticos / indios
    "sony sports ten", "star sports", "dd sports", "ptv sports",
    "ten sports", "willow", "big magic", "colors", "sab tv",
    "zee ", "sony liv", "gaora", "j sports", "nittele",
    "htv", "tvri", "t sports", "udaya", "vissa",
    # Rusos / este europeo
    "матч", "бокс тв", "старт", "русский", "беларусь",
    "астрахань", "gramy dalej", "qazport",
    # Turcos
    "trt spor", "s sport", "tabii spor", "a-plus tv",
    # Iraníes / persas
    "irib", "varzesh", "telewebion", "persiana",
    # Vietnamitas
    "đồng nai", "htv thể",
    # Catalanes
    "esport3", "carac",
    # Pluto TV
    "pluto tv",
    # Deportes muy específicos
    "golf network", "golf channel", "one golf", "tennis channel",
    "cycling channel", "tjk tv", "teletrak", "tvs bowling", "tvs boxing",
    "tvs classic", "tvs turbo", "tvs women", "tvs vintage", "tvs flashback",
    "tvs sports bureau", "tvs sports", "nudge sports", "more than sports",
    "unbeaten sports", "world of freesports", "vital drive", "w14dk",
    "pac 12", "bek tv", "cricket gold", "awapa", "atg live",
    "fb tv", "ftv", "game+", "gramy",
    # Idiomas no deseados
    "rai sport", "sport italia", "sport1", "sportitalia",
    "l'equipe", "6ter", "arte ",
    "lrt plius", "suspilne", "ct sport", "mnb sport", "m4 sport",
    "adjarasport", "rtsh sport", "san marino rtv sport",
    "smg football", "sin po", "tr sport",
    # Canales que no funcionan
    "pluto tv", "buzzr", "decades", "cozi tv", "el rey",
    "ion ", "game show network", "gametoon", "heartland",
    "mystery tv", "wipeout", "xplore", "color blind",
    "bflix", "goldmines", "moviedome", "filmex",
    "nba tv", "nfl ", "mlb ", "nhl ",
]

# PAÍSES PERMITIDOS
PAISES_PERMITIDOS = [
    ".ar", ".mx", ".cl", ".co", ".ve", ".pe", ".uy", ".py", ".bo",
    ".es", ".cu", ".do", ".pr", ".pa", ".cr", ".hn", ".gt", ".sv",
    ".ni", ".ec", ".us",
]

# FILTROS POR GRUPO
FILTROS_GRUPO = [
    "undefined",
]

# IDIOMAS PERMITIDOS
IDIOMAS_PERMITIDOS = ["spa", ""]

def canal_permitido(nombre, grupo, idioma="", tvgid=""):
    nombre_lower = nombre.lower()
    grupo_lower  = grupo.lower()

    for palabra in FILTROS_NOMBRE:
        if palabra.lower() in nombre_lower:
            return False

    for g in FILTROS_GRUPO:
        if g.lower() in grupo_lower:
            return False

    for char in nombre:
        if ord(char) > 1000:
            return False

    if idioma and idioma not in IDIOMAS_PERMITIDOS:
        return False

    if tvgid:
        partes = tvgid.lower().split("@")[0]
        if not any(partes.endswith(p) for p in PAISES_PERMITIDOS):
            return False

    return True

def main():
    print(f"Generando lista Master: {datetime.now()}")
    entradas = []
    urls_vistas = set()
    filtrados = 0

    for url_fuente in FUENTES_M3U:
        try:
            print(f"Extrayendo de: {url_fuente}")
            with urllib.request.urlopen(url_fuente, timeout=15) as r:
                contenido = r.read().decode('utf-8')

            lineas = contenido.splitlines()
            i = 0
            while i < len(lineas):
                if lineas[i].startswith('#EXTINF'):
                    extinf = lineas[i]
                    nombre_match = re.search(r',(.+)$', extinf)
                    grupo_match  = re.search(r'group-title="([^"]*)"', extinf)
                    idioma_match = re.search(r'tvg-language="([^"]*)"', extinf)
                    tvgid_match  = re.search(r'tvg-id="([^"]*)"', extinf)
                    nombre = nombre_match.group(1).strip() if nombre_match else ""
                    grupo  = grupo_match.group(1).strip()  if grupo_match  else ""
                    idioma = idioma_match.group(1).strip().lower() if idioma_match else ""
                    tvgid  = tvgid_match.group(1).strip()  if tvgid_match  else ""

                    i += 1
                    while i < len(lineas) and not lineas[i].startswith('http'):
                        i += 1
                    if i < len(lineas):
                        url = lineas[i].strip()
                        if url and url not in urls_vistas:
                            if canal_permitido(nombre, grupo, idioma, tvgid):
                                urls_vistas.add(url)
                                entradas.append(f'{extinf}\n{url}')
                            else:
                                filtrados += 1
                i += 1

        except Exception as e:
            print(f"Error en fuente: {url_fuente} - {e}")

    epg_url = 'https://iptv-org.github.io/epg/guides/ar.xml,https://iptv-org.github.io/epg/guides/mx.xml,https://iptv-org.github.io/epg/guides/es.xml'

    with open("lista.m3u", "w", encoding="utf-8") as f:
        f.write(f'#EXTM3U x-tvg-url="{epg_url}"\n' + "\n".join(entradas))

    print(f"Lista generada con {len(entradas)} canales unicos")
    print(f"Canales filtrados: {filtrados}")

if __name__ == "__main__":
    main()
