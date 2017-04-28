### Paramètres d'héritage

Quand nous créons une classe, nous savons que nous pouvons spécifier entre parenthèses les classes à hériter.

```python
class A(B, C): # A hérite de B et C
    pass
```

Les classes parentes sont ici comme les arguments positionnels d'un appel de fonction.
Vous vous en doutez peut-être maintenant, mais il est aussi possible de préciser des arguments nommés.

```python
class A(B, C, foo='bar', x=3):
    pass
```

Cette fonctionnalité existait déjà en Python 3.5, mais était assez étrange et se gérait au niveau de la métaclasse.
La comportement est simplifié avec [Python 3.6 qui ajoute une méthode spéciale pour gérer ces arguments](https://zestedesavoir.com/articles/1540/sortie-de-python-3-6/#principales-nouveautes).

Il est donc maintenant possible d'implémenter la méthode de classe `__init_subclass__`, qui recevra tous les arguments nommés.
La méthode ne sera pas appelée pour la classe courante, mais le sera pour toutes ses classes filles.

Pour reprendre notre class `Deque`, nous pourrions imaginer une classe `TypedDeque` qui gérerait des listes d'éléments d'un type prédéfini.
Nous lèverions alors une exception pour toute insertion de valeur d'un type inadéquat.

```python
class TypedDeque(Deque):
    elem_type = None

    def __init_subclass__(cls, type, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.elem_type = type

    @classmethod
    def check_type(cls, value):
        if cls.elem_type is not None and not isinstance(value, cls.elem_type):
            raise TypeError('Cannot insert element of type '
                            f'{type(value).__name__} in {cls.__name__}')

    def append(self, value):
        self.check_type(value)
        super().append(value)

    def insert(self, i, value):
        self.check_type(value)
        super().insert(i, value)

    def __setitem__(self, key, value):
        self.check_type(value)
        super().__setitem__(key, value)

class IntDeque(TypedDeque, type=int):
    pass

class StrDeque(TypedDeque, type=str):
    pass
```

```python
>>> d = IntDeque([0, 1, 2])
>>> d.append(3)
>>> list(d)
[0, 1, 2, 3]
>>> d.append('foo')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "init_subclass.py", line 91, in append
    self.check_type(value)
  File "init_subclass.py", line 87, in check_type
    raise TypeError('Cannot insert element of type '
TypeError: Cannot insert element of type str in IntDeque
>>>
>>> d = StrDeque()
>>> d.append('foo')
>>> list(d)
['foo']
>>> d.insert(0, 5)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "init_subclass.py", line 95, in insert
    self.check_type(value)
  File "init_subclass.py", line 87, in check_type
    raise TypeError('Cannot insert element of type '
TypeError: Cannot insert element of type int in StrDeque
```

Le paramètre `cls` de la méthode `__init_subclass__` correspond bien ici à la classe fille.
Il convient d'utiliser `super` pour faire appel aux `__init_subclass__` des autres parents, en leur donnant le reste des arguments nommés.
On note aussi qu'`__init_subclass__` étant oligatoirement une méthode de classe, l'utilisation du décorateur `@classmethod` est facultative.
