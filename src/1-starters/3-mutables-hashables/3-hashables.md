### Hashables

Comme je le disais plus tôt, les objets hashables vont notamment servir pour les clefs des dictionnaires.
Mais voyons tout d'abord à quoi correspond cette capacité.

#### Le condensat

En informatique, et plus particulièrement en cryptographie, on appelle condensat (*hash*) un nombre
- unique pour une valeur
- est invariable
- deux valeurs égales ont le même hash
- attention aux conflits

#### La fonction `hash`

En Python, on peut calculer le condensat d'un objet à l'aide de la fonction `hash`.

```python
>>> hash(10)
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
Pourquoi ? On a vu que le *hash* était invariable, mais devait correspondre à la valeur.

Or, en modifiant une liste, le condensat calculé auparavant deviendrait invalide. Il est donc impossible de hasher les listes.
Il en est de même pour les dictionnaires et les ensembles (`set`).
Tous les autres types d'objets sont par défaut hashables.

On remarque une certaine corrélation entre types mutables et hashables.
En effet, il est plus facile d'assurer l'invariabilité du condensat quand l'objet est lui-même immutable.
Pour les objets mutables, le *hash* n'est possible que si la modification n'altère pas l'égalité entre deux objets.

#### À quoi servent-ils ?

Je parle depuis le début de clefs de dictionnaires, nous allons maintenant voir pourquoi les dictionnaires utilisent des condensats.

Les dictionnaires, d'ailleurs appelés tables de hashage dans certains langages, sont des structures qui doivent permettre un accès rapide aux éléments.
Ainsi, ils ne peuvent pas être une simple liste de couples clef/valeur, qui serait parcourue chaque fois que l'on demande un élément.

À l'aide des *hash*, les dictionnaires disposent les éléments tels que dans un tableau et offre un accès direct à la majorité d'entre eux.

Outre les dictionnaires, ils sont aussi utilisés dans les `set`, ensemble non ordonnés de valeurs uniques.

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

#### Implémentation

Les types de votre création sont par défaut hashables, puisque l'égalité entre objets vaut l'idendité.

- méthode `__hash__`
- résultat tronqué pour la taille fixe
- `__eq__` (si eq est implémentée, hash doit être mise à None ou réimplémentée)
- invariable !
