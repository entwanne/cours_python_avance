### TP : Évaluation paresseuse

Dans ce dernier TP, nous nous intéresserons à l'évaluation paresseuse (*lazy evaluation*), et nous reviendrons sur un exemple qu'on avait laissé de côté après le chapitre sur les décorateurs : l'implémentation d'une récursivité terminale en Python.

#### L'évaluation paresseuse, c'est quoi ?

Lorsque vous entrez une expression Python dans votre interpréteur et que celui-ci vous retourne une valeur, on dit que cette expression est évaluée. Évaluer une expression correspond donc à en calculer le résultat.

L'évaluation paresseuse se différencie de l'évaluation standard par rapport au moment où le calcul a lieu.
Lors d'une évaluation traditionnelle, le résultat est tout de suite retourné, et peut être manipulé.
Dans le cas d'une évaluation paresseuse, celui-ci n'est calculé que lorsqu'il est réellement nécessaire (quand on commence à manipuler l'objet), d'où le terme de paresseux.

En Python par exemple, nous avons étudié plus tôt le concept de générateurs, ils correspondent à de l'évaluation paresseuse : ils ne sont pas évalués avant que l'on ne commence à itérer dessus.

#### Objectif du TP

Ici, nous voulons réaliser un appel paresseux à une fonction. C'est à dire embarquer la fonction à appeler et ses paramètres, mais ne réaliser l'appel qu'au moment où nous avons besoin du résultat.

Par exemple :

```python
>>> def square(x): return x ** 2
>>> a = square(3)
>>> b = square(4)
>>> c = square(5)
>>> a + b == c
True
```

Nous n'avons réellement besoin des valeurs `a`, `b` et `c` qu'en ligne 5.

Si nous ne voulons pas calculer tout de suite le résultat, il faudra tout de même que notre fonction `square` retourne quelque chose.
Et dans notre exemple, l'objet retourné devra posséder les méthodes `__add__` et `__eq__`. Méthodes qui se chargeront d'effectuer le calcul du carré.

Ce ne sont ici que deux opérateurs, mais il en existe beaucoup d'autres, *dont l'énumération serait inutile et fastidieuse*, et il va nous falloir tous les gérer.

#### Opérateurs et méthodes spéciales

Le problème des opérateur en Python, c'est que les appels aux méthodes spéciales sont optimisés et ne passent pas par `__getattribute__`.

```python
>>> class A:
...     def __add__(self, rhs):
...         return 0
...     def __getattribute__(self, name):
...         print('getattribute')
...         return super().__getattribute__(name)
...
>>> A() + A()
0
>>> import operator
>>> operator.add(A(), A())
0
>>> A().__add__(A())
getattribute
0
```

Il va donc nous falloir intégrer toutes les méthodes spéciales à nos objets, et les métaclasses nous seront alors d'une grande aide pour toutes les générer.

Une liste de méthodes spéciales nous est fournie dans la documentation Python : <https://docs.python.org/3/reference/datamodel.html#specialnames>

* `__new__`, `__init__`, `__del__`
* `__repr__`, `__str__`, `__bytes__`, `__format__`
* `__lt__`, `__le__`, `__eq__`, `__ne__`, `__gt__`, `__ge__`
* `__hash__`, `__bool__`
* `__getattr__`, `__getattribute__`, `__setattr__`, `__delattr__`, `__dir__`
* `__get__`, `__set__`, `__delete__`
* `__instancecheck__`, `__subclasscheck__`
* `__call__`
* `__len__`, `__length_hint__`, `__getitem__`, `__missing__`, `__setitem__`, `__delitem__`, `__iter__`, `__reversed__`, `__contains__`
* `__add__`, `__sub__`, `__mul__`, `__matmul__`, `__truediv__`, `__floordiv__`, `__mod__`, `__divmod__`, `__pow__`, `__lshift__`, `__rshift__`, `__and__`, `__xor__`, `__or__`
* `__radd__`, `__rsub__`, `__rmul__`, `__rmatmul__`, `__rtruediv__`, `__rfloordiv__`, `__rmod__`, `__rdivmod__`, `__rpow__`, `__rlshift__`, `__rrshift__`, `__rand__`, `__rxor__`, `__ror__`
* `__iadd__`, `__isub__`, `__imul__`, `__imatmul__`, `__itruediv__`, `__ifloordiv__`, `__imod__`, `__ipow__`, `__ilshift__`, `__irshift__`, `__iand__`, `__ixor__`, `__ior__`
* `__neg__`, `__pos__`, `__abs__`, `__invert__`, `__complex__`, `__int__`, `__float__`, `__round__`, `__index__`
* `__enter__`, `__exit__`
* `__await__`, `__aiter__`, `__anext__`, `__aenter__`, `__aexit__`

Mais celle-ci n'est pas complète, `__next__` n'y figure par exemple pas.
Je n'ai pas trouvé de liste exhaustive, et c'est donc celle-ci que nous utiliserons.
Nous omettrons cependant la première ligne (constructeur, initialisateur et destructeur), car les objets que nous recevrons seront déjà construits.

