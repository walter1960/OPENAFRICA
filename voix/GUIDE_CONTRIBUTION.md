# Guide du Contributeur Vocale OPENAFRICA

Merci de participer à la préservation et à la valorisation des langues africaines dans l'intelligence artificielle !

---

## 1. Comment enregistrer ?

Vous n'avez pas besoin d'un microphone professionnel. Un smartphone suffit amplement :
* **Application enregistreur vocal** de votre téléphone (format MP3, M4A, WAV).
* **Notes vocales WhatsApp** (format `.ogg` directement accepté).
* **Enregistrements de radios locales** (émissions de débats, journaux en langues nationales).

---

## 2. Comment nommer votre fichier ?

Pour que les chercheurs et développeurs puissent entraîner l'IA avec précision, essayez de nommer votre fichier selon ce format :

```text
[VILLE]_[GENRE_AGE]_[SUJET]_[NUMERO].[ext]
```

### Exemples :
* **Togo - Éwé** : `lome_h35_conte_001.mp3` *(Lomé, Homme 35 ans, conte)*
* **Togo - Kabiyè** : `kara_f22_discussion_002.ogg` *(Kara, Femme 22 ans, causerie)*
* **Bénin - Fon** : `cotonou_h40_marche_001.m4a` *(Cotonou, Homme 40 ans, négociation)*
* **Bénin - Bariba** : `nikki_h65_proverbe_001.mp3` *(Nikki, Homme 65 ans, proverbe)*
* **Mali - Bambara** : `segou_f30_recit_001.wav` *(Ségou, Femme 30 ans, récit)*
* **Mali - Songhaï** : `gao_h28_radio_001.mp3` *(Gao, Homme 28 ans, radio locale)*

*(Si vous ne connaissez pas l'âge exact, une estimation suffit : `jeune`, `adulte`, `ancien`).*

---

## 3. Comment déposer votre fichier ?

1. Choisissez le dossier : `voix/[pays]/[langue]/`
2. Déposez-y directement votre fichier sonore.
3. C'est tout ! Les programmes automatiques se chargeront du reste (découpage des silences, analyse du pitch et des tons).
