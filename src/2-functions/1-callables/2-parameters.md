### Paramètres de fonctions

#### Paramètres et arguments

Parlons un peu des paramètres de fonctions (et plus généralement de *callables*). Les paramètres sont décrits lors de la définition de la fonction, ils possèdent un nom, et potentiellement une valeur par défaut.

Il faut les distinguer des arguments : les arguments sont les valeurs passées lors de l'appel.

```python
def function(a, b, c, d=1, e=2):
    return
```

`a`, `b`, `c`, `d` et `e` sont les paramètres de la fonction `function`. `a`, `b` et `c` n'ont pas de valeur par défaut, il faut donc en préciser explicitement lors de l'appel, pour que celui-ci soit valide. Les paramètres avec valeur par défaut se placent obligatoirement après les autres.

```python
function(3, 4, d=5, c=3)
```

Nous sommes là dans un appel de fonction, donc les valeurs sont des arguments.
`3` et `4` sont des arguments positionnels, car ils sont repérés par leur position, et seront donc associés aux deux premiers paramètres de la fonction (`a` et `b`).
`d=5` et `c=3` sont des arguments nommés, car la valeur est précédée du nom du paramètre associé. Ils peuvent ainsi être placés dans n'importe quel ordre (pour peu qu'ils soient placés après les arguments positionnels).

Des paramètres avec valeur par défaut peuvent recevoir des arguments positionnels, et des paramètres sans valeur par défaut peuvent recevoir des arguments nommés.
Les deux notions, même si elles partagent une notation commune, sont distinctes.

Voici enfin différents cas d'appels posant problème :

```python
>>> function(1) # Pas assez d'arguments
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: function() missing 2 required positional arguments: 'b' and 'c'
>>> function(1, 2, 3, 4, 5, 6) # Trop d'arguments
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: function() takes from 3 to 5 positional arguments but 6 were given
>>> function(1, b=2, 3) # Mélange d'arguments positionnels et nommés
  File "<stdin>", line 1
SyntaxError: non-keyword arg after keyword arg
>>> function(1, 2, b=3, c=4) # b est à la fois positionnel et nommé
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: function() got multiple values for argument 'b'
```

#### Opérateur *splat*, le retour

On retrouve l'opérateur *splat* que nous avions vu lors des assignations dans le chapitre sur les Itérables.
Il nous permet ici de récupérer la liste (ou plus précisément le `tuple`) des arguments positionnels passés lors d'un appel, on appelle cela le *packing*.

```python
>>> def func(*args): # Il est conventionnel d'appeler args la liste ainsi récupérée
...     print(args)
...
>>> func(1, 2, 3, 'a', 'b', None)
(1, 2, 3, 'a', 'b', None)
```

La présence d'`*args` n'est pas incompatible avec celle d'autres paramètres.

```python
>>> def func(foo, bar, *args):
...     print(foo)
...     print(bar)
...     print(args)
...
>>> func(1, 2, 3, 'a', 'b', None)
1
2
(3, 'a', 'b', None)
```

Les paramètres placés avant `*args` pourront toujours recevoir des arguments positionnels comme nommés.
Mais ceux placés après ne seront éligibles qu'aux arguments nommés (puisqu'`*args` aura récupéré le reste des positionnels).

```python
>>> def func(foo, *args, bar):
...     print(foo)
...     print(args)
...     print(bar)
...
>>> func(1, 2, 3, 'a', 'b', None)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: func() missing 1 required keyword-only argument: 'bar'
>>> func(1, 2, 3, 'a', 'b', None, bar='c')
1
(2, 3, 'a', 'b', None)
c
```

On notera aussi que *splat* peut s'utiliser sans nom de paramètre, pour marquer une distinction entre les types d'arguments.

```python
def func(foo, *, bar):
    print(foo)
    print(bar)
```

Ici, aucune récupération de la liste des arguments nommés n'est opérée.
Mais `foo`, placé à gauche de `*`, peut prendre un argument positionnel ou nommé, alors que `bar` placé à droite ne peut recevoir qu'un argument nommé.

```python
>>> func(1, bar=2)
1
2
>>> func(foo=1, bar=2)
1
2
>>> func(bar=2, foo=1)
1
2
```

Je disais plus haut que les paramètres avec valeur par défaut se plaçaient obligatoirement après ceux sans.
Ceci est à nuancer avec l'opérateur *splat*, qui sépare en deux parties la liste des paramètres : cela n'est vrai qu'à gauche du *splat*.
À droite, cela n'importe pas puisque tous les paramètres recevront des arguments nommés (donc sans notion d'ordre).

```python
>>> def f(a, b=1, *, d): pass
...
>>> def f(a, b=1, *, d=2): pass
...
>>> def f(a, b=1, *, d=2, e): pass
...
>>> def f(a, b=1, *, d=2, e, f=3): pass
...
>>> def f(a, b=1, *, d, e=2, f, g=3): pass
...
```

#### Le double-*splat*

Enfin, outre l'opérateur *splat* que nous connaissions déjà, on découvre ici le double-*splat* (`**`).
Cet opérateur sert à récupérer le dictionnaire des arguments nommés.
Celui-ci doit se placer après tous les paramètres, et se nomme habituellement `kwargs`.

```python
>>> def func(a, b=1, **kwargs):
...     print(kwargs)
...
>>> func(0)
{}
>>> func(0, b=2)
{}
>>> func(0, c=3)
{'c': 3}
```

En combinant ces deux opérateurs, une fonction est donc en mesure de récupérer l'ensemble de ses arguments (positionnels et nommés).

```python
def func(*args, **kwargs):
    pass
```

On notera que contrairement au simple *splat* qui servait aussi pour les assignations, le double n'a aucune signification en dehors des arguments de fonctions.

#### L'appel du *splat*

Mais ces opérateurs servent aussi lors de l'appel à une fonction, via l'*unpacking*.
Comme pour les assignations étudiées dans le chapitre des itérables, il est possible de transformer un itérable en arguments positionnels grâce à lopérateur *splat*.

Le double-*splat* nous permet aussi ici de transformer un dictionnaire (ou autre *mapping*) en arguments nommés.

```python
>>> def addition_3(a, b, c):
...     return a + b + c
...
>>> addition_3(*[1, 2, 3])
6
>>> addition_3(1, *[2, 3])
6
>>> addition_3(**{'b': 2, 'a': 1, 'c': 3})
6
>>> addition_3(1, **{'b': 2, 'c': 3})
6
>>> addition_3(1, *[2], **{'c': 3})
6
>>> addition_3(*range(3)) # Splat est valable avec tous les itérables
3
```

Ainsi, il est possible de relayer les paramètres reçus par une fonction à une autre fonction, sans les préciser explicitement.

```python
>>> def proxy_addition_3(*args, **kwargs):
...     return addition_3(*args, **kwargs)
...
>>> proxy_addition_3(1, 2, 3)
6
>>> proxy_addition_3(1, c=3, b=2)
6
```

Avant Python 3.5, chaque opérateur *splat* ne pouvait être utilisé qu'une fois dans un appel, et `*` devait être placé après tous les arguments positionnels.

Ces règles ont depuis disparu, comme relaté dans [cet article sur la sortie de Python 3.5](https://zestedesavoir.com/articles/175/sortie-de-python-3-5/#2-principales-nouveautes).

```python
>>> addition_3(*[1, 2], 3)
6
>>> addition_3(*[1], 2, *[3])
6
>>> addition_3(*[1], **{'b': 2}, **{'c': 3})
6
```
