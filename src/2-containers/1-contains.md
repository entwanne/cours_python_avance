### Les conteneurs, c'est `in`

Comme indiqué, les conteneurs sont donc des objets qui contiennent d'autres objets.
Ils se caractérisent par l'opérateur `in` : `(0, 1, 2, 3)` étant un conteneur, il est possible de tester s'il contient telle ou telle valeur à l'aide de cet opérateur.

```python
>>> 3 in (0, 1, 2, 3)
True
>>> 4 in (0, 1, 2, 3)
False
```

Comment cela fonctionne ? C'est très simple. Comme pour de nombreux comportements, Python se base sur des méthodes spéciales des objets, vous en connaissez déjà probablement, ce sont les méthodes dont les noms débutent et s'achèvent par `__`.

Ici, l'opérateur `in` fait simplement appel à la méthode `__contains__` de l'objet, qui prend en paramètre l'opérande gauche, et retourne un booléen.

```python
>>> 'o' in 'toto'
True
>>> 'toto'.__contains__('o')
True
```

Il nous suffit ainsi d'implémenter cette méthode pour faire de notre objet un conteneur.

```python
>>> class MyObject:
...     def __contains__(self, value):
...         return value is not None # contient tout sauf None
...
>>> 'salut' in MyObject()
True
>>> 1.5 in MyObject()
True
>>> None in MyObject()
False
```
