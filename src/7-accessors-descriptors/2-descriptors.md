## Les descripteurs

Les descripteurs sont une manière d'avoir des comportements plus évolués lors de la récupération/édition/suppression d'un attribut.
Un descripteur est un attribut particulier d'une classe, et dont certaines méthodes spéciales (`__get__`, `__set__`, et `__delete__`) sont appelées lorsque les accès correspondant sont réalisés sur l'attribut.

Le descripteur peut alors s'utiliser sur la classe dans laquelle il est défini, ou sur les instances de cette classe.
Cependant, seul l'accès en lecture sera possible sur la classe, les opérations de modification et de suppression servant à remplacer ou supprimer le descripteur.

La méthode `__get__` du descripteur prend deux paramètres : `instance` et `owner`.
`instance` correspond à l'objet depuis lequel on accède à l'attribut.
Dans le cas où l'attribut est récupéré depuis depuis la classe (`Foo.attr`), `instance` vaudra `None`.
C'est alors que `owner` intervient, ce paramètre contient toujours la classe.

`__set__` prend simplement l'instance et la nouvelle valeur, `__delete__` se contente de l'instance.

Pour reprendre notre exemple précédent sur les températures, nous pourrions avoir deux descripteurs `Celsius` et `Fahrenheit`, qui modifieraient à leur manière la valeur de notre objet `Temperature`.

```python
class Celsius:
    def __get__(self, instance, owner):
        # Dans le cas où on appellerait `Temperature.celsius`
        # On préfère retourner le descripteur lui-même
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
    # On instancie les deux attributs de la classe
    celsius = Celsius()
    fahrenheit = Fahrenheit()

    def __init__(self):
        self.value = 0
```

Je vous laisse exécuter à nouveau les exemples précédents pour constater que le comportement est le même.
