## L'attribut de Dana

Que font réellement `getattr`, `setattr` et `delattr` ? Elles appellent des méthodes spéciales de l'objet.
`setattr` et `delattr` sont les cas les plus simples, la correspondance est faite avec les méthodes `__setattr__` et `__delattr__` de l'objet. Ces deux méthodes prennent respectivement les mêmes paramètres (en plus de `self`) que les fonctions auxquelles elles correspondent. `__setattr__` prendra donc le nom de l'attribut et sa nouvelle valeur, et `__delattr__` le nom de l'attribut.

Quant à `getattr`, la chose est un pleu complexe, car deux méthodes spéciales lui correspondent : `__getattribute__` et `__getattr__`. Ces deux méthodes prennent en paramètre le nom de l'attribut.
La première est appelée lors de la récupération de tout attribut. La seconde est réservée aux cas où l'attribut n'existe pas (si `__getattribute__` lève une `AttributeError` par exemple).
Par défaut, `__getattribute__` se charge de retourner les attributs contenus dans `__dict__`. Si vous voulez ajouter des attributs dynamiques, il vous faut donc plutôt passer par `__getattr__`.

Ainsi, pour définir dynamique un attribut, il nous suffit de coupler ces méthodes, tout en pensant à y utiliser `super` pour faire appel au comportement par défaut dan le cas où nous agissons sur un attribut « normal ».

```python
class Temperature:
    def __init__(self):
        self.value = 0

    def __getattr__(self, name):
        if name == 'celsius':
            return self.value
        if name == 'fahrenheit':
            return self.value * 1.8 + 32
        return super().__getattr__(name)

    def __setattr__(self, name, value):
        if name == 'celsius':
            self.value = value
        elif name == 'fahrenheit':
            self.value = (value - 32) / 1.8
	else:
            super().__setattr__(name, value)
```

### dict et slots

### MRO
