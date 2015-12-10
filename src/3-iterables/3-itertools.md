## Utilisation avancée : le module `itertools`

Nous l'avons vu, les itérables sont au cœur des fonctions élémentaires de Python. Je voudrais maintenant vous présenter un module qui vous sera propablement très utile : [`itertools`](https://docs.python.org/3/library/itertools.html).

Ce module met à disposition de nombreux itérables plutôt variés, dont :

- `chain(p, q, ...)` — Met bout à bout plusieurs itérables ;
- `islice(p, start, stop, step)` — Fait un travail semblable aux slices, mais en travaillant avec des itérables (nul besoin de pouvoir indexer notre objet) ;
- `combinations(p, r)` — Retourne toutes les combinaisons de `r` éléments possibles dans `p` ;
- `zip_longest(p, q, ...)` — Similaire à `zip`, mais s'aligne sur l'itérable le plus grand plutôt que le plus petit (en permettant de spécifier une valeur de remplissage).

```python
>>> import itertools
>>> itertools.chain('abcd', [1, 2, 3])
<itertools.chain object at 0x7f757b508c88>
>>> list(itertools.chain('abcd', [1, 2, 3]))
['a', 'b', 'c', 'd', 1, 2, 3]
>>> list(itertools.islice(itertools.chain('abcd', [1, 2, 3]), 1, None, 2))
['b', 'd', 2]
>>> list(itertools.combinations('abc', 2))
[('a', 'b'), ('a', 'c'), ('b', 'c')]
>>> list(itertools.zip_longest('abcd', [1, 2, 3]))
[('a', 1), ('b', 2), ('c', 3), ('d', None)]
```

Je tiens enfin à attirer votre attention sur les [recettes (*recipes*)](https://docs.python.org/3/library/itertools.html#itertools-recipes), un ensemble d'exemples qui vous sont proposés mettant à profit les outils présents dans `itertools`.
