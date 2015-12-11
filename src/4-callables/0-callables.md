# Callables

Nous allons maintenant nous intéresser à un « nouveau » type d'objets : les *callables*. Je place des guillemets autour de nouveau car vous les fréquentez en réalité depuis que vous faites du Python, les fonctions sont des *callables*.

Qu'est-ce qu'un *callable* me demanderez-vous ? C'est un objet que l'on peut appeler. Appeler un objet consiste à utiliser l'opérateur `()`, en lui passant un certain nombre d'arguments, de façon à recevoir une valeur de retour.

```python
>>> print('Hello', 'world', end='!\n') # Appel d'une fonction avec différents paramètres
Hello world!
>>> x = pow(2, 3) # Valeur de retour
>>> x
8
```
