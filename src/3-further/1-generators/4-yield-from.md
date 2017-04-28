### Déléguer à un autre générateur avec `yield from`

Nous savons produire les valeurs d'un générateur à l'aide du mot clef `yield`.
Voyons maintenant quelque chose d'un peu plus complexe avec `yield from`.
Ce nouveau mot clef permet de déléguer l'itération à un sous-générateur pris en paramètre.
La rencontre du `yield from` provoque une interruption du générateur courant, le temps d'itérer et produire les valeurs du générateur délégué.

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
Tout comme sont relayés aux sous-générateurs les appels aux méthodes `throw` et `close`.

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

Où l'on voit bien que le `send` est pris en compte par la sous-queue, et la valeur ajoutée à la file.
Je vous invite à essayer avec la seconde implémentation de `big_queue` (celle sans `yield from`), pour bien observer l'effet de la délégation du `send`.

On peut aussi noter que `yield from` n'attend pas nécessairement un générateur en paramètre, mais n'importe quel type d'itérable.

```python
def gen_from_iterables():
    yield from [1, 2, 3]
    yield from 'abcdef'
    yield from {'x': 1, 'y': -1}
```

Et par exemple, si nous voulions réécrire la fonction `chain` du module `itertools`, nous pourrions procéder ainsi :

```python
def chain(*iterables):
    for iterable in iterables:
        yield from iterable
```
