# Projet MSI

## Réalisé par :
- JAKOBOWSKI Aymeric
- BOBEUF Jules
- SANTORO Thomas

## Comment utiliser notre application ?

### Installation :

Notre application a été conçue pour être la plus simple d'utilisation possible.

Afin de pouvoir utiliser notre application, vous devez vous rendre sur le projet GitLab grâce au lien suivant : https://gitlab.univ-artois.fr/thomas_santoro/projet-msi

Une fois ceci réalisé, vous pouvez cliquer sur le bouton bleu a droite de votre écran `Clone`. Ceci vous donne l’accès à un URL que vous devez copier.

Maintenant que vous avez réalisé ceci, vous pouvez le cloner dans un dossier que vous aurez créé au préalable.

Pour cloner un projet, il vous suffit de vous rendre dans le dossier créé, de faire un clic droit et de sélectionner « ouvrir dans un terminal » une fois cela fait écrivez dans votre terminal la commande : git clone « L’url copié au préalable ».

Une fois cette étape finie, il ne vous reste plus qu’à ouvrir le projet et de le lancer dans une application. Nous vous conseillons PyCharm ou Visual Studio Code par exemple.

Veuillez avoir installé toutes les dépendances nécessaires, sinon le projet ne marchera pas. 

Afin que le fichier `.env` soit bien compatible avec l'application, veuillez exécuter cette commande :
```
pip install python-dotenv
```

Et pour terminer vous n’avez plus qu’à lancer le projet et vous rendre sur l’URL donné par l’application.

### Utilisation :

Une fois rendu sur l’URL récupérer grâce à l’installation précédente il n’y a rien de plus simple vous devez simplement remplir la case avec le nom de la ville que vous souhaitez et ceci vous permettra de récupérer toutes les informations sur cette ville.

Notez bien que les informations sont mises à jour chaque heures.

Pour vérifier que les informations sont bien rajoutées dans la base de données, il suffit d’ouvrir le fichier `logs.txt` qui se situe à la racine du fichier. Celui-ci est rempli automatiquement par l’application après chaque ajout de données.

J’espère que notre application vous plaira.
