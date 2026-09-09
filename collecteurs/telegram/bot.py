#!/usr/bin/env python3
# collecteurs/telegram/bot.py
# Bot Telegram de collecte vocale pour OPENAFRICA (Ewe, Mina, Togo)
# Fonctionne avec la bibliotheque standard Python et requests.
# Garanti sans aucun emoji.

import os
import sys
import time
import json
import tempfile
import requests
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

from prompts import obtenir_sujet_aleatoire
from storage import sauvegarder_audio_collecte

# Configuration du token Telegram
# Peut etre defini via variable d'environnement TELEGRAM_BOT_TOKEN
# ou passe en argument en ligne de commande.
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()

API_BASE_URL = "https://api.telegram.org/bot"
FILE_BASE_URL = "https://api.telegram.org/file/bot"

# Dictionnaire de session utilisateur : chat_id -> dict
USER_SESSIONS = {}

def api_request(method, payload=None):
    if not BOT_TOKEN:
        raise ValueError("Le token du bot Telegram n'est pas defini. Exportez TELEGRAM_BOT_TOKEN ou specifiez-le.")
    url = f"{API_BASE_URL}{BOT_TOKEN}/{method}"
    try:
        response = requests.post(url, json=payload, timeout=40)
        return response.json()
    except Exception as e:
        print(f"Erreur API Telegram ({method}): {e}", file=sys.stderr)
        return None

