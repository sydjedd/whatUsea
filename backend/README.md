# WhatUsea backend

Application qui récupére les observations de certains animaux marins à proximité des îlots de la province sud de la Nouvelle-Calédonie.

## Pré-requis

* Python
* PIP

## Installation

### Créer le fichier dotenv

> Ne pas oublier de remplacer "***baseDeDonnees***", "***utilisateur***" et "***motDePasse***" par les ceux de la base de données whatusea

```dotenv
ENV=development
ALLOWED_HOSTS=localhost,127.0.0.1
FRONTEND_URL=http://localhost:8080

DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_NAME=baseDeDonnees
DATABASE_USER=utilisateur
DATABASE_PASSWORD=motDePasse
```

### Installer l'environnement virtuel

```shell
python3 -m venv venv
```

### Activer l'environnement virtuel

```shell
. venv/bin/activate
```

### Mise à jour de pip

```shell
pip3 install --upgrade pip
```

### Installer les dépendances

```shell
pip3 install -r requirements.txt
```

### Création des tables

```shell
python3 manage.py makemigrations observation referential
python3 manage.py migrate
```

### Importer les référentiels et le jeu d'essai

```shell
python3 manage.py loaddata referential
python3 manage.py loaddata observation
```

## Lancer l'application en développement

```shell
python3 manage.py runserver 0.0.0.0:8000
```

## Désactiver l'environnement virtuel

```shell
deactivate
```

## API

|Méthode    |URL                       |Description                                                               |
|-----------|--------------------------|--------------------------------------------------------------------------|
|GET        |/observation/?species={id}|Liste toutes les observation, filtre sur id de l'espèce (voir référentiel)|
|POST       |/observation/             |Création d'une observation                                                |
|GET        |/observation/{id}         |Détails de l'observation dont l'ID est {id}                               |
|PUT        |/observation/{id}         |Modification de l'observation dont l'ID est {id}                          |
|DELETE     |/observation/{id}         |Suppression de l'observation dont l'ID est {id}                           |
|GET        |/referential/             |Liste tous les référentiels                                               |
|GET        |/referential/quality/     |Liste toutes les qualités d'identification                                |
|GET        |/referential/family/      |Liste toutes les familles d'animaux                                       |
|GET        |/referential/species/     |Liste toutes les espèces                                                  |

### Entité observation
|Paramètres           |Type      |Nullable|Descritption              |
|---------------------|----------|--------|--------------------------|
|ilot                 |id        |        |voir référentiel API Ïlot |
|ilot_distance        |entier    |        |entier > 0                |
|date_time            |date heure|        |format YYYY-MM-DD HH:MM:SS|
|quality              |id        |        |voir referentiel quality  |
|species              |id        |        |voir référentiel species  |
|fish_single          |boolean   |oui     |True ou False             |
|fish_number          |entier    |oui     |entier > 0                |
|animal_length        |entier    |oui     |entier > 0                |
|mammel_apnea_duration|entier    |oui     |entier > 0                |

### Entité quality, family, species
|Paramètres|Type  |Nullable|Descritption|
|----------|------|--------|------------|
|id        |entier|        |            |
|libelle   |chiane|        |            |

### Ïlot

|Méthode    |URL                                                             |Description                         |
|-----------|----------------------------------------------------------------|------------------------------------|
|GET        |https://www.province-sud.nc/pandoreweb/pandore/ilot/IlotDto/    |Liste de tous les ilôts             |
|GET        |https://www.province-sud.nc/pandoreweb/pandore/ilot/IlotDto/{id}|Détails de l'ilôt dont l'ID est {id}|

### Entité Ïlot
[Lien API Ïlot](https://www.province-sud.nc/swagger/?url=/pandoreweb/openapi)