### Transformer un générateur en gestionnaire de contexte

**Pré-requis : Décorateurs, Générateurs, Gestionnaires de contexte**

Nous avons vu dans ce cours le module `contextlib` et son décorateur `contextmanager` qui permet de créer un gestionnaire de contexte à partir d'une fonction génératrice.
Vous l'aurez deviné, le but de cet exercice sera de recoder ce décorateur, ou au moins une version basique.

Le code du décorateur en lui-même sera assez court.
Celui-ci se chargera de *wrapper* la fonction, afin de retourner un gestionnaire de contexte plutôt qu'un générateur lors des appels à celle-ci.

```python
import functools

def contextmanager(gen_func):
    @functools.wraps(gen_func)
    def wrapper(*args, **kwargs):
        gen = gen_func(*args, **kwargs)
        return GeneratorContextManager(gen)
    return wrapper
```

Le type `GeneratorContextManager`, qu'il nous reste à définir, est un gestionnaire de contexte.
Il fera appel au générateur qui lui est passé en paramètre pour ses méthodes `__enter__` et `__exit__`.

Nous pouvons en imaginer une première version sous la forme suivante :

```python
class GeneratorContextManager:
    def __init__(self, generator):
        self.generator = generator

    def __enter__(self):
        return next(self.generator)

    def __exit__(self, exc_type, exc_value, traceback):
        next(self.generator)
```

Le code est ici plutôt simple : `__enter__` provoque une première itération du générateur, afin d'aller jusqu'au `yield`.
Et `__exit__` en provoque une seconde, pour exécuter la code qui suit ce `yield`.

Mais nous pouvons déjà constater un premier problème.

```python
>>> @contextmanager
... def context():
...     print('before')
...     yield 'foo'
...     print('after')
...
>>> with context() as val:
...     print('during', val)
...
before
during foo
after
Traceback (most recent call last):
  File "<stdin>", line 2, in <module>
  File "<stdin>", line 9, in __exit__
StopIteration
```

Tout se déroule bien… jusqu'à la fermeture.
En effet, `__exit__` fait un `next` sur le générateur, mais ce dernier ne contient qu'un `yield`, il est donc normal qu'il lève une exception `StopIteration`.
Il nous faudra alors l'attraper afin de la masquer.

Et d'ailleurs, nous voulons empêcher que le générateur produise plus d'une valeur.
Pour cela, nous lèverons notre propre exception si aucune `StopIteration` n'est attrapée.

Nous réécrivons alors comme suit notre méthode `__exit__`.

```python
def __exit__(self, exc_type, exc_value, traceback):
    try:
        next(self.generator)
    except StopIteration:
        return
    else:
        raise RuntimeError("generator didn't stop")
```

Et notre gestionnaire de contexte se comporte maintenant correctement avec l'exemple précédent.

```python
>>> with context() as val:
...     print('during', val)
...
before
during foo
after
```

Mais, de la même manière que nous nous assurons que notre générateur ne produise pas plus d'une valeur, il faudrait aussi vérifier qu'il en produit au moins une.

Nous allons donc ajouter un `try`/`except` à notre méthode `__enter__` et lever une `RuntimeError` en cas de `StopIteration` lors du `next`.

```python
def __enter__(self):
    try:
        return next(self.generator)
    except StopIteration:
        raise RuntimeError("generator didn't yield")
```

Notre gestionnaire est maintenant plus complet, mais il lui manque une fonctionnalité cruciale : il ne gère pas les exceptions levées dans le bloc `with`.

Avec `@contextmanager`, il est normalement possible d'écrire le gestionnaire suivant, qui attraperait toutes les `TypeError`.

```python
@contextmanager
def catch_typerror():
    try:
        yield
    except TypeError:
        pass
```

Avec notre décorateur, l'exception n'est jamais attrapée.

```python
>>> with catch_typerror():
...     print(1 + '2')
...
Traceback (most recent call last):
  File "<stdin>", line 2, in <module>
TypeError: unsupported operand type(s) for +: 'int' and 'str'
```

En effet, en cas d'exception attrapée, la méthode `__exit__` est censée retourner `True`.
Mais l'exception étant levée dans le contexte, et gérée par le gestionnaire, elle n'atteint jamais le générateur.

Comment alors savoir si l'exception aurait bien été attrapée par le générateur ?
Il suffit de la lui faire lever avec sa méthode `throw`, et de regarder si cette exception remonte jusqu'au gestionnaire de contexte.
On distingue alors 4 cas :