def telecharger_fichier(file_path, destination_path):
    url = f"{FILE_BASE_URL}{BOT_TOKEN}/{file_path}"
    try:
        response = requests.get(url, stream=True, timeout=60)
        with open(destination_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        return True
    except Exception as e:
        print(f"Erreur lors du telechargement du fichier audio : {e}", file=sys.stderr)
        return False

def envoyer_message(chat_id, texte, reply_markup=None):
    payload = {
        "chat_id": chat_id,
        "text": texte,
        "parse_mode": "Markdown"
    }
    if reply_markup:
        payload["reply_markup"] = reply_markup
    return api_request("sendMessage", payload)

def modifier_message(chat_id, message_id, texte, reply_markup=None):
    payload = {
        "chat_id": chat_id,
        "message_id": message_id,
        "text": texte,
        "parse_mode": "Markdown"
    }
    if reply_markup:
        payload["reply_markup"] = reply_markup
    return api_request("editMessageText", payload)

def acquitter_callback(callback_query_id):
    return api_request("answerCallbackQuery", {"callback_query_id": callback_query_id})

def gerer_commande_start(chat_id):
    texte = (
        "*Bienvenue sur le Bot OPENAFRICA*\n\n"
        "Ce bot permet de collecter des enregistrements vocaux en *Ewe* et *Mina* "
        "pour entrainer une intelligence artificielle conversationnelle respectant nos langues.\n\n"
        "Vous pouvez :\n"
        "1. Demander un sujet de conversation en appuyant sur le bouton ci-dessous.\n"
        "2. Ou envoyer directement une note vocale en parlant naturellement.\n\n"
        "Akpe kaka pour votre participation !"
    )
    clavier = {
        "inline_keyboard": [
            [{"text": "Proposer un sujet de conversation", "callback_data": "action:nouveau_sujet"}],
            [{"text": "Comment fonctionne la collecte ?", "callback_data": "action:aide"}]
        ]
    }
    envoyer_message(chat_id, texte, clavier)

def gerer_nouveau_sujet(chat_id, message_id=None):
    sujet = obtenir_sujet_aleatoire()
    texte = (
        f"*Theme : {sujet['theme']}*\n\n"
        f"*Francais :* {sujet['question_fr']}\n\n"
        f"*Evegbe :* {sujet['question_ee']}\n\n"
        f"*Mina :* {sujet['question_ge']}\n\n"
        "_Appuyez sur le micro de Telegram et enregistrez votre reponse vocale (30 secondes a 2 minutes)._"
    )
    clavier = {
        "inline_keyboard": [
            [{"text": "Autre sujet", "callback_data": "action:nouveau_sujet"}]
        ]
    }
    
    # Enregistrer le sujet actif pour ce contributeur
    if chat_id not in USER_SESSIONS:
        USER_SESSIONS[chat_id] = {}
    USER_SESSIONS[chat_id]["sujet_actif"] = sujet["id"]
    
    if message_id:
        modifier_message(chat_id, message_id, texte, clavier)
    else:
        envoyer_message(chat_id, texte, clavier)

def gerer_reception_audio(chat_id, file_id, duree_secondes):
    # Recuperer les informations du fichier via l'API Telegram
    res = api_request("getFile", {"file_id": file_id})
    if not res or not res.get("ok"):
        envoyer_message(chat_id, "Impossible de recuperer l'enregistrement. Veuillez reessayer.")
        return

    file_path = res["result"]["file_path"]
    temp_dir = tempfile.gettempdir()
    temp_filename = os.path.join(temp_dir, f"tg_{chat_id}_{int(time.time())}.ogg")
    
    succes = telecharger_fichier(file_path, temp_filename)
    if not succes:
        envoyer_message(chat_id, "Erreur lors de la reception du fichier. Veuillez reessayer.")
        return

    # Initialiser la session pour ce fichier audio
    sujet_precedent = USER_SESSIONS.get(chat_id, {}).get("sujet_actif", "libre")
    USER_SESSIONS[chat_id] = {
        "temp_path": temp_filename,
        "duree": duree_secondes,
        "sujet_id": sujet_precedent,
        "etape": "langue"
    }

    texte = (
        "*Enregistrement vocal bien recu !*\n\n"
        "*Etape 1 sur 3* : Dans quelle langue avez-vous parle ?"
    )
    clavier = {
        "inline_keyboard": [
            [
                {"text": "Ewe (Evegbe)", "callback_data": "lang:ewe"},
                {"text": "Mina / Gen (Gengbe)", "callback_data": "lang:mina"}
            ],
            [
                {"text": "Kabiye", "callback_data": "lang:kabiye"},
                {"text": "Autre langue", "callback_data": "lang:autre"}
            ]
        ]
    }
    envoyer_message(chat_id, texte, clavier)

def gerer_selection_langue(chat_id, message_id, langue):
    if chat_id not in USER_SESSIONS or "temp_path" not in USER_SESSIONS[chat_id]:
        envoyer_message(chat_id, "Session expiree. Veuillez envoyer a nouveau votre message vocal.")
        return

    USER_SESSIONS[chat_id]["langue"] = langue
    USER_SESSIONS[chat_id]["etape"] = "ville"

    texte = (
        f"*Langue selectionnee : {langue.upper()}*\n\n"
        "*Etape 2 sur 3* : Quelle est votre ville ou region d'origine ?"
    )
    
    if langue == "ewe":
        clavier = {
            "inline_keyboard": [
                [{"text": "Lome (Be, Agoe)", "callback_data": "ville:lome"}, {"text": "Kpalime (Kloto)", "callback_data": "ville:kpalime"}],
                [{"text": "Tsevie (Zio)", "callback_data": "ville:tsevie"}, {"text": "Notse (Haho)", "callback_data": "ville:notse"}],
                [{"text": "Agou", "callback_data": "ville:agou"}, {"text": "Danyi", "callback_data": "ville:danyi"}],
                [{"text": "Keve (Ave)", "callback_data": "ville:keve"}, {"text": "Vogan (Ouatchi)", "callback_data": "ville:vogan"}],
                [{"text": "Tabligbo (Yoto)", "callback_data": "ville:tabligbo"}, {"text": "Autre localite", "callback_data": "ville:autre"}]
            ]
        }
    elif langue == "mina":
        clavier = {
            "inline_keyboard": [
                [{"text": "Lome (Assigame, Ville)", "callback_data": "ville:lome"}, {"text": "Aneho / Glidji", "callback_data": "ville:aneho"}],
                [{"text": "Agbodrafo (Porto-Seguro)", "callback_data": "ville:agbodrafo"}, {"text": "Togoville", "callback_data": "ville:togoville"}],
                [{"text": "Autre localite", "callback_data": "ville:autre"}]
            ]
        }
    else:
        clavier = {
            "inline_keyboard": [
                [{"text": "Lome", "callback_data": "ville:lome"}, {"text": "Kara", "callback_data": "ville:kara"}],
                [{"text": "Autre", "callback_data": "ville:autre"}]
            ]
        }

    modifier_message(chat_id, message_id, texte, clavier)

def gerer_selection_ville(chat_id, message_id, ville):
    if chat_id not in USER_SESSIONS or "temp_path" not in USER_SESSIONS[chat_id]:
        envoyer_message(chat_id, "Session expiree. Veuillez renvoyer votre vocal.")
        return

    USER_SESSIONS[chat_id]["ville"] = ville
    USER_SESSIONS[chat_id]["etape"] = "profil"

    texte = (
        f"*Ville/Variete : {ville.upper()}*\n\n"
        "*Etape 3 sur 3* : Profil du locuteur (aide a calibrer la frequence de la voix) :"
    )
    clavier = {
        "inline_keyboard": [
            [{"text": "Homme (Moins de 30 ans)", "callback_data": "prof:h_jeune"}, {"text": "Femme (Moins de 30 ans)", "callback_data": "prof:f_jeune"}],
            [{"text": "Homme (30 a 50 ans)", "callback_data": "prof:h_adulte"}, {"text": "Femme (30 a 50 ans)", "callback_data": "prof:f_adulte"}],
            [{"text": "Homme (Plus de 50 ans)", "callback_data": "prof:h_aine"}, {"text": "Femme (Plus de 50 ans)", "callback_data": "prof:f_ainee"}]
        ]
    }
    modifier_message(chat_id, message_id, texte, clavier)

def finaliser_enregistrement(chat_id, message_id, profil):
    if chat_id not in USER_SESSIONS or "temp_path" not in USER_SESSIONS[chat_id]:
        envoyer_message(chat_id, "Session expiree. Veuillez renvoyer votre vocal.")
        return

    session = USER_SESSIONS[chat_id]
    temp_path = session["temp_path"]
    langue = session.get("langue", "ewe")
    ville = session.get("ville", "lome")
    duree = session.get("duree", 0)
    sujet_id = session.get("sujet_id", "libre")

    try:
        dest_path, nom_fichier = sauvegarder_audio_collecte(
            temp_audio_path=temp_path,
            langue=langue,
            ville=ville,
            profil_locuteur=profil,
            sujet_id=sujet_id,
            duree=duree,
            telegram_user_id=chat_id
        )

        texte_confirmation = (
            "*Akpe kaka ! Enregistrement valide avec succes.*\n\n"
            f"*Fichier enregistre :* `{nom_fichier}`\n"
            f"*Dossier :* `{dest_path}`\n"
            f"*Duree :* {duree} secondes\n\n"
            "Votre voix enrichit directement la base de donnees de l'intelligence artificielle africaine.\n\n"
            "Pret pour un nouvel enregistrement ?"
        )
        clavier = {
            "inline_keyboard": [
                [{"text": "Nouveau sujet de conversation", "callback_data": "action:nouveau_sujet"}]
            ]
        }
        modifier_message(chat_id, message_id, texte_confirmation, clavier)
    except Exception as e:
        print(f"Erreur de sauvegarde finale : {e}", file=sys.stderr)
        modifier_message(chat_id, message_id, "Une erreur est survenue lors de la sauvegarde. Veuillez reessayer.")
    finally:
        USER_SESSIONS.pop(chat_id, None)

def executer_polling():
    print("Demarrage du bot Telegram OPENAFRICA...")
    offset = 0
    while True:
        try:
            updates = api_request("getUpdates", {"offset": offset, "timeout": 20})
            if not updates or not updates.get("ok"):
                time.sleep(2)
                continue

            for item in updates.get("result", []):
                offset = item["update_id"] + 1

                # Gestion des messages texte et vocaux
                if "message" in item:
                    msg = item["message"]
                    chat_id = msg["chat"]["id"]

                    # Commande /start
                    if "text" in msg:
                        texte = msg["text"].strip()
                        if texte.startswith("/start"):
                            gerer_commande_start(chat_id)
                        elif texte.startswith("/sujet"):
                            gerer_nouveau_sujet(chat_id)
                        elif texte.startswith("/aide"):
                            envoyer_message(chat_id, "Envoyez simplement un message vocal en parlant en Ewe ou en Mina. Le bot s'occupe de tout classer !")

                    # Message vocal ou fichier audio
                    elif "voice" in msg:
                        voice = msg["voice"]
                        gerer_reception_audio(chat_id, voice["file_id"], voice.get("duration", 0))
                    elif "audio" in msg:
                        audio = msg["audio"]
                        gerer_reception_audio(chat_id, audio["file_id"], audio.get("duration", 0))

                # Gestion des clics sur les boutons (CallbackQuery)
                elif "callback_query" in item:
                    cb = item["callback_query"]
                    cb_id = cb["id"]
                    chat_id = cb["message"]["chat"]["id"]
                    msg_id = cb["message"]["message_id"]
                    data = cb.get("data", "")
                    
                    acquitter_callback(cb_id)

                    if data == "action:nouveau_sujet":
                        gerer_nouveau_sujet(chat_id, msg_id)
                    elif data == "action:aide":
                        modifier_message(chat_id, msg_id, "Envoyez un message vocal (enregistre avec le micro Telegram). Repondez ensuite aux 3 questions pour qualifier la langue et la ville.")
                    elif data.startswith("lang:"):
                        langue = data.split(":")[1]
                        gerer_selection_langue(chat_id, msg_id, langue)
                    elif data.startswith("ville:"):
                        ville = data.split(":")[1]
                        gerer_selection_ville(chat_id, msg_id, ville)
                    elif data.startswith("prof:"):
                        profil = data.split(":")[1]
                        finaliser_enregistrement(chat_id, msg_id, profil)

        except KeyboardInterrupt:
            print("\nArret du bot demande.")
            break
        except Exception as e:
            print(f"Exception dans la boucle principale : {e}", file=sys.stderr)
            time.sleep(3)

if __name__ == "__main__":
    if len(sys.argv) > 1 and not BOT_TOKEN:
        BOT_TOKEN = sys.argv[1].strip()

    if not BOT_TOKEN:
        print("ATTENTION : Aucun token Telegram fourni.")
        print("Utilisation :")
        print("  export TELEGRAM_BOT_TOKEN='votre_token_ici'")
        print("  python3 collecteurs/telegram/bot.py")
        print("Ou :")
        print("  python3 collecteurs/telegram/bot.py 'votre_token_ici'")
        sys.exit(1)

    executer_polling()
