# OPENAFRICA

> **L'ecosysteme d'IA Audio-First & Tonal-Aware pour les langues africaines.**
> Batir l'intelligence artificielle pour les langues d'Afrique en partant de la parole, de la melodie et des tons.

---

## La Vision OPENAFRICA

La majorite des modeles d'IA modernes imposent un biais occidental : **le texte d'abord**. 
Pour des langues ouest-africaines fondamentalement orales et tonales (Ewe, Mina, Kabiye, Fon, Yoruba, Bambara...), forcer la parole dans un moule texte non diacrite detruit le sens :
- En **Ewe**, l'orthographe plate `to` peut signifier l'oreille (*to* ton haut), le pere (*to* ton haut voyelle ouverte), la riviere (*to* ton bas), ou trois (*eto*).
- A l'oral, **l'ambiguite est nulle** car le ton (la hauteur melodique F0) et le timbre portent le sens.

**OPENAFRICA** est une initiative communautaire panafricaine open-source concue pour :
1. Collecter et preserver le patrimoine vocal des langues africaines a travers les **54 pays du continent**, variete par variete.
2. Developper des pipelines acoustiques adaptes qui respectent les tons et les dialectes.
3. Rendre la contribution ultra-accessible : **chacun peut enrichir la langue de sa communaute sans barriere technique**.

---

## Architecture des 54 Pays Africains

L'ensemble des **54 pays souverains africains** est structure dans le repertoire [`voix/`](voix/README.md) :

```text
voix/
|-- afrique_du_sud/
|-- algerie/
|-- angola/
|-- benin/
|-- botswana/
|-- burkina_faso/
|-- burundi/
|-- cameroun/
|-- cap_vert/
|-- centrafrique/
|-- comores/
|-- congo_brazzaville/
|-- congo_rdc/
|-- cote_divoire/
|-- djibouti/
|-- egypte/
|-- erythree/
|-- eswatini/
|-- ethiopie/
|-- gabon/
|-- gambie/
|-- ghana/
|-- guinee/
|-- guinee_bissau/
|-- guinee_equatoriale/
|-- kenya/
|-- lesotho/
|-- liberia/
|-- libye/
|-- madagascar/
|-- malawi/
|-- mali/
|-- maroc/
|-- maurice/
|-- mauritanie/
|-- mozambique/
|-- namibie/
|-- niger/
|-- nigeria/
|-- ouganda/
|-- rwanda/
|-- sao_tome_et_principe/
|-- senegal/
|-- seychelles/
|-- sierra_leone/
|-- somalie/
|-- soudan/
|-- soudan_du_sud/
|-- tanzanie/
|-- tchad/
|-- togo/
|-- tunisie/
|-- zambie/
`-- zimbabwe/
```

Chaque dossier de pays comprend :
* Une fiche pays `README.md` detaillant les langues nationales, familles linguistiques et aires geographiques.
* Les sous-dossiers des langues principales avec fiches explicatives et directives de collecte.

---

## Comment contribuer en 3 etapes ?

Aucune competence en programmation n'est requise pour participer :

1. **Rendez-vous dans le dossier de votre pays et de votre langue** (ex: `voix/togo/ewe/`, `voix/mali/bambara/`, `voix/senegal/wolof/` ou `voix/rdc/lingala/`).
2. **Deposez vos enregistrements audio** :
   * Notes vocales spontanees (WhatsApp, conversations).
   * Extraits de radios locales (debats, journaux en langues nationales).
   * Contes traditionnels, proverbes et recits d'anciens.
3. **Consultez le guide pratique** : [GUIDE_CONTRIBUTION.md](voix/GUIDE_CONTRIBUTION.md) pour les conseils de nommage des fichiers.

---

## Communaute et Licence

Ce projet est distribue sous licence [MIT](LICENSE) et appartient a l'ensemble des communautes de locuteurs africains et de la diaspora.
