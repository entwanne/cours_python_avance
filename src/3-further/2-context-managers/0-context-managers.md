## Gestionnaires de contexte

Avant de parler de cette spécificité du langage, je voudrais expliciter la notion de contexte.
Un contexte est une portion de code cohérente, avec des garanties en entrée et en sortie.

Par exemple, pour la lecture d'un fichier, on garantit que celui-ci soit ouvert et accessible en écriture en entrée (donc à l'intérieur du contexte), et l'on garantit sa fermeture en sortie (à l'extérieur).

De multiples utilisations peuvent être faites des contextes, comme l'allocation et la libération de ressources (fichiers, verrous, etc.), ou encore des modifications temporaires sur l'environnement courant (répertoire de travail, redirection d'entrées/sorties).

Python met à notre disposition des gestionnaires de contexte, c'est-à-dire une structure de contrôle pour les mettre en place, à l'aide du mot-clef `with`.
