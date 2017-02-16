### Déléguer à un autre générateur avec `yield from`

Il est aussi possible de déléguer l'itération à un sous-générateur, à l'aide du mot clef `yield from`.

```python
def big_queue():
    yield 0
    yield from queue(1, 2, 3)
    yield 4
```

Celui-ci agit comme si nous itérions sur `queue(1, 2, 3)` depuis `big_queue`, tout en *yieldant* toutes ses valeurs.

```python
def big_queue():
    yield 0
    for value in queue(1, 2, 3):
        yield value
    yield 4
```

À la différence près qu'avec `yield from`, les paramètres passés lors d'un `send` sont aussi relégués aux sous-générateurs.

Dans notre première version, nous pouvons nous permettre ceci :

```python
>>> q = big_queue()
>>> next(q)
0
>>> next(q)
1
>>> q.send('foo')
>>> next(q)
2
>>> next(q)
3
>>> next(q)
'foo'
>>> next(q)
4
>>> next(q)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
StopIteration
```

Je vous laisse essayer avec la seconde implémentation de `big_queue` (sans `yield from`), pour bien observer l'effet de la délégation du `send`.

On peut aussi noter que `yield from` n'attend pas nécessairement un générateur, mais n'importe quel type d'itérable.

```python
def gen_iterables():
    yield from [1, 2, 3]
    yield from 'abcdef'
    yield from {'x': 1, 'y': -1}
```

Et par exemple, si nous voulions réécrire la fonction `itertools.chain`, nous pourrions procéder ainsi :

```python
def chain(*iterables):
    for iterable in iterables:
        yield from iterable
```
