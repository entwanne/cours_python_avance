### Récursivité terminale

**Pré-requis : Callables, Décorateurs**

La récursivité terminale est un concept issu du [paradigme fonctionnel](https://fr.wikipedia.org/wiki/Programmation_fonctionnelle), permettant d'optimiser les appels récursifs.

Chaque fois que vous réalisez un appel de fonction, un contexte doit se mettre en place afin de contenir les variables locales à la fonction (dont les paramètres).
Il doit être conservé jusqu'à la fin de l'exécution de la fonction.

Ces contextes sont stockés dans une zone mémoire appelée la pile, de taille limitée. Lors d'appels récursifs, les fonctions parentes restent présentes dans la pile, car n'ont pas terminé leur exécution.
Donc plus on s'enfonce dans les niveaux de récursivité, plus la pile se remplit, jusqu'à parfois être pleine.
Une fois pleine, il n'est alors plus possible d'appeler de nouvelles fonctions, cela est représenté par l'exception `RecursionError` en Python.

Si vous avez déjà tenté d'écrire des fonctions récursives en Python, vous vous êtes rapidement confronté à l'impossibilité de descendre au-delà d'un certain niveau de récursion, à cause de la taille limitée de la pile d'appels.

```python
>>> def factorial(n):
...     if not n:
...         return 1
...     return n * factorial(n - 1)
...
>>> factorial(5)
120
>>> factorial(1000)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "<stdin>", line 4, in factorial
  File "<stdin>", line 4, in factorial
  [...]
  File "<stdin>", line 4, in factorial
RecursionError: maximum recursion depth exceeded in comparison
```

Certains langages, notamment les langages fonctionnels, ont réussi à résoudre ce problème, à l'aide de la récursivité terminale. Il s'agit en fait d'identifier les appels terminaux dans la fonction (c'est à dire quand aucune autre opération n'est effectuée après l'appel récursif).
Si l'appel est terminal, cela signifie que l'on ne fera plus rien d'autre dans la fonction, et il est alors possible de supprimer son contexte de la pile, et ainsi économiser de l'espace à chaque appel récursif.

Prenons la fonction `factorial` codée plus haut : elle ne peut pas être optimisée par récursivité terminale.
En effet, une multiplication est encore effectuée entre l'appel récursif et le `return`.

Prenons maintenant cette seconde implémentation :

```python
def factorial(n, acc=1):
    if not n:
        return acc
    return factorial(n - 1, acc * n)
```

Le problème est ici résolu : la multiplication est effectuée avant l'appel puisque dans les arguments. Cette deuxième fonction peut donc être optimisée.

Cependant, [la récursivité terminale n'existe pas en Python](http://neopythonic.blogspot.com.au/2009/04/tail-recursion-elimination.html). Guido von Rossum le dit lui-même.
Mais il nous est possible de la simuler, en reproduisant le comportement voulu, avec un décorateur dédié.

En fait, nous allons nous contenter d'ajouter uné méthode `call` à nos fonctions.
Lorsque nous ferons `function.call(...)`, nous n'appellerons pas réellement la fonction, mais enregistrerons l'appel.
Le *wrapper* de notre fonction sera ensuite chargé d'exécuter en boucle tous ces appels enregistrés.

Il faut bien noter que le retour de la méthode `call` ne sera pas le retour de notre fonction. Il s'agira d'un objet temporaire qui servira à réaliser plus tard le réel appel de fonction, dans le *wrapper*.

Nous nous appuierons sur une classe `tail_rec_exec`, qui n'est autre qu'un *tuple* comportant la fonction à appeler et ses arguments (`args` et `kwargs`).

```python
class tail_rec_exec(tuple):
    pass
```

Maintenant nous allons réaliser notre décorateur `tail_rec`, j'ai opté pour une classe :

```python
import functools

class tail_rec:
    def __init__(self, func):
        self.func = func
        functools.update_wrapper(self, func)

    def call(self, *args, **kwargs):
        return tail_rec_exec((self.func, args, kwargs))

    def __call__(self, *args, **kwargs):
        r = self.func(*args, **kwargs)
        # Nous exécutons les appels "récursifs" tant que le retour est de type tail_rec_exec
        while isinstance(r, tail_rec_exec):
            func, args, kwargs = r
            r = func(*args, **kwargs)
        return r
```

La méthode `__call__` sera celle utilisée lorsque nous appellerons notre fonction, et la méthode `call` utilisée pour temporiser appel.

À l'utilisation, cela donne :

```python
@tail_rec
def my_sum(values, acc=0):
    if not values:
        return acc
    return my_sum.call(values[1:], acc + values[0])

@tail_rec
def factorial(n, acc=1):
    if not n:
        return acc
    return factorial.call(n - 1, acc * n)

@tail_rec
def even(n):
    if not n:
        return True
    return odd.call(n - 1)

@tail_rec
def odd(n):
    if not n:
        return False
    return even.call(n - 1)
```

```python
>>> my_sum(range(5000))
12497500
>>> factorial(5)
120
>>> factorial(1000)
4023872600770937735437024...
>>> even(5000)
True
>>> odd(5000)
False
>>> even(5001)
False
>>> odd(5001)
True
```
