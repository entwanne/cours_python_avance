### TP : Types immutables

Nous avons vu dans le chapitre précédent comment réaliser un type immutable.
Nous voulons maintenant aller plus loin, en mettant en place une métaclasse qui nous permettra facilement de créer de nouveaux types immutables.

Déjà, à quoi ressemblerait une classe d'objets immutables ?
Il s'agirait d'une classe dont les noms d'attributs seraient fixés à l'avance pour tous les objets.
Et les attributs en question ne seraient bien sûr pas modifiables sur les objets.
La classe pourrait bien sûr définir des méthodes, mais toutes ces méthodes auraient un accès en lecture seule sur les instances.

On aurait par exemple quelque chose comme :

```python
class Point(metaclass=ImmutableMeta):
    __fields__ = ('x', 'y')

    def distance(self):
        return (self.x**2 + self.y**2)**0.5
```

```python
>>> p = Point(x=3, y=4)
>>> p.x
3
>>> p.y
4
>>> p.distance()
5.0
>>> p.x = 0
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: can´t set attribute
>>> p.z = 0
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: 'Point' object has no attribute 'z'
```

#### Hériter de `tuple`

Plusieurs solutions s'offrent à nous pour mener ce travail.
Nous pouvons, comme précédemment, faire hériter tous nos immutables de `tuple`.
Il faudra alors faire pointer chacun des noms d'attributs sur les éléments du *tuple*, *via* des propriétés par exemple.
On peut simplifier cela avec `namedtuple`, qui réalise cette partie du travail.

Notre métaclasse se chargerait ainsi d'extraire les champs du type immutable, de créer un `namedtuple` correspondant, puis en faire hériter notre classe immutable.

```python
class ImmutableMeta(type):
    def __new__(cls, name, bases, dict):
        fields = dict.pop('__fields__', ())
        bases += (namedtuple(name, fields),)
        return super().__new__(cls, name, bases, dict)
```

Si l'on implémente une classe `Point` comme dans l'exemple plus haut, on remarque que la classe se comporte comme convenu jusqu'au `p.z = 0`.
En effet, il nous est ici possible d'ajouter de nouveaux attributs à nos objets, pourtant voulus immutables.

```python
>>> p = Point(x=3, y=4)
>>> p.z = 5
>>> p.z
5
```

#### Les slots à la rescousse

Comme nous l'avons vu avec les accesseurs, il est possible de définir un ensemble `__slots__` des attributs possibles des instances de cette classe.
Celui-ci a entre autres pour effet d'empêcher de définir d'autres attributs à nos objets.

C'est donc dans ce sens que nous allons maintenant l'utiliser.
Nos types immutables n'ont besoin d'aucun attribut : tout ce qu'ils stockent est contenu dans un *tuple*, et les accesseurs sont des propriétés.
Ainsi, notre métaclasse `ImmutableMeta` peut simplement définir un attribut `__slots__ = ()` à nos classes.

```python
class ImmutableMeta(type):
    def __new__(cls, name, bases, dict):
        fields = dict.pop('__fields__', ())
        bases += (namedtuple(name, fields),)
        dict['__slots__'] = ()
        return super().__new__(cls, name, bases, dict)
```

#### Le problème des méthodes de `tuple`

Nous avons maintenant entre les mains une classe de types immutables répondant aux critères décrits plus haut.
Mais si on y regarde de plus près, on remarque un léger problème :
nos classes possèdent des méthodes incongrues héritées de `tuple` et `namedtuple`.
On voit par exemple des méthodes `__getitem__`, `count` ou `index` qui ne nous sont d'aucune utilité et polluent les classes.
`__getitem__` est d'autant plus problématique qu'il s'agit d'un opérateur du langage, qui se retrouve automatiquement surchargé.

```python
>>> dir(Point)
['__add__', '__class__', '__contains__', '__delattr__', '__dict__', '__dir__',
'__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getitem__',
'__getnewargs__', '__getstate__', '__gt__', '__hash__', '__init__', '__iter__',
'__le__', '__len__', '__lt__', '__module__', '__mul__', '__ne__', '__new__',
'__reduce__', '__reduce_ex__', '__repr__', '__rmul__', '__setattr__',
'__sizeof__', '__slots__', '__str__', '__subclasshook__', '_asdict', '_fields',
'_make', '_replace', '_source', 'count', 'index', 'x', 'y']
```

Alors on peut dans un premier temps choisir d'hériter de `tuple` plutôt que d'un `namedtuple` pour faire un premier tri, mais ça ne règle pas le soucis.
Et il nous est impossible de supprimer ces méthodes, puisqu'elles ne sont pas définies dans nos classes mais dans une classe parente.

Il faut alors bidouiller, en remplaçant les méthodes par des attributs levant des `AttributeError` pour faire croire à leur absence, en redéfinissant `__dir__` pour les en faire disparaître, etc.
Mais nos objets continueront à être des *tuples* et ces méthodes resteront accessibles d'une manière ou d'une autre (en appelant directement `tuple.__getitem__`, par exemple).

Nous verrons dans les exercices complémentaires une autre piste pour créer nos propres types immutables.
