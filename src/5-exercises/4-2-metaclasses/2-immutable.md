### Types immutables

**Pré-requis : Descripteurs, Métaclasses**

Je vous avais promis une autre approche pour créer des types immutables, la voici !
Pour rappel, notre première version créait des classes héritant de `tuple`/`namedtuple`.
Les attributs, ainsi stockés dans une structure immutable, n'étaient alors pas réassignables.
Mais nous étions gênés par la présence de trop nombreuses méthodes qui polluaient nos objets.

La seconde version que je vous propose ici est plus étonnante, car elle ne repose pas sur un type immutable, mais sur `super`.
Vous pourriez vous demander ce que `super` vient faire dans cette histoire.
Pour vous l'expliquer, intéressons-nous au fonctionnement des objets de ce type.

#### Objets `super`

Dans sa forme complète, un objet `super` s'initialise avec une classe et une instance (plus ou moins directe) de cette classe.

```python
>>> obj = super(tuple, (1, 2, 3))
```

L'objet ainsi créé se comportera comme une instance de la classe suivante dans le *MRO*.
Dans l'exemple précédent, `obj` se comportera comme une instance d'`object` (classe parente de `tuple`).

Les deux arguments fournis à `super` se retrouvent stockés dans l'objet.

```python
>>> obj.__thisclass__
<class 'tuple'>
>>> obj.__self__
(1, 2, 3)
```

On trouve aussi un 3ème attribut, `__self_class__`, le type de `__self__`.
Ce type pouvant être différent de `__thisclass__` si l'instance passée à `super` est l'instance d'une de ses classes filles.

```python
>>> class T(tuple): pass
...
>>> obj = super(tuple, T((0, 1, 2)))
>>> obj.__thisclass__
<class 'tuple'>
>>> obj.__self_class__
<class '__main__.T'>
```

L'intérêt est que ces 3 seuls attributs ne sont pas redéfinissables.

```python
>>> obj.__self__ = (2, 3, 4)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: readonly attribute
```

Aussi, les objets `super` disposent de peu d'attributs et méthodes, contrairement aux *tuples*.

```python
>>> dir(obj) # obj a peu d'attributs/méthodes
['__class__', '__delattr__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__',
'__get__', '__getattribute__', '__gt__', '__hash__', '__init__', '__le__', '__lt__',
'__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__self__',
'__self_class__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__thisclass__']
```

Sur ces 26 éléments, seuls 7 sont définis dans `super`, les autres appartiennent à `object`.

```python
>>> [meth for meth in dir(obj) if getattr(getattr(super, meth, None), '__objclass__', None) is super]
['__get__', '__getattribute__', '__init__', '__repr__', '__self__', '__self_class__', '__thisclass__']
```

Ainsi, notre nouvelle version de types immutables se basera sur `super`, en incluant un objet `tuple` qui stockera les données.

#### `ImmutableMeta`

Mais revenons-en à nos métaclasses.
Ne nous appuyant ici pas sur `namedtuple`, il va falloir gérer nous-même la liaison entre les noms d'attributs et les éléments du *tuple*.

Pour cela, depuis le champ `__fields__` définit dans la classe immutable, on générera des propriétés pour chaque nom de champ, en l'associant à un index du *tuple*.

On utilisera pour cela une méthode `field_property`, qui sera définie comme méthode statique dans la métaclasse, et recevra un unique paramètre : l'index dans le *tuple* du champ à indexer.

```python
@staticmethod
def field_property(i):
    def get_field(self):
        return self.__self__[i] # On accède au tuple pointé par __self__ et à l'élément d'index i
    return property(get_field) # On enveloppe la fonction get_field dans une property
```

Il nous faudra aussi gérer l'initialisateur de notre classe, associant les arguments positionnels et nommés aux champs de nos objets.

Vient alors la méthode `__new__` de la métaclasse, qui se déroulera en plusieurs temps :

