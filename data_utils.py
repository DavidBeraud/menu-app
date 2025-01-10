import json
import os
import logging

# Configuration des logs
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Chemins des fichiers
DATA_DIR = os.path.join(os.path.dirname(__file__), 'static', 'data')
INGREDIENTS_FILE = os.path.join(DATA_DIR, 'ingredients.json')
RECETTES_FILE = os.path.join(DATA_DIR, 'recettes.json')
MENU_FILE = os.path.join(DATA_DIR, 'menu-semaine.json')

def load_data(file_path, key):
    """
    Charge les données depuis un fichier JSON.
    
    :param file_path: Chemin du fichier JSON.
    :param key: Clé à extraire du fichier JSON.
    :return: Données associées à la clé, ou un dictionnaire vide en cas d'erreur.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            if key in data and isinstance(data[key], (dict, list)):  # Supporte les dictionnaires et les listes
                return data[key]
            else:
                logging.warning(f"La clé '{key}' n'existe pas ou n'est pas un dictionnaire/liste dans {file_path}.")
                return {}
    except FileNotFoundError:
        logging.error(f"Fichier non trouvé : {file_path}")
        return {}
    except json.JSONDecodeError:
        logging.error(f"Erreur de décodage JSON dans le fichier : {file_path}")
        return {}
    except Exception as e:
        logging.error(f"Erreur inattendue lors du chargement de {file_path} : {e}")
        return {}

def save_data(file_path, data):
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        print(f"Données sauvegardées dans {file_path}")  # Debug
    except Exception as e:
        print(f"Erreur lors de la sauvegarde des données : {e}")  # Debug