## Dessine-moi un générateur

Les générateurs sont donc des itérables, mais aussi des itérateurs, ce qui implique qu'ils se consomment quand on les parcourt (et donc nous ne pouvons les parcourir qu'une fois).

Ils sont généralement créés par des fonctions construites à l'aide du mot clef `yield`. Par abus de langage ces fonctions sont parfois appelées générateurs.

### Le mot-clef `yield`

Une générateur est donc créé à partir d'une fonction. Mais contrairement aux fonctions habituelles, celle-ci ne comprendra aucun `return`, mais un ou plusieurs `yield`.

Lors de l'appel, la fonction retournera un générateur, et à chaque appel à `next` sur le générateur, le code jusqu'au prochain `yield` sera exécuté. La valeur retournée par `next` sera la valeur apposée au `yield`. Un exemple pour mieux comprendre cela :

```python
>>> def function():
...     yield 4
...     yield 5
...     yield 6
...
>>> gen = function()
>>> next(gen)
4
>>> next(gen)
5
>>> next(gen)
6
>>> next(gen)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
StopIteration
>>> list(gen) # Tout le générateur a été parcouru
[]
```

Ou avec un `for` :

```python
>>> for i in function():
...     print(i)
...
4
5
6
```

Le générateur en lui-même ne retourne rien (il n'est pas *callable*), il produit des valeurs à l'aide de `yield`.
Pour bien faire la différence entre notre générateu et sa fonction génératrice, on peut regarder ce qu'en dit Python.

```python
>>> gen
<generator object function at 0x7f008dfb0570>
>>> function
<function function at 0x7f008dce2ea0>
```

Bien sûr, notre générateur est très simpliste dans l'exemple, mais toutes les structures de contrôle du Python peuvent y être utilisées. De plus, le générateur peut aussi être paramétré *via* les arguments passés à la fonction. Un exemple un peu plus poussé avec un générateur produisant les `n` premiers termes d'une suite de Fibonacci débutant par `a` et `b`.

```python
>>> def fibonacci(n, a=0, b=1):
...     for _ in range(n):
...         yield a
...         a, b = b, a + b
...
>>> list(fibonacci(10))
[0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
>>> list(fibonacci(5, 6, 7))
[6, 7, 13, 20, 33]
```
