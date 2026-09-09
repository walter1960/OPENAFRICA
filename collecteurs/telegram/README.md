# Bot Telegram de Collecte Vocale OPENAFRICA

Ce bot permet de collecter facilement et massivement des enregistrements vocaux spontanes aupres de locuteurs natifs de l'Ewe et du Mina (et d'autres langues togolaises) directement via Telegram.

Le script est autonome et ne depend que de la bibliotheque standard Python et de `requests`. Aucun framework lourd n'est requis.

---

## 1. Creation du Bot sur Telegram (2 minutes)

1. Ouvrez Telegram sur votre telephone ou ordinateur.
2. Cherchez l'utilisateur officiel : `@BotFather`.
3. Tapez la commande : `/newbot`.
4. Choisissez un nom pour votre bot (ex: `OpenAfrica Voice Collector`).
5. Choisissez un nom d'utilisateur finissant par `bot` (ex: `openafrica_togo_bot`).
6. BotFather vous donnera immediatement un **Jeton d'acces (API Token)** ressemblant a :
   ```text
   7123456789:AAHk...votre_token...xyz
   ```

---

## 2. Lancement du Bot

Vous pouvez lancer le bot de deux manieres simples :

### Option A : En passant le token directement en ligne de commande
```bash
python3 collecteurs/telegram/bot.py "VOTRE_TOKEN_ICI"
```

### Option B : En exportant la variable d'environnement
```bash
export TELEGRAM_BOT_TOKEN="VOTRE_TOKEN_ICI"
python3 collecteurs/telegram/bot.py
```

---

## 3. Parcours Utilisateur (Experience de Collecte)

1. **Accueil (`/start`)** : Le contributeur recoit un message de bienvenue et peut soit demander un sujet, soit envoyer un vocal.
2. **Animation des sujets (`/sujet`)** : Le bot propose un sujet parmi une selection (cuisine locale, proverbes *lododo*, commerce a Assigame, contes de la tortue, vie quotidienne).
3. **Reception du vocal** :
   * Le contributeur appuie sur le micro de Telegram et parle naturellement en Ewe ou en Mina.
   * Le bot telecharge le fichier audio temporaire.
4. **Qualification en 3 clics** :
   * Question 1 : Ewe, Mina, Kabiye ou autre.
   * Question 2 : Ville d'origine (Lome, Kpalime, Tsevie, Notse, Aneho, Agou, Danyi, etc.).
   * Question 3 : Profil du locuteur (Homme/Femme, tranche d'age).
5. **Sauvegarde et Metadonnees** :
   * Le fichier est automatiquement renomme et deplace dans le bon sous-dossier, par exemple :
     `voix/togo/ewe/kpalime_kloto/ewe_kpalime_kloto_h_adulte_20260909_163012.ogg`
   * Une ligne est ajoutee au fichier d'inventaire `voix/togo/metadonnees_collecte.csv`.

---

## 4. Structure des Donnees Sauvegardees

### Fichier CSV : `voix/togo/metadonnees_collecte.csv`
Colonnes generees automatiquement :
* `id_fichier` : Nom du fichier audio
* `chemin_relatif` : Emplacement exact dans le depot
* `langue` : `ewe` ou `mina`
* `variete_slug` : `be_lome`, `kpalime_kloto`, `aneho_glidji`, etc.
* `ville` : Ville renseignee
* `profil_locuteur` : Tranche d'age et genre
* `sujet_id` : Identifiant du sujet aborde
* `duree_secondes` : Duree exacte de l'audio
* `date_heure` : Horodatage ISO
* `telegram_user_id` : Identifiant anonymise du contributeur
