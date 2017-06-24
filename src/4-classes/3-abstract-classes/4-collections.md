### Collections abstraites

Nous connaissons le module [`collections`](https://docs.python.org/3/library/collections.html), spécialisé dans les conteneurs ;
et [`abc`](https://docs.python.org/3/library/abc.html), dédié aux classes abstraites.
Que donnerait le mélange des deux ? [`collections.abc`](https://docs.python.org/3/library/collections.abc.html) !

Ce module fournit des classes abstraites toutes prêtes pour reconnaître les différentes interfaces du langage (`Container`, `Sequence`, `Mapping`, `Iterable`, `Iterator`, `Hashable`, `Callable`, etc.).

Assez simples à appréhender, ces classes abstraites testent la présence de méthodes essentielles au respect de l'interface.

```python
>>> import collections.abc
>>> isinstance(10, collections.abc.Hashable)
True
>>> isinstance([10], collections.abc.Hashable)
False
>>> issubclass(list, collections.abc.Sequence)
True
>>> issubclass(dict, collections.abc.Sequence)
False
>>> issubclass(list, collections.abc.Mapping)
False
>>> issubclass(dict, collections.abc.Mapping)
True
```

Outre la vérification d'interfaces, certaines de ces classes servent aussi de *mixins*, en apportant des méthodes abstraites et des méthodes prêtes à l'emploi.

La classe `MutableMapping`, par exemple, a pour méthodes abstraites `__getitem__`, `__setitem__`, `__delitem__`, `__iter__` et `__len__`.
Mais la classe fournit en plus l'implémentation d'autres méthodes utiles aux *mappings* : `__contains__`, `keys`, `items`, `values`, `get`, `__eq__`, `__ne__`, `pop`, `popitem`, `clear`, `update`, et `setdefault`.

C'est-à-dire qu'il suffit de redéfinir les 5 méthodes abstraites pour avoir un type de dictionnaires parfaitement utilisable.

```python
class MyMapping(collections.abc.MutableMapping):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self._subdict = dict(*args, **kwargs)

    def __getitem__(self, key):
        return self._subdict[key]

    def __setitem__(self, key, value):
        self._subdict[key] = value

    def __delitem__(self, key):
        del self._subdict[key]

    def __iter__(self):
        return iter(self._subdict)

    def __len__(self):
        return len(self._subdict)
```

```python
>>> m = MyMapping()
>>> m['a'] = 0
>>> m['b'] = m['a'] + 1
>>> len(m)
2
>>> list(m.keys())
['b', 'a']
>>> list(m.values())
[1, 0]
>>> dict(m)
{'b': 1, 'a': 0}
>>> m.get('b')
1
>>> 'a' in m
True
>>> m.pop('a')
0
>>> 'a' in m
False
```

Dans un genre similaire, on notera aussi les classes du module `numbers` : `Number`, `Complex`, `Real`, `Rational`, `Integral`.
Ces classes abstraites, en plus de reconnaître l'ensemble des types numériques, permettent par héritage de créer nos propres types de nombres.
