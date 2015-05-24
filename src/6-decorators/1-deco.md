## D&CO, une semaine pour tout changer

- Principe, fonctionnement interne, équivalence (func = decorator(func))

En Python, vous en avez peut-être déjà croisés, les décorateurs reposent sur le caractère `@`.

Le principe de la décoration en Python est d'appliquer un décorateur à une fonction, afin de retourner un nouvel objet (généralement appelable).
Un décorateur est donc une fonction prenant une fonction en paramètre et retournant une fonction.

```python
def decorator(f): # decorator est un décorateur
    return f
```

Note: J'utilise ici le terme « fonction » mais cela est applicable à tout *callable*.

Pour appliquer un décorateur, on précède la ligne de définition de la fonction à décorer par une ligne comportant un `@` puis le nom du décorateur à appliquer, par exemple :

```python
@decorator
def addition(a, b):
    return a + b
```

Cela a pour effet de remplacer `addition` par le retour de la fonction `decorator` appelée avec `addition` en paramètre, c'est donc strictement équivalent à :

```python
def addition(a, b):
    return a + b

addition = decorator(addition)
```

On voit donc bien que le décorateur est appliqué à la création de la fonction, et non lors de ses appels.
Nous utilisons ici un décorateur très simple qui retourne la même fonction, mais il se pourrait très bien qu'il en retourne une autre, qui pourrait être créée à la volée.
Disons que nous aimerions modifier notre fonction `addition` pour afficher les opérandes puis le résultat, sans toucher au corps de notre fonction. Nous pouvons réalier un décorateur qui retournera une nouvelle fonction se chargeant d'afficher les paramètres, d'appeler notre fonction originale, puis d'afficher le retour et de le retourner (afin de conserver le comportement original).

Ainsi, notre décorateur devient

```python
def print_decorator(function):
    def new_function(a, b): # Nouvelle fonction se comportant comme la fonction à décorer
        print('Addition des nombres {} et {}'.format(a, b))
        ret = function(a, b) # Appel de la fonction originale
        print('Retour: {}'.format(ret))
        return ret
    return new_function # Ne pas oublier de retourner notre nouvelle fonction
```

Testons maintenant d'appliquer ce décorateur à une fonction d'addition :

```python
>>> @print_decorator
... def addition(a, b):
...     return a + b
...
>>> addition(1, 2)
Addition des nombres 1 et 2
Retour: 3
3
```

Mais notre décorateur est ici très sépcialisé, il ne fonctionne qu'avec les fonctions prenant deux paramètres, et affichera « Addition » dans tous les cas. Nous pouvons le modifier pour le rendre plus générique (souvenez vous d'`*args` et `**kwargs`).

```python
def print_decorator(function):
    def new_function(*args, **kwargs):
        print('Appel de la fonction {} avec args={} et kwargs={}'.format(
            function.__name__, args, kwargs))
        ret = function(*args, **kwargs)
        print('Retour: {}'.format(ret))
        return ret
    return new_function
```

Je vous laisse l'essayer sur des fonctions différentes pour vous rendre compte de sa généricité.

Les définitions de fonctions ne sont pas limitées à un seul décorateur : il est possible d'en spécifier autant que vous le souhaitez, en les plaçant les uns à la suite des autres.

```python
@decorator
@print_decoration
def useless():
    pass
```

L'ordre dans lequel ils sont spécifiés importe, le code précédent équivaut à :

```python
def useless():
    pass
useless = decorator(print_decorator(useless))
```

On voit donc que les décorateurs spécifiés en premiers sont ceux qui seront appliqués en derniers.

Enfin, pour rappel, l'application du décorateur n'est pas limité aux fonctions, mais s'étend aussi aux méthodes de classes ou aux classes elles-mêmes:

```python
@print_decorator
class MyClass:
    pass
```
