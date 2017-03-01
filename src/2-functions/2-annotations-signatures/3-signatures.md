### Signatures

Le module `inspect` ne nous a pas encore révélé toutes ses surprises.
Il contient aussi une méthode `signature`, retournant la signature d'une fonction.

La signature est l'ensemble des paramètres (avec leurs noms, positions, valeurs par défaut et annotations), ainsi que l'annotation de retour d'une fonction.
C'est à dire toutes les informations décrites à droite du nom de fonction lors d'une définition.

```python
>>> sig = inspect.signature(addition)
>>> print(sig)
(a:int, b:int) -> int
```

Les objets retournés par `signature` sont de type `Signature`.
Ces objets comportent notamment un dictionnaire ordonné des paramètres de la fonction (attribut `parameters`), et l'annotation de retour (`return_annotation`).

Les paramètres sont un encore un nouveau type d'objets, `Parameter`.
Les objets `Parameter` possèdent un nom (`name`), une valeur par défaut (`default`), une annotation (`annotation`), et un type de positionnement (`kind`).

```python
>>> sig.return_annotation
<class 'int'>
>>> for param in sig.parameters.values():
...     print(param.name, param.default, param.annotation, param.kind)
...
a <class 'inspect._empty'> <class 'int'> POSITIONAL_OR_KEYWORD
b <class 'inspect._empty'> <class 'int'> POSITIONAL_OR_KEYWORD
```

On retrouve bien les noms et annotations de nos paramètres.
`inspect._empty` indique que nos paramètres ne prennent pas de valeurs par défaut.

Le type de positionnement correspond à la différence entre arguments positionnels et arguments nommés, ils sont au nombre de 5 :

* `POSITIONAL_ONLY` -- Le paramètre ne peut recevoir qu'un argument positionnel ;
* `POSITIONAL_OR_KEYWORD` -- Le paramètre peut indifféremment recevoir un argument positionnel ou nommé ;
* `VAR_POSITIONAL` -- Correspond au paramètre spécial `*args` ;
* `KEYWORD_ONLY` -- Le paramètre ne peut recevoir qu'un argument nommé ;
* `VAR_KEYWORD` -- Correspond au paramètre spécial `**kwargs`.

Il n'existe aucune syntaxe en Python pour définir des paramètres *positional-only*, ils existent cependant dans certaines *builtins* (`range` par exemple).

Les *positonal-or-keyword* sont les plus courants. Ils sont en fait tous les paramètres définis à gauche d'`*args`.

Les *keyword-only* sont ceux définis à sa droite.

Pour prendre une signature de fonction plus complète :

```python
>>> def function(a, b:int, c=None, d:int=0, *args, g, h:int, i='foo', j:float=5.0, **kwargs):
...     pass
...
>>> for param in inspect.signature(function).parameters.values():
...     print(param.name, param.default, param.annotation, param.kind)
...
a <class 'inspect._empty'> <class 'inspect._empty'> POSITIONAL_OR_KEYWORD
b <class 'inspect._empty'> <class 'int'> POSITIONAL_OR_KEYWORD
c None <class 'inspect._empty'> POSITIONAL_OR_KEYWORD
d 0 <class 'int'> POSITIONAL_OR_KEYWORD
args <class 'inspect._empty'> <class 'inspect._empty'> VAR_POSITIONAL
g <class 'inspect._empty'> <class 'inspect._empty'> KEYWORD_ONLY
h <class 'inspect._empty'> <class 'int'> KEYWORD_ONLY
i foo <class 'inspect._empty'> KEYWORD_ONLY
j 5.0 <class 'float'> KEYWORD_ONLY
kwargs <class 'inspect._empty'> <class 'inspect._empty'> VAR_KEYWORD
```

Notons aussi qu'il est possible d'avoir des paramètres *keyword-only* sans pour autant définir `*args`.
Il faut pour cela avoir un simple `*` dans la liste des paramètres, juste à gauche des *keyword-only*.

