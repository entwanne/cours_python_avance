## TP : divers décorateurs

Dans ce TP, nous allons mettre en pratique les décorateurs à l'aide de quelques petits exercices qui vous permettront je l'espère de comprendre toutes les possibilités qu'ils offrent.

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
        if key not in cache:
            cache[key] = f(*args, **kwargs)
        return cache[key]
    return decorated
```

Je vous conseille de le tester sur une fonction procédant à des affichages, pour bien constater la mise en cache.

Comme je le disais, c'est une version simple, dans le sens où s'il nous venait à l'esprit d'utiliser une fonction tantôt avec des arguments positionnels, tantôt avec des arguments nommés, nous ne bénéficierions pas des capacités du cache.

#### Signatures

Nous allons pour cela utiliser les signatures de fonctions. Ce sont des objets qui vont entre autres nous permettre, suivant la déclaration de la fonction, d'identifier quels arguments correspondent à quels paramètres ; et ainsi d'obtenir un couple unique `(args, kwargs)`, où tous les arguments nommés qui peuvent l'être seront transfomés en positionnels.

Leur utilisation est très simple, le module `inspect` contient une fonction `signature` qui retourne la signature du *callable* passé en paramètre. Cette signature possède ensuite une méthode `bind`, à laquelle nous donnerons nos arguments pour obtenir un objet de type `BoundArguments`, qui possède deux attributs `args` et `kwargs`.

Il ne s'agit alors que de peu de modifications dans notre code.

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
...     print('calcul')
...     return a + b
...
>>> addition(1, 2)
calcul
3
>>> addition(1, 2)
3
>>> addition(1, b=2)
3
>>> addition(b=2, a=1)
3
>>> addition(2, 1)
calcul
3
```

