from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import requests
import io
from utils.logger import logger

def open_image(source):
    """
    Ouvre une image depuis un chemin local ou une URL.
    """
    try:
        if source.startswith('http://') or source.startswith('https://'):
            response = requests.get(source, timeout=10)
            response.raise_for_status()
            image = Image.open(io.BytesIO(response.content))
            logger.info(f"Image téléchargée depuis URL: {source}")
        else:
            image = Image.open(source)
            logger.info(f"Image ouverte localement: {source}")
        return image
    except Exception as e:
        logger.error(f"Erreur ouverture image {source}: {e}")
        return None

def extract_basic_metadata(image):
    """
    Extrait les métadonnées basiques d’une image PIL.
    """
    try:
        metadata = {
            "format": image.format,
            "mode": image.mode,
            "size": image.size,  # (largeur, hauteur)
        }
        return metadata
    except Exception as e:
        logger.error(f"Erreur extraction métadonnées basiques: {e}")
        return {}

def extract_exif_data(image):
    """
    Extrait les données EXIF avec tags lisibles et GPS.
    """
    exif_data = {}
    try:
        info = image._getexif()
        if not info:
            logger.info("Aucune donnée EXIF trouvée.")
            return {}

        for tag, value in info.items():
            decoded = TAGS.get(tag, tag)
            if decoded == "GPSInfo":
                gps_data = {}
                for t in value:
                    sub_decoded = GPSTAGS.get(t, t)
                    gps_data[sub_decoded] = value[t]
                exif_data[decoded] = gps_data
            else:
                exif_data[decoded] = value
        return exif_data
    except Exception as e:
        logger.error(f"Erreur extraction EXIF: {e}")
        return {}

def get_geotagging(exif_data):
    """
    Extrait latitude et longitude si présentes dans GPSInfo.
    Retourne tuple (lat, lon) ou None.
    """
    if not exif_data or "GPSInfo" not in exif_data:
        logger.info("Pas de données GPS dans EXIF.")
        return None

    gps_info = exif_data["GPSInfo"]

    def _convert_to_degrees(value):
        d = value[0][0] / value[0][1]
        m = value[1][0] / value[1][1]
        s = value[2][0] / value[2][1]
        return d + (m / 60.0) + (s / 3600.0)

    try:
        lat = _convert_to_degrees(gps_info['GPSLatitude'])
        if gps_info['GPSLatitudeRef'] != 'N':
            lat = -lat
        lon = _convert_to_degrees(gps_info['GPSLongitude'])
        if gps_info['GPSLongitudeRef'] != 'E':
            lon = -lon
        return (lat, lon)
    except Exception as e:
        logger.error(f"Erreur extraction géotags: {e}")
        return None
