# collecteurs/telegram/prompts.py
# Banque de sujets de conversation pour le bot Telegram OPENAFRICA
# Garanti sans aucun emoji.

SUJETS_CONVERSATION = [
    {
        "id": "cuisine_akoume",
        "theme": "Cuisine et Gastronomie",
        "question_fr": "Expliquez en detail comment preparer l'Akoume (la pate traditionnelle) ou le Fufu chez vous.",
        "question_ee": "Gblo ale si woɖaa Akple alo Fufu le mia gbɔ le Evegbe me.",
        "question_ge": "Tɔ kpo nɛ wo ɖo a ɖa Akumɛ alo Fufu le Mina me."
    },
    {
        "id": "proverbe_lododo",
        "theme": "Sagesse et Proverbes",
        "question_fr": "Donnez un proverbe (lododo) en Ewe ou en Mina et expliquez sa lecon de vie.",
        "question_ee": "Gblo lododo aɖe le Evegbe me eye naɖe egɔme.",
        "question_ge": "Do lododo ɖeka le Mina me eye nà gblɔ nuxɔlɔ̃ame ci le eme."
    },
    {
        "id": "marche_assigame",
        "theme": "Commerce et Marches",
        "question_fr": "Racontez une scene de negociation ou vos courses au grand marche d'Assigame ou a votre marche local.",
        "question_ee": "Gblo ale si woflea nu le asime kple asidolawo le Evegbe me.",
        "question_ge": "Gblo nuxu so asime yiyi kpo le Mina me."
    },
    {
        "id": "conte_enfance",
        "theme": "Contes et Traditions",
        "question_fr": "Racontez un conte ou une fable traditionnelle (comme les histoires de la tortue / gli) que l'on vous racontait enfant.",
        "question_ee": "Gblo gli aɖe so klo alo lannuwo ŋu le Evegbe me.",
        "question_ge": "Gblo gli so klo ŋu le Mina me."
    },
    {
        "id": "journee_travail",
        "theme": "Vie Quotidienne",
        "question_fr": "Racontez comment s'est passee votre journee, votre metier ou vos projets du moment.",
        "question_ee": "Gblo nu siwo nado go egbe le dɔwɔƒe alo aƒeme le Evegbe me.",
        "question_ge": "Gblo le egbegbe nuxu le Mina me."
    },
    {
        "id": "itineraire_ville",
        "theme": "Geographie et Quartier",
        "question_fr": "Expliquez le chemin pour aller de votre quartier vers un lieu connu (la plage, le marche, l'universite).",
        "question_ee": "Fia mɔ tso wò nɔƒe yi teƒe aɖe si wonya nyuie le du la me.",
        "question_ge": "Fia mɔ so axwe yi asime le Mina me."
    },
    {
        "id": "sante_remede",
        "theme": "Plantes et Sante Traditionnelle",
        "question_fr": "Parlez d'une tisane, plante ou remede traditionnel que votre famille utilise pour soigner la fievre ou les maux de ventre.",
        "question_ee": "Gblo atike gbe siwo mi zana le aƒeme hena dɔlelewo gbɔkpɔkpɔ.",
        "question_ge": "Gblo ama ci wo zana le axwe so dɔlele ŋu."
    }
]

def obtenir_sujet_aleatoire():
    import random
    return random.choice(SUJETS_CONVERSATION)
