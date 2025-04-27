BiglobeValidator v1.0
===================

BiglobeValidator est un outil professionnel qui permet de tester automatiquement
des listes de comptes email:password via connexion SMTP.
Il identifie rapidement les comptes valides et enregistre les résultats.

Fonctionnalités :
-----------------
- Validation Biglobe rapide et fiable
- Connexion sécurisée SSL/TLS
- Support du format email:password
- Résultats sauvegardés proprement
- Multi-threading pour plus de vitesse
- Affichage console propre avec logo
- Interruption sécurisée avec Ctrl+C

Installation :
--------------
1. Installer Python 3.8 ou supérieur.
2. Télécharger le fichier smtp_validator.py.

Utilisation :
-------------
Lancer le script :

    python smtp_validator.py

Le script vous demandera :
- Le chemin du fichier d'entrée (email:password par ligne)
- Le chemin du fichier de sortie (emails valides)
- L'email de réception pour les tests SMTP

Exemple de fichier d'entrée :

    test1@biglobe.ne.jp:password1
    test2@biglobe.ne.jp:password2
    test3@biglobe.ne.jp:password3

Exemple de résultat de sortie :

    test1@biglobe.ne.jp:password1
    test3@biglobe.ne.jp:password3

Configuration rapide :
----------------------
Vous pouvez ajuster dans le script :
- Nombre de threads (THREADS)
- Délai entre chaque test (DELAY_BETWEEN_CHECKS)
- Serveur SMTP ciblé (SMTP_SERVER)
- Port SMTP (SMTP_PORT)

Remarques :
-----------
- Plus de threads = plus rapide, mais plus de risques de blocages SMTP.
- Assurez-vous que l'email de réception est accessible sans filtrage.
- L'usage est sous votre seule responsabilité.

Support :
---------
Pour toute question ou développement sur mesure :
support@smtp-validator.pro

Licence :
---------
Usage éducatif uniquement.
L'utilisation commerciale ou abusive est de la responsabilité de l'utilisateur.

