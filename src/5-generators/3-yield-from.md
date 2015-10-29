## Déléguer à un autre générateur avec `yield from`

Il est aussi possible de déléguer l'itération à un sous-générateur, à l'aide du mot clef `yield from`.

```python
def gen1():
    yield 1
    yield 2
    yield 3

def gen2():
    yield 0
    yield from gen1()
    yield 4
```

Celui-ci agit comme si nous itérions sur `gen1()` depuis `gen2`, tout en *yieldant* toutes ses valeurs.

```python
def gen2():
    yield 0
    for value in gen1():
        yield value
    yield 4
```

À la différence près qu'avec `yield from`, les paramètres passés avec `send` sont aussi relégués aux sous-générateurs.

On peut aussi noter que `yield from` n'attend pas nécessairement un générateur, mais n'importe quel type d'itérable. `gen1` pourrait donc plus simplement s'écrire :

```python
def gen1():
    yield from [1, 2, 3]
```

Et par exemple, si nous voulions réécrire la fonction `itertools.chain`, nous pourrions procéder ainsi :

```python
def chain(*iterables):
    for iterable in iterables:
        yield from iterable
```