* D'abord, récupérer le champ `__fields__` du `dict` de la classe, et instancier un `field_property` pour chaque, ajouté au `dict` ;
* Ensuite, générer une signature de la méthode `__init__`, utilisée pour vérifier que les arguments correspondent bien aux champs lors de la construction ;
* Enfin, définir dans le `dict` un attribut `__slots__` à `()` pour éviter de pouvoir ajouter d'autres attributs aux instances de nos classes ;

Notre classe `ImmutableMeta` complète est donc la suivante.

```python
class ImmutableMeta(type):
    def __new__(cls, name, bases, dict):
        fields = dict.pop('__fields__', ())
        # Création des properties associées aux champs
        dict.update({field: cls.field_property(i) for i, field in enumerate(fields)})
        # Création d'une signature artificielle composée des noms de champs
        dict['__signature__'] = inspect.Signature(
          inspect.Parameter(field, inspect.Parameter.POSITIONAL_OR_KEYWORD) for field in fields)
        dict['__slots__'] = ()
        c = super().__new__(cls, name, bases, dict)
        return c

    @staticmethod
    def field_property(i):
        def get_field(self):
            return self.__self__[i]
        return property(get_field)
```

Et pour l'utiliser, nous créons une classe `Immutable`, héritant de `super` et définissant une méthode `__init__` pour initialiser nos objets immutables.
Cette méthode devra vérifier les arguments conformément à la signature, puis créer un *tuple* des attributs, à passer à l'initialisateur parent (celui de `super`).

```python
class Immutable(super, metaclass=ImmutableMeta):
    def __init__(self, *args, **kwargs):
        t = self.__signature__.bind(*args, **kwargs).args
        # Rappel : l'intialisateur prend un type et une instance de ce type
        super().__init__(tuple, t)
```

Il nous suffit alors d'hériter d'`Immutable`, et de définir un champ `__fields__` pour avoir un nouveau type d'objets immutables.

```python
class Point(Immutable):
    __fields__ = ('x', 'y')

    def distance(self):
        return (self.x**2 + self.y**2)**0.5
```

```python
>>> p = Point(3, 4)
>>> p.x
3
>>> p.y
4
>>> p.distance()
5.0
>>> p.x = 0
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: can't set attribute
>>> p.z = 0
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: 'Point' object has no attribute 'z'
```

Grâce à `super`, nous n'avons plus ici accès à `[]` ou `__getitem__` sur nos objets.

```python
>>> p[0]
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: 'Point' object does not support indexing
>>> p.__getitem__(0)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: 'Point' object has no attribute '__getitem__'
```

#### Améliorations

Notre classe est terminée, mais nous pouvons encore lui apporter quelques améliorations.

Premièrement, redéfinir la méthode `__repr__` de la classe `Immutable`.
Elle pointe ici sur celle de `super`, qui ne correspond pas vraiment à notre objet.

On peut choisir de la faire pointer sur `object.__repr__` :

```python
>>> Immutable.__repr__ = object.__repr__
>>> Point(1, 2)
<__main__.Point object at 0x7f012d454448>
```

Ou encore donner un résultat similaire aux *named tuples*, en écrivant le nom de la classe suivi de ses attributs entre paramètres.

```python
def __repr__(self):
    return '{}{}'.format(type(self).__name__, repr(self.__self__))
```

```python
>>> Point(1, 2)
Point(1, 2)
>>> Point(x=1, y=2)
Point(1, 2)
```

Bonus Python 3.6 :

```python
def __repr__(self):
    return f'{type(self).__name__}{self.__self__!r}'
```

Deuxième amélioration, masquer les méthodes inutiles.
Pour cela, on on peut définir une méthode `__dir__` dans `Immutable`.
Cette méthode spéciale est celle appelée par la fonction `dir`.
Nous pouvons alors en filtrer les méthodes pour supprimer celles définies par `super` (comme nous l'avons fait plus tôt en regardant l'attribut `__objclass__` des méthodes).

```python
def __dir__(self):
    d = super().__dir__()
    d = [meth for meth in d if getattr(getattr(type(self), meth, None), '__objclass__', None) is not super]
    return d
```
