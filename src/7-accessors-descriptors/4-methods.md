## Les méthodes

- methods, bound methods, static methods, class methods

Les méthodes en python semblent d'extérieur quelque chose d'assez simple. Cependant, si vous avez déjà rencontré les termes de méthodes d'instance (*bound methods*), méthodes de classe (*class methods*) ou méthodes statiques (*static methods*), vous avez pu vous demander comment cela fonctionnait.

En fait, les méthodes sont des descripteurs vers les fonctions que vous définissez à l'intérieur de votre classe. Elles sont même ce qu'on appelle des *non-data descriptors*, cest à dire des descripteurs qui ne définissent ni de *getter* ni de *setter*.

Définissons une simple classe `A` possédant différents types de méthodes.

```python
class A:
    def method(self):
        return self
    @staticmethod
    def staticmeth():
        pass
    @classmethod
    def clsmeth(cls):
        return cls
```

Puis appelons ces méthodes de différentes manières.

```python
>>> A.method()
>>> A().method()
>>> A.staticmeth()
>>> A().staticmeth()
>>> A.clsmeth()
>>> A().clsmeth()
```