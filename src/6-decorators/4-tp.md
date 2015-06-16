## TP: divers décorateurs

Dans ce TP, nous allons mettre en pratique les décorateurs à l'aide de trois petits exercices qui vous permettront je l'espère de comprendre toutes les possibilités qu'ils offrent.

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


### Templates


### Récursivité terminale
