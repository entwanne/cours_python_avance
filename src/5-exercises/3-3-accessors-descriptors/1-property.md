### Propriétés

**Pré-requis : Décorateurs, Attributs, Descripteurs**

Durant le chapitre sur les descripteurs, nous avons utilisé `my_property`, une copie minimaliste de la classe `property`.
Je vous propose ici d'en terminer l'implémentation, afin de rendre ces deux classes similaires.

Pour rappel, `property` est une classe de descripteurs, utilisable en tant que décorateur sur les méthodes à transformer en propriétés.
Les propriétés étant des descripteurs faisant appel à des fonctions particulières pour l'accès en lecture/écriture ou la suppression de l'attribut.
En plus des méthodes `__get__`, `__set__` et `__delete__` des descripteurs, `property` possède aussi des méthodes/décorateurs `getter`, `setter` et `deleter` pour redéfinir ces fonctions.

Notre implémentation utilisée dans le chapitre sur les accesseurs était la suivante :

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

Nous implémentons bien les 3 méthodes propres aux descripteurs, mais il faut pour chaque propriété que ces 3 fonctions soient définies, et notre classe n'est pas utilisable comme décorateur.
Il manque aussi la redéfinition des fonctions.

Un autre point qui n'a pas été abordé est celui de la documentation.
En plus des `fget`, `fset` et `fdel`, la propriété peut-être initialisée avec un paramètre `doc`, qui sera la documentation de l'attribut.
En l'absence de `doc`, l'attribut prendra pour documentation celle de la fonction `fget`, si existante.

Ces 4 paramètres sont tous facultatifs, nous les initialiserons alors à `None`.
Nous pouvons alors écrire le nouvel initialisateur de notre classe `my_property`.

```python
    def __init__(self, fget=None, fset=None, fdel=None, doc=None):
        if doc is None and fget is not None:
            doc = getattr(fget, '__doc__', None)
        self.fget, self.fset, self.fdel = fget, fset, fdel
        self.__doc__ = doc
```

On récupère ainsi la documentation de `fget` si aucune documentation n'a été fournie à la construction (`doc is None`), et si `fget` est présente (`fget is not None`).
En utilisant `getattr`, on permet à `fget` de ne pas avoir de documentation, auquel cas `doc` vaudra toujours `None`.

Les méthodes `__get__`, `__set__` et `__delete__` seront un peu plus complexes que précédemment.
Il nous faudra maintenant tester la présence des fonctions cibles (`fget`, `fset` et `fdel`), et lever une exception `AttributeError` le cas échéant.
Cette exception indiquera que l'attribut n'est pas lisible, redéfinissable, ou supprimable.

Nous ferons aussi en sorte que `__get__` appelée sans instance (`instance` valant `None`) retourne la propriété elle-même.

```python
    def __get__(self, instance, owner):
        'Return an attribute of instance, which is of type owner.'
        if instance is None:
            return self
        if self.fget is None:
            raise AttributeError('unreadable attribute')
        return self.fget(instance)

    def __set__(self, instance, value):
        'Set an attribute of instance to value.'
        if self.fset is None:
            raise AttributeError("can't set attribute")
        return self.fset(instance, value)

    def __delete__(self, instance):
        'Delete an attribute of instance.'
        if self.fdel is None:
            raise AttributeError("can't delete attribute")
        return self.fdel(instance)
```

Enfin, les méthodes `getter`, `setter` et `deleter` copieront celles de `property`.
Plutôt que de modifier la proprité avec la fonction reçue en paramètre, elles retourneront une nouvelle propriété.
Aucun changement ne sera effectué si le paramètre vaut `None`.

```python
    def getter(self, fget):
        'Descriptor to change the getter on a property.'
        if fget is None:
            return self
        return type(self)(fget, self.fset, self.fdel, self.__doc__)

    def setter(self, fset):
        'Descriptor to change the setter on a property.'
        if fset is None:
            return self
        return type(self)(self.fget, fset, self.fdel, self.__doc__)

    def deleter(self, fdel):
        'Descriptor to change the deleter on a property.'
        if fdel is None:
            return self
        return type(self)(self.fget, self.fset, fdel, self.__doc__)
```

Où nous utilisons `type(self)(...)` afin de faire appel au constructeur de notre propriété.
Ce qui restera valable avec une nouvelle classe qui hériterait de `my_property`.

Une fois toutes ces méthodes réunies dans notre classe `my_property`, à laquelle on ajouterait encore une petite dose de documentation, on retrouve un équivalent complet de `property`.

```python
class my_property:
    '''
    my_property(fget=None, fset=None, fdel=None, doc=None) -> property attribute

    fget is a function to be used for getting an attribute value, and likewise
    fset is a function for setting, and fdel a function for del'ing, an
    attribute.  Typical use is to define a managed attribute x:

    class C(object):
        def getx(self): return self._x
        def setx(self, value): self._x = value
        def delx(self): del self._x
        x = my_property(getx, setx, delx, "I'm the 'x' property.")

    Decorators make defining new properties or modifying existing ones easy:

    class C(object):
        @my_property
        def x(self):
            "I am the 'x' property."
            return self._x
        @x.setter
        def x(self, value):
            self._x = value
        @x.deleter
        def x(self):
            del self._x
    '''

    def __init__(self, fget=None, fset=None, fdel=None, doc=None):
        if doc is None and fget is not None:
            doc = getattr(fget, '__doc__', None)
        self.fget, self.fset, self.fdel = fget, fset, fdel
        self.__doc__ = doc

    def __get__(self, instance, owner):
        'Return an attribute of instance, which is of type owner.'
        if instance is None:
            return self
        if self.fget is None:
            raise AttributeError('unreadable attribute')
        return self.fget(instance)

    def __set__(self, instance, value):
        'Set an attribute of instance to value.'
        if self.fset is None:
            raise AttributeError("can't set attribute")
        return self.fset(instance, value)

    def __delete__(self, instance):
        'Delete an attribute of instance.'
        if self.fdel is None:
            raise AttributeError("can't delete attribute")
        return self.fdel(instance)

    def getter(self, fget):
        'Descriptor to change the getter on a property.'
        if fget is None:
            return self
        return type(self)(fget, self.fset, self.fdel, self.__doc__)

    def setter(self, fset):
        'Descriptor to change the setter on a property.'
        if fset is None:
            return self
        return type(self)(self.fget, fset, self.fdel, self.__doc__)

    def deleter(self, fdel):
        'Descriptor to change the deleter on a property.'
        if fdel is None:
            return self
        return type(self)(self.fget, self.fset, fdel, self.__doc__)
```

Que nous pouvons alors utiliser dans notre classe `Temperature` par exemple.

```python
class Temperature:
    def __init__(self):
        self.value = 0

    @my_property
    def celsius(self): # le nom de la méthode devient le nom de la propriété
        return self.value
    @celsius.setter
    def celsius(self, value): # le setter doit porter le même nom
        self.value = value

    @my_property
    def fahrenheit(self):
        return self.value * 1.8 + 32
    @fahrenheit.setter
    def fahrenheit(self, value):
        self.value = (value - 32) / 1.8
```

```python
>>> t = Temperature()
>>> t.celsius
0
>>> t.fahrenheit
32.0
>>> t.celsius = 100
>>> t.fahrenheit
212.0
```
