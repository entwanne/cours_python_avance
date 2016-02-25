## Paramètres de fonctions

### Paramètres et arguments

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

### L'opérateur *splat*

#### Appels

L'opérateur *splat* est représenté par le caractère `*`. À ne pas confondre avec la multiplication, opérateur binaire entre deux objets, il s'agit ici d'un opérateur unaire : c'est à dire qu'il n'opère que sur un objet, en se plaçant devant.

Cet opérateur permet de récupérer la liste (ou plus précisément le `tuple`) des arguments positionnels passés lors d'un appel, on appelle cela le *packing*.

```python
>>> def func(*args): # Il est conventionnel d'appeler args la liste ainsi récupérée
...     print(args)
...
>>> func(1, 2, 3, 'a', 'b', None)
(1, 2, 3, 'a', 'b', None)
```

La présence d'`*args` n'est pas incompatible avec celle d'autres paramètres, s'ils sont placés avant.

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

`*args` peut néanmoins se placer n'importe où par rapport aux paramètres ayant une valeur par défaut (avant, après, au milieu).

```python
def func1(a, *args, b=1): pass
def func2(a, b=1, *args): pass
def func3(a, b=1, *args, c=2): pass
```

Enfin, il existe aussi l'opérateur double-*splat* (`**`), pour récupérer le dictionnaire des arguments nommés. Celui-ci doit se placer après tous les paramètres, et se nomme habituellement `kwargs`.

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

Une fonction peut donc récupérer tous ses arguments (positionnels et nommés) en combinant ces deux opérateurs.

```python
def func(*args, **kwargs):
    pass
```

Mais ces opérateurs servent aussi lors de l'appel à une fonction, via ce qu'on appelle l'*unpacking* : il est possible de transformer une liste en arguments positionnels, et un dictionnaire en arguments nommés (ou tout autres itérables compatibles). La seule règle est encore une fois de placer `*` après tous les arguments positionnels, et `**` après tous les nommés.

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
>>> addition_3(*range(3)) # Valable avec tous les itérables
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

#### Assignations

Je tenais enfin à vous présenter une dernière utilité de l'opérateur `*` : lors d'une assignation. Vous connaissez probablement déjà l'assignation multiple (`a, b, c = 0, 1, 2`), mais saviez vous que la partie droite pouvait être un itérable quelconque ?

```python
>>> a, b, c = range(3)
>>> a
0
>>> b
1
>>> c
2
```

Voyons maintenant ce que nous permet l'opérateur *splat* :

```python
>>> head, *tail = range(10)
>>> head
0
>>> tail
[1, 2, 3, 4, 5, 6, 7, 8, 9]
>>> first, second, *tail = range(10)
>>> second
1
>>> tail
[2, 3, 4, 5, 6, 7, 8, 9]
>>> first, *_, last = range(10)
>>> first
0
>>> last
9
```

Notons enfin que les possibilités offertes par l'opérateur *splat* ont encore été étendues avec Python 3.5, pour en savoir plus : <https://zestedesavoir.com/articles/175/sortie-de-python-3-5/#2-principales-nouveautes>
