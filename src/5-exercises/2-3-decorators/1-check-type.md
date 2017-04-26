### Vérification de types

**Pré-requis : Annotations, Signatures, Décorateurs**

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
    # (en remplaçant les annotations vides par None pour conserver l'ordre)
    args_types = [(p.annotation if p.annotation != sig.empty else None)
                  for p in sig.parameters.values()
                  if p.kind == p.POSITIONAL_OR_KEYWORD]
    # Puis ceux des paramètres nommés
    # (il n'est pas nécessaire de conserver les empty ici)
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
            # (toutes les valeurs sont de type object)
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
