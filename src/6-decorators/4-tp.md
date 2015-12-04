## TP : divers décorateurs

Dans ce TP, nous allons mettre en pratique les décorateurs à l'aide de quatre petits exercices qui vous permettront je l'espère de comprendre toutes les possibilités qu'ils offrent.

### Mémoïsation

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


### Fonctions génériques

Nous avons déjà parlé de [`functools`](https://docs.python.org/3/library/functools.html). à plusieurs reprises dans ce cours. Si vous y avez prêté attention, vous avez remarqué que le décorateur que nous venons d'implémenter ressemble beaucoup à `lru_cache` (à l'exception près que notre version gère les types non-hashables, mais avec une perte de performances).

Nous allons maintenant nous intéresser à `singledispatch`, une implémentation de fonctions génériques permettant de *dispatcher* l'appel en fonction du type du premier paramètre.

Un décorateur, `singledispatch` prend une fonction en paramètre (c'est la fonction qui sera appelée si aucune spécialisation n'est trouvée), et en retourne un nouvel objet.
Cet objet possède une méthode `register` qui s'utilisera comme un décorateur paramétré en lui précisant le type pour lequel nous voulons spécialiser.

Lors de chaque appel à l'objet, il sera déterminé suivant le type du premier paramètre la fonction à appeler. Nos appels devront donc posséder au minimum un argument positionnel.

Je vous propose pour cette fois de réaliser notre décorateur à l'aide d'une classe.

```python
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

Pour aller plus loin, nous pourrions aussi permettre de *dispatcher* en fonction du type de tous les paramètres, ou encore utiliser les annotations pour préciser les types.


### Vérification de types

L'intérêt de ce nouvel exercice va être de vérifier dynamiquement que les types des arguments passés à notre fonction sont les bons, à l'aide d'annotations sur les paramètres de la fonction.
La vérification ne pourra ainsi se faire que sur les paramètres possédant un nom.

Notre décorateur va donc se charger d'analyser les paramètres lors de chaque appel à la fonction, et de les comparer un à un avec les annotations de notre fonction.
Pour accéder aux annotations, nous allons à nouveau utiliser la fonction `signature`. La signature retournée comportant un attribut `parameters` contenant la liste des paramètres.

Ces paramètres peuvent-être de différents types, suivant leur emplacement dans la ligne de définition de la fonction.
Par exemple, si notre fonction se définit par :

```python
def f(a, b, c='', *args, d=(), e=[], **kwargs): pass
```

* `*args` est de type `VAR_POSITIONNAL`, il ne nous intéressera pas dans notre cas.
* `**kwargs` est de type `VAR_KEYWORD`, de même, il ne nous intéresse pas ici.
* `a`, `b` et `c` sont de type `POSITIONAL_OR_KEYWORD` (on peut les utiliser via des arguments positionnels ou via des arguments nommés).
* Enfin, `d` et `e` sont des `KEYWORD_ONLY` (on ne peut les utiliser que via des arguments nommés).
* Un dernier type existe, `POSITIONAL_ONLY`, mais il n'est pas représentable en Python, il peut cependant exister dans des builtins ou des extensions. Ce type ne nous intéressera pas non plus ici.

Ainsi, nous voudrons récupérer les annotations des paramètres `POSITIONAL_OR_KEYWORD` et `KEYWORD_ONLY`.
Reprenons notre fonction donnée plus haut et ajoutons lui des annotations pour certains paramètres :

```python
def f(a:int, b, c:str='', *args, d=(), e:list=[], **kwargs): pass
```

Analysons maintenant les paramètres tels que définis dans la signature de la fonction.

```python
>>> for p in signature(f).parameters.values():
...     print(p.name, p.kind, p.annotation)
a POSITIONAL_OR_KEYWORD <class 'int'>
b POSITIONAL_OR_KEYWORD <class 'inspect._empty'>
c POSITIONAL_OR_KEYWORD <class 'str'>
args VAR_POSITIONAL <class 'inspect._empty'>
d KEYWORD_ONLY <class 'inspect._empty'>
e KEYWORD_ONLY <class 'list'>
kwargs VAR_KEYWORD <class 'inspect._empty'>
```

Nous retrouvons donc les types énoncés plus haut, ainsi que nos annotations (ou `empty` quand aucune annotation n'est donnée).
Nous stockerons donc d'un côté les annotations des `POSITIONAL_OR_KEYWORD` dans une liste, et de l'autre celles des `KEYWORD_ONLY` dans un dictionnaire.
Par la suite, `bind` rangera pour nous les paramètres de ce premier type dans `args`, et ceux du second dans `kwargs`.

```python
from functools import wraps
from inspect import signature

def check_types(f):
    sig = signature(f)
    # Nous récupérons les types des paramètres positionnels
    #   (en remplaçant les annotations vides par None pour conserver l'ordre)
    args_types = [(p.annotation if p.annotation != sig.empty else None)
                  for p in sig.parameters.values()
                  if p.kind == p.POSITIONAL_OR_KEYWORD]
    # Puis ceux des paramètres nommés
    #   (il n'est pas nécessaire de conserver les empty ici)
    kwargs_types = {p.name: p.annotation for p in sig.parameters.values()
                    if p.kind == p.KEYWORD_ONLY and p.annotation != p.empty}
    @wraps(f)
    def decorated(*args, **kwargs):
        # On range correctement les paramètres des deux types
        bind = sig.bind(*args, **kwargs)
        # Vérification des paramètres positionnels
        for value, typ in zip(bind.args, args_types):
            if typ and not isinstance(value, typ):
                raise TypeError('{} must be of type {}'.format(value, typ))
        for name, value in bind.kwargs.items():
            # Si le type n'est pas précisé par l'annotation, on considère object
            #   (toutes les valeurs sont de type object)
            typ = kwargs_types.get(name, object)
            if not isinstance(value, typ):
                raise TypeError('{} must be of type {}'.format(value, typ))
        return f(*args, **kwargs)
    return decorated
```

Je vous invite maintenant à tester ce décorateur sur notre précédente fonction.


### Récursivité terminale

[La récursivité terminale n'existe pas en Python](http://neopythonic.blogspot.com.au/2009/04/tail-recursion-elimination.html). Guido von Rossum le dit lui-même. Mais il nous est possible de la simuler.

Si vous avez déjà tenté d'écrire des fonctions récursives en Python, vous vous êtes rapidement confronté à l'impossibilité de descendre au-delà d'un certain niveau de récursion, à cause de la taille limitée de la pile d'appels.
Certains langages implémentent l'optimisation dite de récursivité terminale : si l'appel récursif est la dernière instruction exécutée dans la fonction, il est possible de supprimer de la pile le contexte courant avant d'appeler la fonction suivante, et ainsi ne pas surcharger la pile. Ce n'est pas le cas avec Python.

Mais nous allons voir qu'avec le bon décorateur, il est possible de reproduire ce comportement.

En fait, nous allons nous contenter d'ajouter uné méthode `call` à nos fonctions. Lorsque nous ferons `function.call(...)`, nous n'appellerons pas réellement la fonction, mais enregistrerons l'appel. le *wrapper* de notre fonction sera ensuite chargé de réaliser en boucle tous ces appels.

Il faut bien noter que le retour de la méthode `call` ne sera pas utilisable comme le résultat réel de notre fonction, nous ne pourrons que le retourner pour qu'il soit ensuite évalué par le *wrapper*.

Pour cela, je m'appuie sur une classe `tail_rec_exec`, qui n'est autre qu'un *tuple* comportant la fonction à appeler et ses arguments (`args` et `kwargs`).

```python
class tail_rec_exec(tuple): pass
```

Maintenant nous allons réaliser notre décorateur `tail_rec`, j'ai opté pour une classe :

```python
class tail_rec:
    def __init__(self, func):
        self.func = func
        functools.update_wrapper(self, func)

    def call(self, *args, **kwargs):
        return tail_rec_exec((self.func, args, kwargs))

    def __call__(self, *args, **kwargs):
        r = self.func(*args, **kwargs)
        while isinstance(r, tail_rec_exec):
            func, args, kwargs = r
            r = func(*args, **kwargs)
        return r
```

Et à l'utilisation :

```python
@tail_rec
def my_sum(values, acc=0):
    if not values:
        return acc
    return my_sum.call(values[1:], acc + values[0])

@tail_rec
def factorial(n, acc=1):
    if not n:
        return acc
    return factorial.call(n - 1, acc * n)

@tail_rec
def even(n):
    if not n:
        return True
    return odd.call(n - 1)

@tail_rec
def odd(n):
    if not n:
        return False
    return even.call(n - 1)

print(my_sum(range(5000)))
print(factorial(5000))
print(factorial(5))
print(even(5000))
print(odd(5000))
print(even(5001))
print(odd(5001))
```

Nous verrons par la suite, dans le chapitre des métaclasses, comment éviter l'appel à une méthode `call` pour effectuer les appels récursifs.
