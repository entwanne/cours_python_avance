## TP: divers décorateurs

Dans ce TP, nous allons mettre en pratique les décorateurs à l'aide de quatre petits exercices qui vous permettront je l'espère de comprendre toutes les possibilités qu'ils offrent.

### Mémoïsation

Un des exemples les plus courants de mise en pratique des décorateurs est la réalisation d'un système de mise en cache (mémoïsation) : sauvegarder les résultats d'un calcul pour éviter de le refaire à chaque appel.

Nous allons débuter par une version simple : pour chaque appel, nous enregistrerons la valeur de retour asociée au couple `(args, kwargs)` si celle-ci n'existe pas déjà. Dans le cas contraire, il nous suffira de retourner la valeur existante.

Seul bémol, nous ne pouvons pas stocker directement `(args, kwargs)` comme clef de notre dictionnaire, car certains objets n'y sont pas hashables (car modifiables). Nous procéderons donc à l'aide d'une sérialisation via `pickle`.

```python
import functools
import pickle

def memoize(f):
    cache = {}
    @functools.wraps(f)
    def decorated(*args, **kwargs):
        key = pickle.dumps((args, kwargs))
        if not key in cache:
            cache[key] = f(*args, **kwargs)
        return cache[key]
    return decorated
```

Je vous conseille de le tester sur une fonction procédant à des affichages, pour bien constater la mise en cache.

Comme je le disais, c'est une version simple, dans le sens où s'il nous venait à l'esprit d'utiliser une fonction tantôt avec des arguments positionnels, tantôt avec des arguments nommés, nous ne bénéficierions pas des capacités du cache.

#### Signatures

Nous allons pour cela utiliser les signatures de fonctions. Il s'agit d'objets qui vont entre-autres nous permettre, suivant la déclaration des paramètres de la fonction, d'identifier quels arguments correspondent à quels paramètres, et ainsi d'obtenir un couple unique `(args, kwargs)`.

Leur utilisation est très simple, le module `inspect` contient une fonction `signature` qui retourne la signature du *callable* passé en paramètre. Cette signature possède ensuite une méthode `bind`, à laquelle nous donnerons nos arguments pour obtenir un objet de type `BoundArguments`, qui possède deux attributs `args` et `kwargs`.

Il ne s'agit alors que de peu de modifications dans notre code.

```python
from inspect import signature

def memoize(f):
    cache = {}
    sign = signature(f)
    @functools.wraps(f)
    def decorated(*args, **kwargs):
        bind = sign.bind(*args, **kwargs)
        key = pickle.dumps((bind.args, bind.kwargs))
        if not key in cache:
            cache[key] = f(*args, **kwargs)
        return cache[key]
    return decorated
```


### Fonctions génériques

Nous avons déjà parlé de [`functools`](https://docs.python.org/3/library/functools.html). à plusieurs reprises dans ce cours. Si vous y avez prêté attention, vous avez remarqué que le décorateur que nous venons d'implémenter ressemble beaucoup à `lru_cache` (à l'exception près que notre version gère les types non-hashables, mais avec une perte de performances).

Nous allons maintenant nous intéresser à `singledispatch`, une implémentation de fonctions génériques permettant de dispatcher l'appel en fonction du type du premier paramètre.

Un décorateur, `singledispatch` prend une fonction en paramètre (c'est la fonction qui sera appelée si aucune spécialisation n'est trouvée), et en retourne un nouvel objet. Cet objet possède une méthode `register` s'utilisera comme un décorateur paramétré en lui précisant le type pour lequel nous voulons spécialiser.

Lors de chaque appel à l'objet, il sera déterminé suivant le type du premier paramètre la fonction à appeler. Nos appels devront donc posséder au minimum un argument positionnel.

Je vous propose pour cette fois de réaliser notre décorateur à l'aide d'une classe.

```python
class singledispatch:
    def __init__(self, func):
        self.default = func
        self.registry = {}
    def __call__(self, *args, **kwargs):
        func = self.registry.get(type(args[0]), self.default)
        return func(*args, **kwargs)
    def register(self, type_):
        def decorator(func):
            self.registry[type_] = func
            return func
        return decorator
```

Pour aller plus loin, nous pourrions aussi permettre de dispatcher en fonction du type de tous les paramètres, ou encore utiliser les annotations pour préciser les types.


### Vérification de types


### Récursivité terminale
