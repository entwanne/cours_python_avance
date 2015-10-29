# Gestionnaires de contexte

Python dispose d'un glaneur de cellules (*garbage collector*), se chargant à votre place de la gestion de la mémoire. Une utilisation fine de celle-ci peut ainsi s'avérer difficile.

Les objets possèdent un destructeur `__del__`, mais on ne sait pas bien quand l'interpréteur décidera de détruire réellement l'objet. Lorsqu'on sort du scope de la variable ou que l'on utilise `del`, on ne fait que supprimer une référence vers l'objet. Tant que d'autres références existent, l'objet ne pourra être détruit.

Et même une fois le compteur de références arrivé à 0, on ne peut s'assurer que la destruction aura lieu tout de suite.

Pourtant, une gestion déterministe des ressources peut s'avérer utile, et c'est là qu'interviennent les gestionnaires de contexte (*context managers*) et leur mot-clef `with`.
