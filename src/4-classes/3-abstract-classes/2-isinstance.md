### `isinstance`

Nous venons de voir que `isinstance` était un opérateur, et qu'il était surcheargable.
Nous allons ici nous intéresser à la mise en œuvre de cette surcharge.

Pour rappel, la surchage d'opérateur se fait par la définition d'une méthode spéciale dans le type de l'objet.
Par exemple, il est possible d'utiliser `+` sur le nombre `4` parce que `4` est de type `int`, et qu'`int` implémente la méthode `__add__`.

`isinstance` est un opérateur qui s'applique à une classe (la classe dont on cherche à savoir si tel objet en est l'instance).
La surcharge se fera donc dans le type de cette classe, c'est à dire dans la métaclasse.

La méthode spéciale correspondant à l'opérateur est `__instancecheck__`, qui reçoit en paramètre l'objet à tester, et retourne un booléen (`True` si l'objet est du type en question, `False` sinon).

On peut par exemple imaginer une classe `ABCIterable`, qui cherchera à savoir si un objet donné est itérable (possède une méthode `__iter__`).
On teste pour cela si cet object a un attribut `__iter__`, et si cet attribut est *callable*.

```python
class ABCIterableMeta(type):
    def __instancecheck__(self, obj):
        return hasattr(obj, '__iter__') and callable(obj.__iter__)

class ABCIterable(metaclass=ABCIterableMeta):
    pass
```

```python
>>> isinstance([], ABCIterable)
True
>>> isinstance((0,), ABCIterable)
True
>>> isinstance('foo', ABCIterable)
True
>>> isinstance({'a': 'b'}, ABCIterable)
True
>>> isinstance(18, ABCIterable)
False
>>> isinstance(object(), ABCIterable)
False
```

Quelques dernières précisions sur `isinstance` : l'opérateur est un peu plus complexe que ce qui a été montré.

Premièrement, `isinstance` peut recevoir en deuxième paramètre un *tuple* de types plutôt qu'un type simple.
Il regardera alors si l'object donné en premier paramètre est une instance de l'un de ces types.

```python
>>> isinstance(4, (int, str))
True
>>> isinstance('foo', (int, str))
True
>>> isinstance(['bar'], (int, str))
False
```

Ensuite, la méthode `__instancecheck__` n'est pas toujours appelée.
Lors d'un appel `isinstance(obj, cls)`, la méthode `__instancecheck__` est appelée que si `type(obj)` n'est pas `cls`.

On peut s'en rendre compte avec une classe dont `__instancecheck__` renverrait `False` pour tout objet testé.

```python
>>> class NoInstancesMeta(type):
...     def __instancecheck__(self, obj):
...         return False
...
>>> class NoInstances(metaclass=NoInstancesMeta):
...     pass
...
>>> isinstance(NoInstances(), NoInstances)
True
```

En revanche, si nous héritons de notre classe `NoInstances` :

```python
>>> class A(NoInstances):
...     pass
...
>>> isinstance(A(), NoInstances)
False
```

Pour comprendre le fonction d'`isinstance`, on pourrait grossièrement réécrire l'opérateur avec la fonction suivante.[^PyObject_IsInstance]

```python
def isinstance(obj, cls):
    if type(obj) is cls:
        return True
    if issubclass(type(cls), tuple):
        return any(isinstance(obj, c) for c in cls)
    return type(cls).__instancecheck__(cls, obj)
```

[^PyObject_IsInstance]: Voir à ce propos la fonction `PyObject_IsInstance` du fichier [`Objects/abstract.c`](https://github.com/python/cpython/blob/master/Objects/abstract.c) des sources de CPython.
