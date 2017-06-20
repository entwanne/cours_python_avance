### Égalité et identité

L'égalité et l'identité sont deux concepts dont la distinction est parfois confuse.
Deux valeurs sont égales lorsqu'elles partagent un même état : par exemple, deux chaînes qui contiennent les mêmes caractères sont égales.
Deux valeurs sont identiques lorsqu'elles sont une même instance, c'est-à-dire un même objet en mémoire.

En Python, on retrouve ces concepts sous les opérateurs `==` (égalité) et `is` (identité).

```python
>>> [1, 2, 3] == [1, 2, 3]
True
>>> [1, 2, 3] is [1, 2, 3]
False
>>> values = [1, 2, 3]
>>> values is values
True
```

Leur différence est fondamentale pour les types mutables, puisque deux valeurs distinctes peuvent être égales à un moment et ne plus l'être par la suite (si l'une d'elles est modifiée).
Deux valeurs identiques resteront à l'inverse égales, puisque les modifications seront perçues sur les deux variables.

```python
>>> values1, values2 = [1, 2, 3], [1, 2, 3]
>>> values1 == values2
True
>>> values1 is values2
False
>>> values1.append(4)
>>> values1 == values2
False
```

```python
>>> values1 = values2 = [1, 2, 3]
>>> values1 == values2
True
>>> values1 is values2
True
>>> values1.append(4)
>>> values1 == values2
True
```

L'opérateur d'égalité est surchargeable en Python, *via* la méthode spéciale `__eq__` des objets.
Il est en effet de la responsabilité du développeur de gérer la comparaison entre ses objets, et donc de déterminer quand ils sont égaux.
Cette méthode reçoit en paramètre la valeur à laquelle l'objet est comparé, et retourne un booléen.

On peut imaginer une valeur qui sera égale à toute les autres, grâce à une méthoe `__eq__` retournant toujours `True`.

```python
>>> class AlwaysEqual:
...     def __eq__(self, value):
...         return True
...
>>> val = AlwaysEqual()
>>> val == 0
True
>>> 1 == val
True
```

L'opérateur d'identité testant si deux objets sont une même instance, il n'est bien sûr pas possibe de le surcharger.
En absence de surcharge, l'opérateur d'égalité donnera la même résultat que l'identité.

Vous pouvez vous référer à [ce chapitre du cours sur la POO en Python](https://zestedesavoir.com/tutoriels/1253/la-programmation-orientee-objet-en-python/4-operators/)
pour davantage d'informations sur la surcharge d'opérateurs.

#### Quel opérateur utiliser ?

Une question légitime à se poser suite à ces lignes est de savoir quel opérateur utiliser pour comparer nos valeurs.
La réponse est que cela dépend des valeurs et des cas d'utilisation.

En règle générale, c'est l'opérateur d'égalité (`==`) qui est à utiliser.
Quand nous comparons un nombre entré par l'utilisateur avec un nombre à deviner, nous ne cherchons pas à savoir s'ils sont un même objet, mais s'ils représentent la même chose.

L'opérateur `is` s'utilise principalement avec `None`.
`None` est une valeur unique (*singleton*), il n'en existe qu'une instance.
Quand on compare une valeur avec `None`, on vérifie qu'elle est `None` et non qu'elle vaut `None`.

Globalement, `is` s'utilise pour la comparaison avec des *singletons*, et `==` s'utilise pour le reste.
