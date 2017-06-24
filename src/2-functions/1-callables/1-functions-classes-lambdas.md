### Fonctions, classes et lambdas

L'ensemble des *callables* contient donc les fonctions, mais pas seulement. Les classes en sont, les méthodes, les lambdas, etc.
Sont callables tous les objets derrière lesquels on peut placer une paire de parenthèses, pour les appeler.

En Python, on peut vérifier qu'un objet est appelable à l'aide de la fonction `callable`.

```python
>>> callable(print)
True
>>> callable(lambda: None)
True
>>> callable(callable)
True
>>> callable('')
False
>>> callable(''.join)
True
>>> callable(str)
True
>>> class A: pass
...
>>> callable(A)
True
>>> callable(A())
False
```