Nous avons déjà parlé de [`functools`](https://docs.python.org/3/library/functools.html). à plusieurs reprises dans ce cours. Si vous y avez prêté attention, vous avez remarqué que le décorateur que nous venons d'implémenter ressemble beaucoup à `lru_cache` (à l'exception près que notre version gère les types non-hashables, mais avec une perte de performances et une moins bonne fiabilité).


### Fonctions génériques

Nous allons ici nous intéresser à une autre fonction de ce module : `singledispatch`, une implémentation de fonctions génériques permettant de *dispatcher* l'appel en fonction du type du premier paramètre.

La généricité est un concept qui permet d'appeler une fonction avec des arguments de types variables.
C'est le cas par défaut en Python : les variables étant typées dynamiquement, il est possible de les appeler quels que soient les types des arguments envoyés.

Mais, de pair avec la généricité vient le concept de spécialisation, qui est plus subtil en Python.
Spécialiser une fonction générique, c'est fournir une implémentation différente de la fonction pour certains types de ses paramètres.

En Python, `singledispatch` permet de spécialiser une fonction selon le type de son premier paramètre.
Il est ainsi possible de définir plusieurs fois une même fonction, en spécifiant le type sur lequel on souhaite la spécialiser.

`singledispatch` est un décorateur, prenant donc une fonction en paramètre (la fonction qui sera appelée si aucune spécialisation n'est trouvée), et retournant un nouveau *callable*.
Ce *callable* possède une méthode `register`, qui s'utilisera comme un décorateur paramétré par le type pour lequel nous voulons spécialiser notre fonction.

Lors de chaque appel au *callable* retourné par `singledispatch`, la fonction à appeler sera déterminée selon le type du premier paramètre. Nos appels devront donc posséder au minimum un argument positionnel.

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


### Vérification de types

L'intérêt de ce nouvel exercice va être de vérifier dynamiquement que les types des arguments passés à notre fonction sont les bons, à l'aide d'annotations sur les paramètres de la fonction.
La vérification ne pourra ainsi se faire que sur les paramètres possédant un nom.

Notre décorateur va donc se charger d'analyser les paramètres lors de chaque appel à la fonction, et de les comparer un à un avec les annotations de notre fonction.
Pour accéder aux annotations, nous allons à nouveau utiliser la fonction `signature`. La signature retournée comportant un attribut `parameters` contenant la liste des paramètres.

Ces paramètres peuvent être de différentes natures, suivant leur emplacement dans la ligne de définition de la fonction.
Par exemple, si notre fonction se définit par :

```python
def f(a, b, c='', *args, d=(), e=[], **kwargs): pass
```

* `*args` est un `VAR_POSITIONNAL`, nous ne nous y intéresserons pas ici.
* `**kwargs` est un `VAR_KEYWORD`, de même, il ne nous intéresse pas dans notre cas.
* `a`, `b` et `c` sont des `POSITIONAL_OR_KEYWORD` (on peut les utiliser *via* des arguments positionnels ou *via* des arguments nommés).
* Enfin, `d` et `e` sont des `KEYWORD_ONLY` (on ne peut les utiliser que *via* des arguments nommés).
* Il existe aussi `POSITIONAL_ONLY`, mais celui-ci n'est pas représentable en Python ; il peut cependant exister dans des builtins ou des extensions. Ce type ne nous intéressera pas non plus ici.

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
	# Et des paramètres nommés
        for name, value in bind.kwargs.items():
            # Si le type n'est pas précisé par l'annotation, on considère object
            #   (toutes les valeurs sont de type object)
            typ = kwargs_types.get(name, object)
            if not isinstance(value, typ):
                raise TypeError('{} must be of type {}'.format(value, typ))
        return f(*args, **kwargs)
    return decorated
```

Voyons maintenant ce que donne notre décorateur à l'utilisation.

```python
>>> @check_types
... def addition(a:int, b:int):
...     return a + b
...
>>> @check_types
... def concat(a:str, b:str):
...     return a + b
...
>>> addition(1, 2)
3
>>> concat('x', 'y')
'xy'
>>> addition(1, 'y')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "<stdin>", line 19, in decorated
TypeError: y must be of type <class 'int'>
>>> concat(1, 'y')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "<stdin>", line 19, in decorated
TypeError: 1 must be of type <class 'str'>
```


### Récursivité terminale

La récursivité terminal est un concept issu du [paradigme fonctionnel](https://fr.wikipedia.org/wiki/Programmation_fonctionnelle).
Chaque fois que vous réalisez un appel de fonction, un contexte doit se mettre en place, afin de contenir les variables locales à la fonction (dont les paramètres), et qui doit être conservé jusqu'à la fin de l'exécution de la fonction.

Ces contextes sont stockés dans une zone mémoire appelée la pile, de taille limitée. Lors d'appels récursifs, les fonctions parentes restent présentes dans la pile, car n'ont pas terminé leur exécution. Donc plus on s'enfonce dans les niveaux de récursivité, plus la pile se remplit, jusqu'à parfois être pleine. Lorsque celle-ci est pleine, il n'est alors plus possible d'appeler de nouvelles fonctions, cela est représenté par l'exception `RecursionError` en Python.

Si vous avez déjà tenté d'écrire des fonctions récursives en Python, vous vous êtes rapidement confronté à l'impossibilité de descendre au-delà d'un certain niveau de récursion, à cause de la taille limitée de la pile d'appels.

```python
>>> def f():
...     return f()
...
>>> f()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "<stdin>", line 2, in f
  [...]
  File "<stdin>", line 2, in f
RecursionError: maximum recursion depth exceeded
```

Certains langages, notamment les langages fonctionnels, ont réussi à résoudre ce problème, à l'aide de la récursivité terminale. Il s'agit en fait d'identifier les appels terminaux dans la fonction (c'est à dire quand aucune autre opération n'est effectuée après l'appel récursif).
Si l'appel est terminal, cela signifie que l'on ne fera plus rien d'autre dans la fonction, et il est alors possible de supprimer son contexte de la pile, et ainsi d'économiser de l'espace à chaque appel récursif.

Prenons ces deux exemples :

```python
>>> def factorial1(n):
...     if not n:
...         return n
...     return n * factorial1(n - 1)
...
>>> def factorial2(n, acc=1):
...     if not n:
...         return acc
...     return factorial1(n - 1, acc * n)
...
```

La première fonction ne peut pas être optimisée par récursivité terminale, en effet, une multiplication est encore effectuée entre l'appel récursif et le `return`. Dans la seconde fonction, le problème est résolu : la multiplication est effectuée avant l'appel puisque dans les arguments. Cette deuxième fonction peut donc être optimisée.

Cependant, [la récursivité terminale n'existe pas en Python](http://neopythonic.blogspot.com.au/2009/04/tail-recursion-elimination.html). Guido von Rossum le dit lui-même. Mais il nous est possible de la simuler.
Nous allons voir qu'avec le bon décorateur, il est possible de reproduire ce comportement.

En fait, nous allons nous contenter d'ajouter uné méthode `call` à nos fonctions.
Lorsque nous ferons `function.call(...)`, nous n'appellerons pas réellement la fonction, mais enregistrerons l'appel.
Le *wrapper* de notre fonction sera ensuite chargé d'exécuter en boucle tous ces appels.

Il faut bien noter que le retour de la méthode `call` ne sera pas le retour de notre fonction. Il s'agira d'un objet temporaire qui servira à réaliser plus tard le réel appel de fonction, dans le *wrapper*.

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

La méthode `__call__` sera celle utilisée lorsque nous appellerons notre fonction, et la méthode `call` utilisée pour temporiser appel.

À l'utilisation, cela donne :

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

Nous verrons par la suite, dans le chapitre des métaclasses, comment éviter l'appel à une méthode `call` pour effectuer les appels récursifs, et ainsi réaliser le tout de façon transparente.
