### Les descripteurs

Les descripteurs sont une manière de placer des comportements plus évolués derrière des attributs.
En effet, plutôt que toujours recourir à `__getattr__` et consorts, ils sont un autre moyen d'avoir des attributs dynamiques.
Les propriétés (*properties*) sont des exemples de descripteurs.

Un descripteur se définit comme attribut d'une classe, et devient accessible en tant qu'attribut de ses instances.
Pour cela, le descripteur peut implémenter des méthodes spéciales `__get__`/`__set__`/`__delete__` qui seront respectivement appelées lors de la lecture/écriture/suppression de l'attribut sur une instance de la classe.

Par exemple, si une classe `Foo` définit un descripteur de type `Descriptor` sous son attribut `attr`, alors, avec `foo` instance de `Foo` :

- `foo.attr` fera appel à `Descriptor.__get__` ;
- `foo.attr = value` à `Descriptor.__set__` ;
- et `del foo.attr` à `Descriptor.__delete__`.

La méthode `__get__` du descripteur prend deux paramètres : `instance` et `owner`.
`instance` correspond à l'objet depuis lequel on accède à l'attribut.
Dans le cas où l'attribut est récupéré depuis depuis la classe (`Foo.attr` plutôt que `foo.attr`), `instance` vaudra `None`.
C'est alors que `owner` intervient, ce paramètre contient toujours la classe définissant le descripteur (`Foo`).

`__set__` prend simplement l'instance et la nouvelle valeur, et `__delete__` se contente de l'instance.
Contrairement à `__get__`, ces deux dernières méthodes ne peuvent s'utiliser que sur les instances, et non sur la classe[^class_descriptor], d'où l'absence du paramètre `owner`.

[^class_descriptor]: En effet, redéfinir `A.attr` ou le supprimer ne doit déclencher aucune méthode spéciale du descripteur, ça revient juste à redéfinir/supprimer l'attribut de classe.

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

#### La méthode `__set_name__`

Depuis Python 3.6[^python36], les descripteurs peuvent aussi être pourvus d'une méthode `__set_name__`.
Cette méthode est appelée pour chaque assignation d'un descripteur à un attribut dans le corps de la classe.
La méthode reçoit en paramètres la classe et le nom de l'attribut auquel le descripteur est assigné.

[^python36]: <https://zestedesavoir.com/articles/1540/sortie-de-python-3-6/#principales-nouveautes>

```python
>>> class Descriptor:
...     def __set_name__(self, owner, name):
...         print(name)
...
>>> class A:
...     value = Descriptor()
...
value
```

Le descripteur peut ainsi agir dynamiquement sur la classe en fonction du nom de son attribut.

Nous pouvons imaginer un descripteur `PositiveValue`, qui assurera qu'un attribut sera toujours positif.
Le descripteur stockera ici sa valeur dans un attribut de l'instance, en utilisant pour cela son nom préfixé d'un *underscore*.

```python
class PositiveValue:
    def __get__(self, instance, owner):
        return getattr(instance, self.attr)

    def __set__(self, instance, value):
        setattr(instance, self.attr, max(0, value))

    def __set_name__(self, owner, name):
        self.attr = '_' + name

class A:
    x = PositiveValue()
    y = PositiveValue()
```

```python
>>> a = A()
>>> a.x = 15
>>> a.x
15
>>> a._x
15
>>> a.x -= 20
>>> a.x
0
>>> a.y = -1
>>> a.y
0
```
