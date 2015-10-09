## Les propriétés

Les propriétés (ou *properties*) sont un moyen de simplifier l'écriture de descripteurs.

En effet, `property` est une classe qui, à la création d'un objet, prend en paramètre les fonctions `fget`, `fset` et `fdel` qui seront respectivement appelées par `__get__`, `__set__` et `__delete__`.

On pourrait ainsi définir une version simplifiée de `property` comme :

```python
class my_property:
    def __init__(self, fget, fset, fdel):
        self.fget = fget
        self.fset = fset
        self.fdel = fdel
    def __get__(self, instance, owner):
        return self.fget(instance)
    def __set__(self, instance, value):
        return self.fset(instance, value)
    def __delete__(self, instance):
        return self.fdel(instance)
```

Pour faire de `my_property` un clone parfait de `property`, il nous faudrait rendre les paramètres du constructeur optionnels, ou encore la gestion de `__get__` quand `instance` vaut `None`.
Ce qui permet à `property` d'être utilisé en tant que décorateur.

Logiquement, en rendant les paramètres `fset` et `fdel` optionnels, lorsque `my_property` serait appelée en tant que décorateur autour d'une fonction, cette fonction correspondrait à `fget`, et un objet `my_property` serait donc instancié puis retourné.

Ajoutons à cela les décorateurs `getter`, `setter` et `deleter` de l'objet `property` pour redéfinir les fonctions à appeler.

À l'utilisation, les propriétés nous offrent donc un moyen simple et élégant de réécrire notre classe `Temperature`.

```python
class Temperature:
    def __init__(self):
        self.value = 0

    @property
    def celsius(self):
        return self.value
    @celsius.setter
    def celsius(self, value): # le nom de cette méthode a peu d'importance
        self.value = value

    @property
    def fahrenheit(self):
        return self.value * 1.8 + 32
    @fahrenheit.setter
    def fahrenheit(self, value):
        self.value = (value - 32) / 1.8
```
