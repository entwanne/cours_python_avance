### `issubclass`

Dans la même veine qu'`isinstance`, nous avons donc l'opérateur `issubclass`, qui vérifie qu'une classe est sous-classe d'une autre.

La surcharge se fait là aussi sur la métaclasse, à l'aide de la méthode spéciale `__subclasscheck__`.
Cette méthode est très semblable à `__instancecheck__` : en plus de `self` (la classe courante), elle reçoit en paramètre la classe à tester.
Elle retourne elle aussi un booléen (`True` si la classe donnée est une sous-classe de l'actuelle, `False` sinon).

Reprenons ici l'exemple précédent des itérables : notre classe `ABCIterable` permet de tester si une classe est un type d'objets itérables.

```python
class ABCIterableMeta(type):
    def __subclasscheck__(self, cls):
        return hasattr(cls, '__iter__') and callable(cls.__iter__)

class ABCIterable(metaclass=ABCIterableMeta):
    pass
```

```python
>>> issubclass(list, ABCIterable)
True
>>> issubclass(tuple, ABCIterable)
True
>>> issubclass(str, ABCIterable)
True
>>> issubclass(dict, ABCIterable)
True
>>> issubclass(int, ABCIterable)
False
>>> issubclass(object, ABCIterable)
False
```

Cet exemple est d'ailleurs meilleur que le précédent, puisque comme Python il vérifie que la méthode `__iter__` est présente au niveau de la classe et pas au niveau de l'instance.

Comme `isinstance`, `issubclass` peut recevoir en deuxième paramètre un *tuple* de différentes classes à tester.

```python
>>> issubclass(int, (int, str))
True
>>> issubclass(str, (int, str))
True
>>> class Integer(int):
...     pass
...
>>> issubclass(Integer, (int, str))
True
>>> issubclass(list, (int, str))
False
```

En revanche, pas de raccourci pour éviter l'appel à `__subclasscheck__`, même quand on cherche à vérifier qu'une classe est sa propre sous-classe.

```python
>>> class NoSubclassesMeta(type):
...     def __subclasscheck__(self, cls):
...         return False
...
>>> class NoSubclasses(metaclass=NoSubclassesMeta):
...     pass
...
>>> issubclass(NoSubclasses, NoSubclasses)
False
```

#### Le cas des classes `ABC`

Pour les classes abstraites `ABC`, c'est à dire qui ont `abc.ABCMeta` comme métaclasse, une facilité est mise en place.
En effet, `ABCMeta` définit une méthode `__subclasscheck__`
(qui s'occupe entre autres de gérer les classes enregistrées *via* `register`).

Pour éviter de recourir à une nouvelle métaclasse et redéfinir `__subclasscheck__`,
la méthode d'`ABCMeta` relaie l'appel à la méthode de classe `__subclasshook__`, si elle existe.
Ainsi, une classe abstraite n'a qu'à définir `__subclasshook__` si elle veut étendre le comportement d'`issubclass`.

```python
>>> import abc
>>> class ABCIterable(abc.ABC):
...     @classmethod
...     def __subclasshook__(cls, subcls):
...         return hasattr(subcls, '__iter__') and callable(subcls.__iter__)
...
>>> issubclass(list, ABCIterable)
True
>>> issubclass(int, ABCIterable)
False
```

On notera que la méthode `__subclasshook__` sert aussi à l'opérateur `isinstance`.

```python
>>> isinstance([1, 2, 3], ABCIterable)
True
```

Contrairement à `__subclasscheck__`, `__subclasshook__` ne retourne pas forcément un booléen.
Elle peut en effet retourner `True`, `False`, ou `NotImplemented`.

Dans le cas où elle retourne un booléen, il sera la valeur de retour de `isinstance`/`issubclass`.
Mais dans le cas de `NotImplemented`, la main est rendue à la méthode `__subclasscheck__` d'`ABC`, qui s'occupe de vérifier si les classes sont parentes, ou si la classe est enregistrée (`register`).

Nous allons donc réécrire notre classe `ABCIterable` de façon à retourner `True` si la classe implémente `__iter__`, et `NotImplemented` sinon.
Ainsi, si la classe hérite d'`ABCIterable` mais n'implémente pas `__iter__`, elle sera tout de même considérée comme une sous-classe, ce qui n'est pas le cas actuellement.

```python
>>> class ABCIterable(abc.ABC):
...     @classmethod
...     def __subclasshook__(cls, subcls):
...         if hasattr(subcls, '__iter__') and callable(subcls.__iter__):
...             return True
...         return NotImplemented
...
>>> issubclass(list, ABCIterable)
True
>>> issubclass(int, ABCIterable)
False
>>> class X(ABCIterable): pass
...
>>> issubclass(X, ABCIterable)
True
```
