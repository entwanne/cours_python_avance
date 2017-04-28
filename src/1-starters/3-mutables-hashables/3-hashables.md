### Hashables

Comme je le disais plus tôt, les objets hashables vont notamment servir pour les clefs des dictionnaires.
Mais voyons tout d'abord à quoi correspond cette capacité.

#### Le condensat

En informatique, et plus particulièrement en cryptographie, on appelle condensat (*hash*) un nombre calculé depuis une valeur quelconque, unique et invariable pour cette valeur.
Deux valeurs égales partageront un même *hash*, deux valeurs différentes auront dans la mesure du possible des *hash* différents.

En effet, le condensat est généralement un nombre de taille fixe (64 bits par exemple), il existe donc un nombre limité de *hashs* pour un nombre infini de valeurs.
Deux valeurs différentes pourront alors avoir un même condensat, c'est ce que l'on appelle une collision.
Les collisions sont plus ou moins fréquentes selon les algorithmes de *hashage*.
En cela, l'égalité entre *hashs* ne doit jamais remplacer l'égalité entre les valeurs, elle n'est qu'une étape préliminaire qui peut servir à optimiser des calculs.

#### La fonction `hash`

En Python, on peut calculer le condensat d'un objet à l'aide de la fonction `hash`.

```python
>>> hash(10)
10
>>> hash(2**61 + 9) # collision
10
>>> hash('toto')
-7475273891964572862
>>> hash((1, 2, 3))
2528502973977326415
>>> hash([1, 2, 3])
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: unhashable type: 'list'
```

Ce dernier exemple nous montre que les listes ne sont pas hashables.
Pourquoi ? On a vu que le *hash* était invariable, mais il doit pourtant correspondre à la valeur.

Or, en modifiant une liste, le condensat calculé auparavant deviendrait invalide. Il est donc impossible de hasher les listes.
Il en est de même pour les dictionnaires et les ensembles (`set`).
Tous les autres types d'objets sont par défaut hashables.

On remarque une certaine corrélation entre types mutables et hashables.
En effet, il est plus facile d'assurer l'invariabilité du condensat quand l'objet est lui-même immutable.
Pour les objets mutables, le *hash* n'est possible que si la modification n'altère pas l'égalité entre deux objets, c'est à dire que deux objets égaux le resteront même si l'un est modifié.

Il faut aussi garder à l'esprit que des types immutables peuvent contenir des mutables. Par exemple une liste dans un *tuple*.
Dans ce genre de cas, la non-hashabilité des valeurs contenues rend non-hashable le conteneur.

```python
>>> t = ((0, 1), (2, 3))
>>> hash(t)
8323144716662114087
>>> t = ((0, 1), [2, 3])
>>> hash(t)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: unhashable type: 'list'
```

#### À quoi servent-ils ?

Je parle depuis le début de clefs de dictionnaires, nous allons maintenant voir pourquoi les dictionnaires utilisent des condensats.

Les dictionnaires, d'ailleurs appelés tables de hashage dans certains langages, sont des structures qui doivent permettre un accès rapide aux éléments.
Ainsi, ils ne peuvent pas être une simple liste de couples clef/valeur, qui serait parcourue chaque fois que l'on demande un élément.

À l'aide des *hash*, les dictionnaires disposent les éléments tels que dans un tableau et offrent un accès direct à la majorité d'entre eux.

Outre les dictionnaires, ils sont aussi utilisés dans les `set`, ensembles non ordonnés de valeurs uniques.

On remarque facilement que les objets non-hashables ne peuvent être utilisés en tant que clefs de dictionnaires ou dans un ensemble.

```python
>>> {[0]: 'foo'}
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: unhashable type: 'list'
>>> {{'foo': 'bar'}}
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: unhashable type: 'dict'
```

Plus généralement, les *hash* peuvent être utilisés pour optimiser le test d'égalité entre deux objets.
Le *hash* étant invariable, il est possible de ne le calculer qu'une fois par objet (en stockant sa valeur).

Ainsi, lors d'un test d'égalité, on peut facilement dire que les objets sont différents, si les *hash* le sont.
L'inverse n'est pas vrai à cause des collisions : deux objets différents peuvent avoir un même *hash*.
Le test d'égalité proprement dit (appel à la méthode `__eq__`) doit donc toujours être réalisé si les *hash* sont égaux.

#### Implémentation

Les types de votre création sont par défaut hashables, puisque l'égalité entre objets vaut l'idendité.
La question de la *hashabilité* ne se pose donc que si vous surchargez l'opérateur `__eq__`.

Dans ce cas, il convient normalement de vous occuper aussi de la méthode spéciale `__hash__`.
C'est cette méthode qui est appelée par la fonction `hash` pour calculer le condensat d'un objet.

Il est aussi possible d'assigner `None` à `__hash__` afin de rendre l'objet non-*hashable*.
Python le fait par défaut lorsque nous surchargeons l'opérateur `__eq__`.

Pour reprendre la classe `AlwaysEqual` définie précédemment :

```python
>>> val = AlwaysEqual()
>>> hash(val)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: unhashable type: 'AlwaysEqual'
>>> print(val.__hash__)
None
```

Si toutefois vous souhaitez redéfinir la méthode `__hash__`, il vous faut respecter les quelques règles énoncées plus haut.

- L'invariabilité du *hash* ;
- L'égalité entre deux *hashs* de valeurs égales.

Ces conditions état plus faciles à respecter pour des valeurs immutables.

Notons enfin que le résultat de la méthode `__hash__` est tronqué par la fonction `hash`, afin de tenir sur un nombre fixe de bits.

Pour plus d'informations sur cette méthode `__hash__` : <https://docs.python.org/3/reference/datamodel.html#object.__hash__>.