- Le générateur lève une `StopIteration`, et s'est donc terminé normalement, `__exit__` retourne `True` ;
- Le générateur lève l'exception qui lui a été fournie lors du `throw`, il ne l'a donc pas attrapée, `__exit__` retourne `False` ;
- Le générateur lève une autre exception, on la laisse remonter ;
- Le générateur ne lève aucune exception, il ne s'est donc pas terminé, on lève une `RuntimeError`.

Ces cas n'interviennent bien sûr que si une exception s'est produite dans le bloc `with`, et donc que le paramètre `exc_type` fourni à `__exit__` ne vaut pas `None`.
Dans le cas où il vaut `None`, nous gardons le comportement actuel de notre méthode.

Nous complétons donc le code de notre méthode `__exit__` pour ajouter cette gestion d'erreurs.

```python
def __exit__(self, exc_type, exc_value, traceback):
    if exc_type is None:
        try:
            next(self.generator)
        except StopIteration:
            return
        else:
            raise RuntimeError("generator didn't stop")
    try:
        self.generator.throw(exc_type, exc_value, traceback)
    except StopIteration:
        return True
    except exc_type:
        return False
    else:
        raise RuntimeError("generator didn't stop after throw")
```

À l'utilisation, on constate bien qu'il permet d'attraper certaines exceptions et d'en laisser remonter d'autres.

```python
>>> @contextmanager
... def catch_typeerror():
...     try:
...         yield
...     except TypeError:
...         pass
...
>>> with catch_typeerror():
...     print(1 + 'a')
...
>>> with catch_typeerror():
...     raise ValueError
...
Traceback (most recent call last):
  File "<stdin>", line 2, in <module>
ValueError
```

Nous approchons de la fin de nos déboires, mais il y a encore deux cas que nous ne gérons pas.

- Que faire si une `StopIteration` survient dans le bloc `with` ?
- Que faire si le générateur lève une `exc_type`, qui n'est pas la même exception que celle survenue dans le bloc `with` ?

Dans le premier cas, l'exception est automatiquement attrapée sans que nous ne l'ayons demandé.

```python
>>> with catch_typeerror():
...     raise StopIteration
...
```

En effet, dans le code d'`__exit__`, nous attrapons toutes les `StopIteration` sans vérifier où elles se sont produites.
Comment faire cela ? En plus du paramètre `exc_type`, la méthode reçoit aussi `exc_value` qui est l'instance de l'exception levée dans le `with`.

Nous pouvons alors vérifier que la `StopIteration` attrapée est la même instance que l'exception survenue dans le `with`.
Si tel est le cas, `__exit__` doit retourner `False` (pour laisser remonter l'exception).
Dans le cas contraire elle continuera de retourner `True`.

Quant au fait que le générateur puisse lever une `exc_type` différente de celle du bloc `with`, il s'agit en fait du même problème.

On peut l'illustrer avec l'exemple suivant.

```python
>>> @contextmanager
... def catch_typeerror():
...     try:
...         yield
...     except TypeError:
...         print('error n°' + 4)
...
>>> with catch_typeerror():
...     raise TypeError
...
Traceback (most recent call last):
  File "<stdin>", line 2, in <module>
TypeError
```

L'exception qui nous remonte est celle du bloc `with`, normalement attrapée par le générateur.
À l'inverse, l'exception qui survient dans le générateur (au niveau du `print`) est totalement ignorée.

Le problème est que `__exit__` retourne `False` dans tous les cas où une `exc_type` survient.
Elle devrait d'abord s'assurer qu'il s'agit de la même instance (en comparant l'exception avec `exc_value`).
Si les instances sont différentes, `__exit__` devrait relayer l'exception (avec `raise`) plutôt que de retourner `False`.

Nous ajoutons donc ces améliorations à `__exit__` pour obtenir notre code final.

```python
def __exit__(self, exc_type, exc_value, traceback):
    if exc_type is None:
        try:
            next(self.generator)
        except StopIteration:
            return
        else:
            raise RuntimeError("generator didn't stop")
    try:
        self.generator.throw(exc_type, exc_value, traceback)
    except StopIteration as e:
        return e is not exc_value
    except exc_type as e:
        if e is exc_value:
            return False
        raise
    else:
        raise RuntimeError("generator didn't stop after throw")
```

Code final ? Oui, dans le sens où nous en resterons là pour notre exercice.
Mais d'autres cas sont normalement gérés par `contextmanager`, notamment celui où `exc_value` vaudrait `None` ou le cas d'exceptions qui en auraient causé d'autres.
Pour une version vraiment complète, je vous invite à consulter [les sources de la classe `_GeneratorContextManager` du module `contextlib`](https://github.com/python/cpython/blob/33a5568f69301562d536852d12b9e03cd8dfc3a4/Lib/contextlib.py#L57).
