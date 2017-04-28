### C'est pas la taille qui compte

Un autre point commun partagé par de nombreux conteneurs est qu'ils possèdent une taille.
C'est à dire qu'ils contiennent un nombre fini et connu d'éléments, et peuvent être passés en paramètre à la fonction `len` par exemple.

```python
>>> len([1, 2, 3])
3
>>> len(MyContainer())
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: object of type 'MyContainer' has no len()
```

Comme pour l'opérateur `in`, la fonction `len` fait appel à une méthode spéciale de l'objet, `__len__`, qui ne prend ici aucun paramètre et doit retourner un nombre entier positif.

```python
>>> len('toto')
4
>>> 'toto'.__len__()
4
```

Nous pouvons donc aisément donner une taille à nos objets :

```python
>>> class MySizeable:
...     def __len__(self):
...         return 18
...
>>> len(MySizeable())
18
```

Je vous invite à faire des essais en retournant d'autres valeurs (nombres négatifs, flottants, chaînes de caractères) pour observer le comportement.
