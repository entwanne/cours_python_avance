## TP: propriétés et méthodes

Pour clore ce chapitre, je vous propose d'implémenter les descripteurs `staticmethod` et `classmethod`. J'ajouterais à cela un descripteur `method` qui reproduirait le comportement par défaut des méthodes en Python.

Pour résumer :

* `my_staticmethod`
    * Retourne la fonction cible, qu'elle soit utilisée depuis la classe ou depuis l'instance
* `my_classmethod`
    * Retourne une méthode préparée avec la classe en 1er paramètre
    * Même comportement que l'on utilise la méthode de classe depuis la classe ou l'instance
* `my_method`
   * Si utilisée depuis la classe, retourne la fonction
   * Sinon, retourne une méthode préparer avec l'instance en 1er paramètre

Notez que vous pouvez vous aider du type `MethodType` (`from types import MethodType`) pour créer vos *bound methods*.
Il s'utilise très facilement, prenant en paramètres la fonction cible et le 1er paramètre de cette fonction.

```python
class my_staticmethod:
    def __init__(self, func):
        self.func = func
    def __get__(self, instance, owner):
        return self.func
```

```python
from types import MethodType

class my_classmethod:
    def __init__(self, func):
        self.func = func
    def __get__(self, instance, owner):
        return MethodType(self.func, owner)
```

```python
from types import MethodType

class my_method:
    def __init__(self, func):
        self.func = func
    def __get__(self, instance, owner):
        if instance is None:
            return self.func
        return MethodType(self.func, owner)
```
