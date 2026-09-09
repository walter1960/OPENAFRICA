# collecteurs/telegram/storage.py
# Gestion du stockage des fichiers audio et des metadonnees
# Garanti sans aucun emoji.

import os
import csv
from datetime import datetime

VARIETES_MAP = {
    "ewe": {
        "lome": ("be_lome", "voix/togo/ewe/be_lome"),
        "kpalime": ("kpalime_kloto", "voix/togo/ewe/kpalime_kloto"),
        "tsevie": ("tsevie_zio", "voix/togo/ewe/tsevie_zio"),
        "notse": ("notse_agbogbome", "voix/togo/ewe/notse_agbogbome"),
        "agou": ("agou", "voix/togo/ewe/agou"),
        "danyi": ("danyi", "voix/togo/ewe/danyi"),
        "keve": ("ave_keve", "voix/togo/ewe/ave_keve"),
        "vogan": ("vo_waci", "voix/togo/ewe/vo_waci"),
        "tabligbo": ("yoto_tabligbo", "voix/togo/ewe/yoto_tabligbo"),
        "autre": ("be_lome", "voix/togo/ewe/be_lome")
    },
    "mina": {
        "lome": ("lome_urbain", "voix/togo/mina/lome_urbain"),
        "aneho": ("aneho_glidji", "voix/togo/mina/aneho_glidji"),
        "agbodrafo": ("agbodrafo", "voix/togo/mina/agbodrafo"),
        "togoville": ("togoville", "voix/togo/mina/togoville"),
        "autre": ("lome_urbain", "voix/togo/mina/lome_urbain")
    }
}

METADATA_FILE = "voix/togo/metadonnees_collecte.csv"

def init_metadata_csv():
    os.makedirs(os.path.dirname(METADATA_FILE), exist_ok=True)
    if not os.path.exists(METADATA_FILE):
        with open(METADATA_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                "id_fichier",
                "chemin_relatif",
                "langue",
                "variete_slug",
                "ville",
                "profil_locuteur",
                "sujet_id",
                "duree_secondes",
                "date_heure",
                "telegram_user_id"
            ])

def sauvegarder_audio_collecte(temp_audio_path, langue, ville, profil_locuteur, sujet_id, duree, telegram_user_id):
    init_metadata_csv()
    
    # Determiner la variete et le dossier cible
    langue_clean = langue.lower()
    ville_clean = ville.lower()
    
    if langue_clean in VARIETES_MAP:
        mapping = VARIETES_MAP[langue_clean]
        variete_slug, target_dir = mapping.get(ville_clean, mapping.get("autre"))
    else:
        variete_slug = "standard"
        target_dir = f"voix/togo/{langue_clean}"
        
    os.makedirs(target_dir, exist_ok=True)
    
    # Generer le nom de fichier standardise
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nom_fichier = f"{langue_clean}_{variete_slug}_{profil_locuteur}_{timestamp}.ogg"
    destination_path = os.path.join(target_dir, nom_fichier)
    
    # Deplacer ou copier le fichier temporaire
    import shutil
    shutil.move(temp_audio_path, destination_path)
    
    # Enregistrer dans le CSV
    with open(METADATA_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            nom_fichier,
            destination_path,
            langue_clean,
            variete_slug,
            ville_clean,
            profil_locuteur,
            sujet_id or "libre",
            duree or 0,
            datetime.now().isoformat(),
            telegram_user_id
        ])
        
    return destination_path, nom_fichier
