### Inspecteur Gadget

Nous savons maintenant renseigner des informations complémentaires sur nos fonctions.
En plus des annotations vues précédemment, vous avez probablement déjà rencontré les *docstrings*.

Les *docstrings* sont des chaînes de caractères, à placer en tête d'une fonction, d'une classe ou d'un module.
Elles servent à décrire l'usage de ces objets, et sont accessibles dans l'aide fournie par `help`, au même titre que les annotations.

```python
def addition(a:int, b:int) -> int:
    "Return the sum of the two numbers `a` and `b`"
    return a + b
```

```python
>>> help(addition)
Help on function addition in module __main__:

addition(a:int, b:int) -> int
    Return the sum of the two numbers `a` and `b`
```

Elles deviennent aussi accessibles par l'attribut spécial `__doc__` de l'objet.

```python
>>> addition.__doc__
'Return the sum of the two numbers `a` and `b`'
```

#### Module `inspect`

[`inspect`](https://docs.python.org/3/library/inspect.html) est un module de la bibliothèque standard qui permet d'extraire des informations complémentaires sur les objets Python.
Il est notamment dédié aux modules, classes et fonctions.

Il comporte en effet des fonctions pour vérifier le type d'un objet : `ismodule`, `isclass`, 'isfunction`, etc.

```python
>>> import inspect
>>> inspect.ismodule(inspect)
True
>>> inspect.isclass(int)
True
>>> inspect.isfunction(addition)
True
>>> inspect.isbuiltin(len)
True
```

D'autres fonctions vont s'intéresser plus particulièrement aux documentations (`getdoc`) et à la gestion du code source (`getsource`, `getsourcefile`, etc.).

Imaginons un fichier `operations.py` contenant le code suivant :

```python
"Mathematical operations"

def addition(a:int, b:int) -> int:
    """
    Return the sum of the two numbers `a` and `b`

    ex: addition(3, 5) -> 8
    """
    return a + b
```

Depuis la fonction `addition` importée du module, nous pourrons grâce à `inspect` récupérer toutes les informations nécessaires au débogage.

```python
>>> import inspect
>>> from operations import addition
>>>
>>> inspect.getdoc(addition)
'Return the sum of the two numbers `a` and `b`\n\nex: addition(3, 5) -> 8'
>>> inspect.getsource(addition)
'def addition(a:int, b:int) -> int:\n    """\n    Return the sum of the two numbers `a` and `b`\n\n    ex: addition(3, 5) -> 8\n    """\n    return a + b\n'
>>> inspect.getsourcefile(addition)
'/home/entwanne/operations.py'
>>> inspect.getmodule(addition)
<module 'operations' from '/home/entwanne/operations.py'>
>>> inspect.getsourcelines(addition)
(['def addition(a:int, b:int) -> int:\n', '    """\n', '    Return the sum of the two numbers `a` and `b`\n', '\n', '    ex: addition(3, 5) -> 8\n', '    """\n', '    return a + b\n'], 3)
```

L'intérêt de `getdoc` par rapport à l'attribut `__doc__` étant que la documentation est nettoyée (suppression des espaces en début de ligne) par la fonction `cleandoc`.

```python
>>> addition.__doc__
'\n    Return the sum of the two numbers `a` and `b`\n\n    ex: addition(3, 5) -> 8\n    '
>>> inspect.cleandoc(addition.__doc__)
'Return the sum of the two numbers `a` and `b`\n\nex: addition(3, 5) -> 8'
```
