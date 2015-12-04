## Utilisation des callables

De même que pour les itérables, les *callables* sont au cœur de Python en pouvant être utilisés avec un grand nombre de builtins.

Par exemple, la fonction `max` évoquée dans un précédent chapitre : en plus de prendre un itérable sur lequel trouver le maximum, elle peut aussi prendre un paramètre `key`. Ce paramètre est un *callable* expliquant comment extraire le maximum depuis les arguments passés à `max`.
Si l'itérable ne contient que des entiers, il est plutôt simple de déterminer le maximum, mais si nous avons une liste de points 2D par exemple ?
Le maximum pourrait être le point avec la plus grande abscisse, la plus grande ordonnée, le point le plus éloigné de l'origine du repère, ou encore bien d'autres choses.

Le *callable* `key` est donc chargé de calculer une valeur numérique pour chacun des paramètres, et pouvoir ainsi les comparer entre-eux. Le paramètre ayant la plus grande valeur sera le maximum.

Nous représenterons ici nos points par des tuples de deux valeurs.

```python
>>> points = [(0, 0), (1, 4), (3, 3), (4, 0)]
>>> max(points) # par défaut, Python sélectionne suivant le premier élément, soit l'abscisse
(4, 0)
>>> max(points, key=lambda p: p[0]) # Nous précisons ici explicitement la sélection par l'abscisse
(4, 0)
>>> max(points, key=lambda p: p[1]) # Par ordonnée
(1, 4)
>>> max(points, key=lambda p: p[0]**2 + p[1]**2) # Par distance de l'origine
(3, 3)
```

En dehors de `max`, d'autres fonctions Python prennent un tel paramètre key, comme `min` ou encore `sorted` :

```python
>>> sorted(points, key=lambda p: p[1])
[(0, 0), (4, 0), (3, 3), (1, 4)]
>>> sorted(points, key=lambda p: p[0]**2 + p[1]**2)
[(0, 0), (4, 0), (1, 4), (3, 3)]
```

`map`, que nous avons déjà vu, prend lui aussi un *callable* de n'importe quel type.

```python
>>> list(map(lambda p: p[0], points))
[0, 1, 3, 4]
>>> list(map(lambda p: p[1], points))
[0, 4, 3, 0]
```

Je vous invite une nouvelle fois à jeter un œil aux builtins Python, ainsi qu'au module `itertools`, et de voir lesquels peuvent vous faire tirer profit des *callables*.
