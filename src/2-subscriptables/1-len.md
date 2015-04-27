## C'est pas la taille qui compte

Tous ces objets ont déjà un premier point commun: ils ont une taille, c'est à dire qu'ils peuvent être passés en paramètre à la fonction `len` par exemple, contrairement à un nombre entier.

```python
>>> len([1, 2, 3])
3
>>> len(42)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: object of type 'int' has no len()
```

Comment cela fonctionne ? C'est très simple. Comme pour de nombreux comportements, python se base sur des méthodes spéciales des objets, vous en connaissez déjà probablement, ce sont les méthodes dont les noms débutent et s'achèvent par `__`.

Ici, la fonction `len` de python fait simplement appel à la méthode `__len__` de l'objet, qui doit retourner un nombre entier positif.

```python
>>> len('toto')
4
>>> 'toto'.__len__()
4
```

Ainsi, il nous suffit d'implémenter cette méthode pour que notre objet ait une taille:

```python
>>> class MyObject:
...     def __len__(self):
...         return 18
...
>>> len(MyObject())
18
```

Je vous invite à faire des essais en retournant d'autres valeurs (nombres négatifs, flottants, chaînes de caractères) pour observer le comportement.
