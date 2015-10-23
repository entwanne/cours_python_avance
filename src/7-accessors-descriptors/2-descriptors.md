## Les descripteurs

Les descripteurs sont une manière d'affecter des comportements plus évolués lors de la récupération/édition/suppression d'un attribut. Un descripteur est un objet assigné à un attribut, et dont des méthodes spéciales (`__get__`, `__set__`, et `__delete__`) seront appelées lorsque des opérations seront réalisées sur l'attribut.

`__get__` prend deux paramètres en plus du `self` : `instance` et `owner`.
`instance` correspond à l'objet sur lequel l'attribut est défini. Cependant, si l'attribut est récupéré depuis depuis la classe de l'instance (`Foo.attr`), `instance` vaudra `None`.
C'est dans ce cas que `owner` intervient, ce paramètre contient toujours la classe de l'instance.

`__set__` prend simplement l'instance et la nouvelle valeur, `__delete__` se contente de l'instance.

Pour reprendre notre exemple précédent sur les températures, nous pourrions avoir deux descripteurs `Celsius` et `Fahrenheit`, qui modifieraient à leur manière la valeur de notre objet `Temperature`.

```python
class Celsius:
    def __get__(self, instance, owner):
        # Dans le cas où on appellerait `Temperature.celsius`
	# On préfère retourner l'attribut lui-même
        if instance is None:
            return self
        return instance.value
    def __set__(self, instance, value):
        instance.value = value

class Fahrenheit:
    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.value * 1.8 + 32
    def __set__(self, instance, value):
        instance.value = (value - 32) / 1.8

class Temperature:
    celsius = Celsius()
    fahrenheit = Fahrenheit()

    def __init__(self):
        self.value = 0
```

Je vous laisse exécuter à nouveau les exemples précédents pour constater que le comportement est le même.

* <https://docs.python.org/3/reference/datamodel.html#implementing-descriptors>
