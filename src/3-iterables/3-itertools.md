## Utilisation avancée: le module `itertools`

Nous l'avons vu, les itérables sont au cœur des fonctions élémentaires de Python. Je voudrais maintenant vous présenter un module qui vous sera propablement très utile: [`itertools`](https://docs.python.org/3/library/itertools.html).

Ce module vous met à disposition de nombreux itérateurs plutôt variés, dont:

- `chain(p, q, ...)` — Met bout à bout plusieurs itérables.
- `islice(p, start, stop, step)` — Fait un travail semblable aux slices, mais en travaillant avec des itérables (nul besoin de pouvoir indéexer notre objet).
- `combinations(p, r)` — Retourne toutes les combinaisons de `r` éléments possibles dans `p`.
- `zip_longest(p, q, ...)` — Similaire à `zip`, mais s'aligne sur l'itérable le plus grand plutôt que le plus petit (en permettant de spécifier une valeur de remplissage).

Je tiens enfin à attrirer votre attention sur les [recettes (*recipes*)](https://docs.python.org/3/library/itertools.html#itertools-recipes), un ensemble d'exemple qui vous sont proposés mettant à profit les outils présents dans `itertools`.