```python
>>> def function(a, *, b, c):
...     pass
...
>>> for param in inspect.signature(function).parameters.values():
...     print(param.name, param.kind)
...
a POSITIONAL_OR_KEYWORD
b KEYWORD_ONLY
c KEYWORD_ONLY
```

#### Arguments préparés

Nous venons de voir quelles informations nous pouvions tirer des signatures.
Mais celles-ci ne servent pas qu'à la documentation.

Les objets `Signature` sont aussi pourvus d'une méthode `bind`.
Cette méthode reçoit les mêmes arguments que la fonction cible et retourne un objet de type `BoundArguments`, qui fait la correspondance entre les paramètres et les arguments, après vérification que ces derniers respectent la signature.

L'objet `BoundArguments`, avec ses attributs `args` et `kwargs`, pourra ensuite être utilisé pour appeler la fonction cible.

```python
>>> sig = inspect.signature(addition)
>>> bound = sig.bind(3, b=5)
>>> bound.args
(3, 5)
>>> bound.kwargs
{}
>>> addition(*bound.args, **bound.kwargs)
8
```

Comme on peut le voir, cela permet de résoudre les paramètres pour n'avoir dans `kwargs` que les *keyword-only*, et les autres (ceux qui peuvent être positionnels) dans `args`.
Cet objet `BoundArguments` sera donc identique quelle que soit la manière dont seront passés les arguments.

```python
>>> sig.bind(3, 5) == sig.bind(b=5, a=3)
True
```

Nous pouvons ainsi avoir une représentation unique des arguments de l'appel, pouvant servir pour une mise en cache des résultats par exemple.

```python
cache_addition = {}
sig_addition = inspect.signature(addition)

def addition_with_cache(*args, **kwargs):
    bound = sig_addition.bind(*args, **kwargs)
    # addition ne reçoit aucun paramètre keyword-only
    # nous pouvons donc nous contenter de bound.args
    if bound.args in cache_addition:
        print('Retrieving from cache')
        return cache_addition[bound.args]
    print('Computing result')
    result = cache_addition[bound.args] = addition(*bound.args)
    return result
```

```python
>>> addition_with_cache(3, 5)
Computing result
8
>>> addition_with_cache(3, b=5)
Retrieving from cache
8
>>> addition_with_cache(b=5, a=3)
Retrieving from cache
8
>>> addition_with_cache(5, 3) # Le résultat de (a=5, b=3) n'est pas en cache
Computing result
8
```

Depuis Python 3.5, une autre fonctionnalité des `BoundArguments` est de pouvoir appliquer les valeurs par défaut aux paramètres.
Ils ont pour cela une méthode `apply_defaults`.

```python
>>> def addition_with_default(a, b=3):
...     return a + b
...
>>> sig = inspect.signature(addition_with_default)
>>> bound = sig.bind(5)
>>> bound.args
(5,)
>>> bound.apply_defaults()
>>> bound.args
(5, 3)
```

#### Méthode `replace`

Je voudrais enfin vous parler des méthodes `replace` des objets `Signature` et `Parameter`.
Ces méthodes permettent de retourner une copie de l'objet en en modifiant un ou plusieurs attributs.

Nous pourrons sur un paramètre modifier les valeurs `name`, `kind`, `default` et `annotation`.

```python
>>> param = sig.parameters['b']
>>> print(param)
b=3
>>> new_param = param.replace(name='c', default=4, annotation=int)
>>> print(new_param)
c:int=4
>>> print(param)
b=3
```

La méthode `replace` des signatures est similaire, et permet de modifier `parameters` et `return_annotation`.

```python
>>> print(sig)
(a, b=3)
>>> new_params = [sig.parameters['a'], new_param]
>>> new_sig = sig.replace(parameters=new_params)
>>> print(new_sig)
(a, c:int=4)
```
