### TP : Liste immutable

Nous en étions resté sur notre liste chaînée à l'opérateur d'égalité, qui rendait la liste non-hashable.
Je vous disais alors que l'on s'intéresserait à un type de liste immutable (et donc hashable) : chose promise, chose due.

Nous savons que pour créer un type immutable en Python, il faut hériter d'un autre type immutable.
Par commodité, nous choisissons `tuple` puisqu'il nous permet en tant que conteneur de stocker des données.

Pour rappel, notre liste se compose de deux classes : `Node` et `Deque`.
Nos nouvelles classes se nommeront `ImmutableNode` et `ImmutableDeque`.

`ImmutableNode` est un ensemble de deux éléments : le contenu du maillon dans `value`, et le maillon suivant (ou `None`) dans `next`.
On peut aisément représenter cette classe par un *tuple* de deux éléments.
On ajoutera juste deux propriétés, `value` et `next`, pour faciliter l'accès à ces valeurs.

```python
class ImmutableNode(tuple):
    def __new__(cls, value, next=None):
        return super().__new__(cls, (value, next))

    @property
    def value(self):
        return self[0]

    @property
    def next(self):
        return self[1]
```

Passons maintenant à `ImmutableDeque`.
Au final, il s'agit aussi d'un ensemble de deux éléments : `first` et `last`, les deux extrêmités de la liste.

Mais `ImmutableDeque` présente un autre défi, c'est cette classe qui est chargée de créer les maillons, qui sont ici immutables.
Cela signifie que le `next` de chaque maillon doit être connu lors de sa création.

Pour rappel, la classe sera instanciée avec un itérable en paramètre, celui-ci servant à créer les maillons.
Il nous faudra donc itérer sur cet ensemble en connaissant l'élément suivant.

Je vous propose pour cela une méthode de classe récursive, `create_node`.
Cette méthode recevra un itérateur en paramètre, récupérera la valeur actuelle avec la fonction `next`, puis appelera la méthode sur le reste de l'itérateur.
`create_node` retournera un objet `ImmutableNode`, qui sera donc utilisé comme maillon `next` dans l'appel parent.
En cas de `StopIteration` (fin de l'itérateur), `create_node` renverra simplement `None`.

```python
class ImmutableDeque(tuple):
    def __new__(cls, iterable=()):
        first = cls.create_node(iter(iterable))
        last = first
        while last and last.next:
            last = last.next
        return super().__new__(cls, (first, last))

    @classmethod
    def create_node(cls, iterator):
        try:
            value = next(iterator)
        except StopIteration:
            return None
        next_node = cls.create_node(iterator)
        return ImmutableNode(value, next_node)
```

À la manière de notre classe `ImmutableNode`, nous ajoutons des propriétés `first` et `last`.
Celles-ci diffèrent un peu tout de même : puisque `__getitem__` sera surchargé dans la classe, nous devons faire appel au `__getitem__` parent, *via* `super`.

```python
@property
def first(self):
    return super().__getitem__(0)

@property
def last(self):
    return super().__getitem__(1)
```

Les autres méthodes (`__contains__`, `__len__`, `__getitem__`, `__iter__` et `__eq__`) seront identiques à celles de la classe `Deque`.
On prendra seulement soin, dans `__getitem__`, de remplacer les occurrence de `Deque` par `ImmutableDeque` en cas de *slicing*, ou de faire appel au type de `self` pour construire la nouvelle liste.

Les méthodes de modification (`append`, `insert`, `__setitem__`) ne sont bien sûr pas à implémenter.
On remarque d'ailleurs que l'attribut `last` de nos listes n'a pas vraiment d'intérêt ici, puisqu'il n'est pas utilisé pour faciliter l'ajout d'élements en fin de liste.

Enfin, on peut maintenant ajouter une méthode `__hash__`, pour rendre nos objets *hashables*.
Pour cela, nous ferons appel à la méthode `__hash__` du parent, qui retournera le condensat du *tuple*.

```python
def __hash__(self):
    return super().__hash__()
```

Nous pouvons maintenant passer au test de notre nouvelle classe.

```python
>>> d = ImmutableDeque(range(10))
>>> d
((0, (1, (2, (3, (4, (5, (6, (7, (8, (9, None)))))))))), (9, None))
>>> list(d)
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
>>> d[1:-1:2]
((1, (3, (5, (7, None)))), (7, None))
>>> list(d[1:-1:2])
[1, 3, 5, 7]
>>> 5 in d
True
>>> 11 in d
False
>>> len(d)
10
>>> d[0], d[1], d[5], d[9]
(0, 1, 5, 9)
>>> d == ImmutableDeque(range(10))
True
>>> d == ImmutableDeque(range(9))
False
>>> hash(d)
-9219024882206086640
>>> {d: 0}
{((0, (1, (2, (3, (4, (5, (6, (7, (8, (9, None)))))))))), (9, None)): 0}
>>> {d: 0}[d]
0
```
