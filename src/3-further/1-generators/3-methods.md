### Méthodes des générateurs

Nous avons vus que les générateurs possédaient des méthodes `__next__` et `send`.
Nous allons maintenant nous intéresser aux deux autres méthodes de ces objets : `throw` et `close`.

#### `throw`

La méthode `throw` permet de lever une exception depuis le générateur, à l'endroit où ce dernier s'est arrêté.
Elle a pour effet de réveiller le générateur pour lui faire lever une exception du type indiqué.

Il s'agit alors d'une autre manière d'influer sur l'exécution d'un générateur, par des événements qui lui sont extérieurs.

`throw` possède 3 paramètres dont deux facultatifs :

* Le premier, `type`, est le type d'exception à lever ;
* Le second, `value`, est la valeur à passer en instanciant cette exception ;
* Et le troisième, `traceback`, permet de passer un pile d'appel (*traceback object*) particulière à l'exception.

L'exception survient donc au niveau du `yield`, et peut tout à fait être attrapée par le générateur.
Si c'est le cas, `throw` retournera la prochaine valeur produite par le générateur, ou lèvera une exception `StopIteration` indiquant que le générateur a été entièrement parcouru, à la manière de `next`.

```python
>>> def generator_function():
...     for i in range(5):
...         try:
...             yield i
...         except ValueError:
...             print('Something goes wrong')
...
>>> gen = generator_function()
>>> next(gen)
0
>>> next(gen)
1
>>> gen.throw(ValueError)
Something goes wrong
2
>>> next(gen)
3
>>> next(gen)
4
>>> gen.throw(ValueError)
Something goes wrong
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
StopIteration
```

Si l'exception n'est pas attrapée par le générateur, elle provoque alors sa fermeture, et remonte logiquement jusqu'à l'objet ayant fait appel à lui.

```python
>>> def generator_function():
...     for i in range(5):
...         yield i
...
>>> gen = generator_function()
>>> next(gen)
0
>>> next(gen)
1
>>> gen.throw(ValueError)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "<stdin>", line 3, in generator_function
ValueError
>>> next(gen)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
StopIteration      
```

#### `close`

Un cas particulier d'appel à la méthode `throw` est de demander au généraeur de s'arrêter en lui faisant lever une exception `GeneratorExit`.

À la réception de cette dernière, il est attendu que le générateur se termine (`StopIteration`) ou lève à son tour une `GeneratorExit` (par exemple en n'attrapant pas l'exception survenue).

La méthode `close` du générateur permet de réaliser cet appel et d'attraper les `StopIteration`/`GeneratorExit` en retour.

```python
>>> def generator_function():
...     for i in range(5):
...         yield i
...
>>> gen = generator_function()
>>> next(gen)
0
>>> next(gen)
1
>>> gen.close()
>>> next(gen)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
StopIteration
```

```python
>>> def generator_function():
...     for i in range(5):
...         try:
...             yield i
...         except GeneratorExit:
...             break
...
>>> gen = generator_function()
>>> next(gen)
0
>>> next(gen)
1
>>> gen.close()
>>> next(gen)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
StopIteration
```

Puisqu'elle attrape les `StopIteration`, il est possible d'appeler plusieurs fois la méthode `close` sur un même générateur.

```python
>>> gen.close()
>>> gen.close()
```

`close` s'occupe aussi de lever une `RuntimeError` dans le cas où le générateur ne s'arrêterait pas et continuerait à produire des valeurs.

```python
>>> def generator_function():
...     for i in range(5):
...         try:
...             yield i
...         except GeneratorExit:
...             print('Ignoring')
...
>>> gen = generator_function()
>>> next(gen)
0
>>> next(gen)
1
>>> gen.close()
Ignoring
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
RuntimeError: generator ignored GeneratorExit
>>> next(gen)
3
```
