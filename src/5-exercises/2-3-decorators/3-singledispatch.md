### Fonctions génériques

**Pré-requis : Callables, Décorateurs**

Nous allons ici nous intéresser à `singledispatch`, une fonction du module `functools`.
Il s'agit d'une implémentation de fonctions génériques en Python, permettant de *dispatcher* l'appel en fonction du type du premier paramètre.

La généricité est un concept qui permet d'appeler une fonction avec des arguments de types variables.
C'est le cas par défaut en Python : les variables étant typées dynamiquement, il est possible d'appeler les fonctions quels que soient les types des arguments envoyés.

Mais, de pair avec la généricité vient le concept de spécialisation, qui est plus subtil en Python.
Spécialiser une fonction générique, c'est fournir une implémentation différente de la fonction pour certains types de ses paramètres.

En Python, `singledispatch` permet de spécialiser une fonction selon le type de son premier paramètre.
Il est ainsi possible de définir plusieurs fois une même fonction, en spécifiant le type sur lequel on souhaite la spécialiser.

`singledispatch` est un décorateur, prenant donc une fonction en paramètre (la fonction qui sera appelée si aucune spécialisation n'est trouvée), et retournant un nouveau *callable*.
Ce *callable* possède une méthode `register`, qui s'utilisera comme un décorateur paramétré par le type pour lequel nous voulons spécialiser notre fonction.

Lors de chaque appel au *callable* retourné par `singledispatch`, la fonction à appeler sera déterminée selon le type du premier paramètre.
Nos appels devront donc posséder au minimum un argument positionnel.

```python
>>> @singledispatch
... def print_type(arg):
...     print('Je ne connais pas le type de ce paramètre')
...
>>> @print_type.register(int)
... def _(arg): # Le nom doit être différent de print_type
...     print(arg, 'est un entier')
...
>>> @print_type.register(str)
... def _(arg):
...     print(arg, 'est une chaîne')
...
>>> print_type(15)
15 est un entier
>>> print_type('foo')
foo est une chaîne
>>> print_type([])
Je ne connais pas le type de ce paramètre
```

Pour notre implémentation, je vous propose pour cette fois de réaliser le décorateur à l'aide d'une classe. Cela nous permettra d'avoir facilement un attribut `registry` à disposition.

```python
import functools

class singledispatch:
    def __init__(self, func):
        self.default = func
        self.registry = {}
        functools.update_wrapper(self, func)

    def __call__(self, *args, **kwargs):
        func = self.registry.get(type(args[0]), self.default)
        return func(*args, **kwargs)

    def register(self, type_):
        def decorator(func):
            self.registry[type_] = func
            return func
        return decorator
```

Il faut donc bien comprendre que c'est `__init__` qui sera appelée lors de la décoration de la première fonction, puisque cela revient à instancier un objet `singledispatch`.
Cet objet contient alors une méthode `register` pour enregistrer des spécialisations de la fonction.
Et enfin, il est appelable, *via* sa méthode `__call__`, qui déterminera laquelle des fonctions enregistrées appeler.

Pour aller plus loin, nous pourrions aussi permettre de *dispatcher* en fonction du type de tous les paramètres, ou encore utiliser les annotations pour préciser les types.