Il nous faut aussi différencier les opérateurs des autres méthodes spéciales. Habituellement, si une méthode spéciale est implémentée pour un opérateur et que l'opération n'est pas réalisable, celle-ci est censée retourner `NotImplemented`.
Le module `operator` nous permettra facilement de savoir si la méthode spéciale est un opérateur, et donc d'agir en conséquence (en vérifiant que la méthode est présente dans `operator.__dict__` par exemple).

La solution que je propose est la suivante.

```python
import operator

class LazyMeta(type):
    # Référencement de toutes les méthodes spéciales, ou presque
    specials = [
        '__repr__', '__str__', '__bytes__', '__format__',
        '__lt__', '__le__', '__eq__', '__ne__', '__gt__', '__ge__',
        '__hash__', '__bool__',
        '__getattr__', '__getattribute__', '__setattr__', '__delattr__', '__dir__',
        '__get__', '__set__', '__delete__',
        '__instancecheck__', '__subclasscheck__',
        '__call__',
        '__len__', '__length_hint__', '__getitem__', '__missing__', '__setitem__', '__delitem__',
        '__iter__', '__reversed__', '__contains__',
        '__add__', '__sub__', '__mul__', '__matmul__', '__truediv__', '__floordiv__', '__mod__',
        '__divmod__', '__pow__', '__lshift__', '__rshift__', '__and__', '__xor__', '__or__',
        '__radd__', '__rsub__', '__rmul__', '__rmatmul__', '__rtruediv__', '__rfloordiv__', '__rmod__',
        '__rdivmod__', '__rpow__', '__rlshift__', '__rrshift__', '__rand__', '__rxor__', '__ror__',
        '__iadd__', '__isub__', '__imul__', '__imatmul__', '__itruediv__', '__ifloordiv__', '__imod__',
        '__ipow__', '__ilshift__', '__irshift__', '__iand__', '__ixor__', '__ior__',
        '__neg__', '__pos__', '__abs__', '__invert__', '__complex__', '__int__', '__float__',
        '__round__', '__index__',
        '__enter__', '__exit__',
        '__await__', '__aiter__', '__anext__', '__aenter__', '__aexit__',
        '__next__'
    ]

    def get_meth(methname):
        "Fonction utilisée pour créer une méthode dynamiquement"
        def meth(self, *args, **kwargs):
            # On tente d'accéder à l'objet évalué (value)
            try:
                value = object.__getattribute__(self, 'value')
            # S'il n'existe pas, il nous faut alors le calculer puis le stocker
            except AttributeError:
                value = object.__getattribute__(self, 'expr')()
                object.__setattr__(self, 'value', value)
            # Appel à l'opérateur si la méthode est un opérateur
            if methname in operator.__dict__:
                return getattr(operator, methname)(value, *args, **kwargs)
            # Sinon, appel à la méthode de l'objet
            return getattr(value, methname)(*args, **kwargs)
        return meth

    @classmethod
    def __prepare__(cls, name, bases):
        # On prépare la classe en lui ajoutant toutes les méthodes référencées
        methods = {}
        for methname in cls.specials:
            methods[methname] = cls.get_meth(methname)
        return methods

# Le type Lazy est celui que nous utiliserons pour l'évaluation paresseuse
class Lazy(metaclass=LazyMeta):
    def __init__(self, expr):
        # Il possède une expression (un callable qui retournera l'objet évalué)
        # Les autres méthodes de Lazy sont ajoutées par la métaclasse
        object.__setattr__(self, 'expr', expr)
```

Nous sommes obligés d'utiliser `object.__getattribute__` et `object.__setattr__` pour accéder aux attributs, afin de ne pas interférer avec les méthodes redéfinies dans la classe courante.

À l'utilisation, cela donne :

```python
>>> def _eval():
...     print('evaluated')
...     return 4
...
>>> l = Lazy(_eval)
>>> l + 5
evaluated
9
>>> l + 5
9
>>> l = Lazy(lambda: [])
>>> l
[]
>>> l.append(5)
>>> l
[5]
>>> type(l)
<class '__main__.Lazy'>
>>> class A:
...     pass
...
>>> l = Lazy(lambda: A())
>>> l
<__main__.A object at 0x7f7e3d7376a0>
>>> type(l)
<class '__main__.Lazy'>
>>> l.x = 0
>>> l.x
0
>>> l.y # AttributeError
>>> l + 1 # TypeError
>>> abs(l) # TypeError
```

Ainsi, pour en revenir à notre TP sur la récursivité terminale, il nous suffirait de faire retourner à notre fonction un objet de type `Lazy` pour ne plus avoir à différencier `call` et `__call__`.
Les appels ne seraient alors exécutés, itérativement, qu'à l'utilisation du retour (quand on chercherait à itérer dessus, à l'afficher, ou autre).
Il n'y aurait ainsi plus besoin de se soucier de savoir si nous sommes dans un appel récursif ou dans le premier appel.
