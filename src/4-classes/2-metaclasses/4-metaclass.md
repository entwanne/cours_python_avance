### Les métaclasses

Nous avons vu qu'une métaclasse était simplement une classe héritant de `type` et permettant d'instancier des classes.
Puisque nous voulons altérer la création et non l'initialisation, c'est dans le constructeur que le tout va s'opérer.

Le constructeur d'une métaclasse devra donc prendre les mêmes paramètres que `type`, et faire appel à ce dernier pour créer notre objet.

```python
>>> class M(type):
...     def __new__(cls, name, bases, dict):
...         return super().__new__(cls, name, bases, dict)
...
>>> A = M('A', (), {})
>>> A
<class '__main__.A'>
>>> type(A)
<class '__main__.M'>
```

Nous avons ainsi créé notre propre métaclasse, et l'avons utilisée pour instancier une nouvelle classe.

Une autre syntaxe pour instancier notre métaclasse est possible, à l'aide du mot clef `class` : la métaclasse à utiliser peut être spécifiée entre les parenthèses derrière le nom de la classe.

```python
>>> class B(metaclass=M):
...     pass
...
>>> type(B)
<class '__main__.M'>
```

#### Préparation de la classe

Nous avons étudié dans le chapitre sur les accesseurs l'attribut `__dict__` des classes. Celui-ci est un dictionnaire, mais à quel moment est-il créé ?

Lors de la définition d'une classe, avant même de s'attaquer à ce que contient son corps, celle-ci est préparée.
C'est à dire que le dictionnaire `__dict__` est instancié, afin d'y stocker tout ce qui sera défini dans le corps.

Par défaut, la préparation d'une classe est donc un appel à `dict`, qui retourne un dictionnaire vide.
Mais si la métaclasse est dotée d'une méthode de classe `__prepare__`, celle-ci sera appelée en lieu et place de `dict`. Cette méthode doit toutefois retourner un dictionnaire ou objet similaire. Elle peut par exemple initialiser ce dictionnaire avec des valeurs par défaut.

```python
>>> class M(type):
...     @classmethod
...     def __prepare__(cls, name, bases):
...         return {'test': lambda self: print(self)}
...
>>> class A(metaclass=M): pass
...
>>> A().test()
<__main__.A object at 0x7f886cfd4e10>
```

#### Une métaclasse utile

Maintenant que nous savons créer et utiliser des métaclasses, servons-nous-en à bon escient. Il faut bien noter que les métaclasses répondent à des problèmes bien spécifiques, leur utilisation pourrait ne pas vous sembler évidente.

Les énumérations en Python sont implémentées à l'aide de métaclasses.

```python
>>> from enum import Enum
>>> class Color(Enum):
...     red = 1
...     green = 2
...     blue = 3
...
>>> Color.red
<Color.red: 1>
>>> Color(1) is Color.red
True
```

En héritant d'`Enum`, on hérite aussi de sa métaclasse (`EnumMeta`)

```python
>>> type(Color)
<class 'enum.EnumMeta'>
```

Attention d'ailleurs, lorsque vous héritez de plusieurs classes, assurez-vous toujours que leurs métaclasses soient compatibles (la hiérarchie entre les différentes métaclasses doit être linéaire).

Une implémentation simplifiée possible d'`Enum` est la suivante :

```python
class EnumMeta(type):
    def __new__(cls, name, bases, dict):
        # Cache dans lequel les instances seront stockées
        dict['__mapping__'] = {}
        # Membres de l'énumération (tous les attributs qui ne sont pas du type __foo__)
        members = {k: v for (k, v) in dict.items() if not (k.startswith('__') and k.endswith('__'))}
        enum = super().__new__(cls, name, bases, dict)
        # On instancie toutes les valeurs possibles et on les intègre à la classe
        for key, value in members.items():
            value = enum(value)
            value.name = key # On spécifie le nom du membre
            setattr(enum, key, value)
        return enum

class Enum(metaclass=EnumMeta):
    def __new__(cls, value):
        # On retourne la valeur depuis le cache si elle existe
        if value in cls.__mapping__:
            return cls.__mapping__[value]
        v = super().__new__(cls)
        v.value = value
        v.name = ''
        # On l'ajoute au cache
        cls.__mapping__[value] = v
        return v
    def __repr__(self):
        return '<{}.{}: {}>'.format(type(self).__name__, self.name, self.value)
```

Notre exemple précédent avec les couleurs s'exécute de la même manière.
