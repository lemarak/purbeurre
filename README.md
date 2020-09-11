# Openclassrooms : DA Python : Projet 8

## Contexte

Projet réalisé dans le cadre de la formation OpenClassrooms, parcours Développement d'applications Python.
La startup Pur Beurre, souhaite développer une plateforme web à destination de ses clients. Ce site permettra à quiconque de trouver un substitut sain à un aliment considéré comme "Trop gras, trop sucré, trop salé"
Un cahier des charges précis est fourni par le client.
Les données seront importés à partir de l'api OpenFoodFacts.

## Présentation

### Organisation

Application centrale du projet :
- **purbeurre_project** : avec le fichier de paramètrage et les routes pour l'accés aux autres applications

Le projet contient trois applications liées à des fonctionnalités précises :
- **Users** : fonctionnalités permettant la gestion des utilisateurs
- **Products** : l'application permettant la sauvegarde des favoris préférés
- **Pages** : l'application se chargeant des produits en eux-mêmes

Et un dossier 
- **static** : fichiers nécessaires pour l'application (images, css...)


### Déploiement

Le déploiement est réalisé sur la plateforme Heroku.
[oc-purbeurre-dauguet.herokuapp.com/](https://oc-purbeurre-dauguet.herokuapp.com/ "PurBeurre - sdauguet")

Le fichier de configuration est Procfile
Variables d'environnement créées dans heroku :
`DATABASE_URL`
`ENV`: "production"
`PWD_DB`
`SECRET_KEY`
`USER`


### Données fournis par l'api

Pour l'import des données, la commande est  `python manage.py import_api`

### Tests

L'éxécution des tests se fait à partir de la commande `python manage.py test`.
La mesure de la couverture se lance avec `coverage run manage.py test`