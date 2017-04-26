### Mémoïsation

**Pré-requis : Signatures, Décorateurs**

Un des exemples les plus courants de mise en pratique des décorateurs est la réalisation d'un système de mise en cache (mémoïsation) : sauvegarder les résultats d'un calcul pour éviter de le refaire à chaque appel.

Nous allons débuter par une version simple : pour chaque appel, nous enregistrerons la valeur de retour associée au couple `(args, kwargs)` si celle-ci n'existe pas déjà. Dans le cas contraire, il nous suffira de retourner la valeur existante.

Seul bémol, nous ne pouvons pas stocker directement `(args, kwargs)` comme clef de notre dictionnaire, car certains objets n'y sont pas hashables (car modifiables, tel que le dictionnaire).
Nous procéderons donc à l'aide d'une sérialisation via `repr` pour obtenir la représentation de nos paramètres sous forme d'une chaîne de caractères.

```python
import functools

def memoize(f):
    cache = {}
    @functools.wraps(f)
    def decorated(*args, **kwargs):
        key = repr((args, kwargs))
        if key not in cache:
            cache[key] = f(*args, **kwargs)
        return cache[key]
    return decorated
```

Je vous conseille de le tester sur une fonction procédant à des affichages, pour bien constater la mise en cache.

```python
>>> @memoize
... def addition(a, b):
...     print('Computing addition of {} and {}'.format(a, b))
...     return a + b
...
>>> addition(3, 5)
Computing addition of 3 and 5
8
>>> addition(3, 5)
8
>>> addition(3, 6)
Computing addition of 3 and 6
9
```

Comme je le disais, c'est une version simple, dans le sens où s'il nous venait à l'esprit d'utiliser une fonction tantôt avec des arguments positionnels, tantôt avec des arguments nommés, nous ne bénéficierions pas des capacités du cache.

```python
>>> addition(3, b=5)
Computing addition of 3 and 5
8
>>> addition(a=3, b=5)
Computing addition of 3 and 5
8
```

#### Signatures

Afin d'avoir une représentation unique de nos arguments, nous allons alors utiliser les signatures de fonctions, et leur méthode `bind`.
Nous obtiendrons ainsi un couple unique `(args, kwargs)`, où tous les arguments nommés qui peuvent l'être seront transfomés en positionnels.

Il ne s'agit que de peu de modifications dans notre code.

```python
import functools
from inspect import signature

def memoize(f):
    cache = {}
    sig = signature(f)
    @functools.wraps(f)
    def decorated(*args, **kwargs):
        bind = sig.bind(*args, **kwargs)
        key = repr((bind.args, bind.kwargs))
        if not key in cache:
            cache[key] = f(*args, **kwargs)
        return cache[key]
    return decorated
```

À l'utilisation, nous obtenons donc :

```python
>>> @memoize
... def addition(a, b):
...     print('Computing addition of {} and {}'.format(a, b))
...     return a + b
...
>>> addition(3, 5)
Computing addition of 3 and 5
8
>>> addition(3, 5)
8
>>> addition(3, b=5)
8
>>> addition(b=5, a=3)
8
>>> addition(5, 3)
Computing addition of 5 and 3
8
```

Nous avons déjà parlé de [`functools`](https://docs.python.org/3/library/functools.html) à plusieurs reprises dans ce cours.
Si vous y avez prêté attention, vous avez remarqué que le décorateur que nous venons d'implémenter ressemble beaucoup à `lru_cache` (à l'exception près que notre version gère les types non-hashables, mais avec une perte de performances et une moins bonne fiabilité).
