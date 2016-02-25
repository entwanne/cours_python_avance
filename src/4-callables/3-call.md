## Call-me maybe

Je vous le disais, plusieurs types d'objets peuvent être appelés. Que cache donc un *callable* ? Comme pour les itérables, c'est un objet qui possède une méthode spéciale, `__call__`, dont les paramètres seront les arguments passés lors de l'appel. La valeur renvoyée par `__call__` sera le retour de l'appel.

Ainsi, testons avec divers objets :

```python
>>> def func(arg): return arg
...
>>> func(1)
1
>>> func.__call__(1)
1
>>> (lambda x: x + 1)(1)
2
>>> (lambda x: x + 1).__call__(1)
2
```

Mais, vous devez vous dire, si on peut appeler `func.__call__`, c'est qu'il s'agit d'un *callable*, qui possède donc sa propre méthode `__call__` ? C'est le cas, et l'on peut continuer ainsi indéfiniment.

```python
>>> func.__call__.__call__(1)
1
>>> func.__call__.__call__.__call__.__call__.__call__.__call__(1)
1
```

Cela s'explique par le fait que `__call__` est une méthode, donc un *callable*.
En interne, Python est capable d'identifier qu'il s'agit d'une fonction et d'en exécuter le code, pour ne pas avoir à appeler indéfiniment des `__call__`.

Ensuite, implémentons `__call__` dans un objet de notre création :

```python
class MyCallable:
    def __init__(self, a):
        self.a = a

    def __call__(self, b):
        return self.a + b
```

Nous avons là une classe `MyCallable`, dont les instances sont des *callables*, réalisant la somme du paramètre reçu à la construction avec celui reçu lors de l'appel.

```python
>>> add_3 = MyCallable(3)
>>> add_3(5)
8
>>> add_3(10)
13
>>> add_100 = MyCallable(100)
>>> add_100(2)
102
>>> MyCallable(6)(3)
9
```

Il y a différents intérêts à créer un type *callable*. Le premier serait simplement de rendre compatible notre objet à l'interface utilisée par de nombreuses fonctions Python que nous verrons dans la section suivante.
Aussi, utiliser une classe pour cela est un moyen simple de sauvegarder un état, permettant d'avoir un comportement différent à chaque appel.

```python
>>> class Increment:
...     def __init__(self):
...         self.n = 0
...     def __call__(self):
...         self.n += 1
...         return self.n
...
>>> incr = Increment()
>>> incr()
1
>>> incr()
2
>>> Increment()() # Les deux objets sont bien indépendants
1
>>> incr()
3
```
