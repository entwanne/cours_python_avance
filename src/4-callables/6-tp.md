## TP: `itemgetter`

Dans ce nouveau TP, nous allons réaliser `itemgetter` à l'aide d'une classe formant des objets *callables*.

Commençons par `itemgetter`, la clef à récupérer est passée à l'instanciation de l'objet, et donc à son constructeur. L'objet depuis lequel nous voulons récupérer la clef est lui passé lors de l'appel (dans la méthode `__call__`, donc).
Il nous suffit, dans cette méthode, d'appeler l'opérateur `[]` sur l'objet avec la clef enregistrée au moment de la construction:

```python
class itemgetter:
    def __init__(self, key):
        self.key = key

    def __call__(self, obj):
        return obj[self.key]
```

C'est aussi simple que cela, et nous pouvons le tester:

```python
>>> points = [(0, 0), (1, 4), (3, 3), (4, 0)]
>>> sorted(points, key=itemgetter(0))
[(0, 0), (1, 4), (3, 3), (4, 0)]
>>> sorted(points, key=itemgetter(1))
[(0, 0), (4, 0), (3, 3), (1, 4)]
```

Nous aurions aussi pu profiter des fermetures (`closures`) de python pour réaliser `itemgetter` sous la forme d'une fonction retournant une fonction:

```python
def itemgetter(key):
    def function(obj):
        return obj[key]
    return function
```

Si vous vous êtes intéressés de plus près à `operator.itemgetter`, vous avez aussi pu remarquer que celle-ci pouvait prendre plus d'un paramètre:

```python
>>> from operator import itemgetter
>>> get_x = itemgetter('x')
>>> get_x_y = itemgetter('x', 'y')
>>> get_x({'x': 9, 'y': 6})
9
>>> get_x_y({'x': 9, 'y': 6})
(9, 6)
```

Je vous propose, pour aller un peu plus loin, d'ajouter cette fonctionnalité à notre classe, et donc d'utiliser les listes d'arguments positionnels. Vous trouverez la solution dans la documentation du module `operator`.
