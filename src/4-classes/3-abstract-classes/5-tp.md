### TP: Reconnaissance d'interfaces

Je vous propose dans ce TP de nous intéresser à la reconnaissance d'interfaces comme nous l'avons fait dans ce chapitre.
Nous allons premièrement écrire une classe `Interface`, héritant de `abc.ABC`, qui permettra de vérifier qu'un type implémente un certain nombre de méthodes.
Cette classe sera destinée à être héritée pour spécifier quelles méthodes doivent être implémentées par quels types.
On trouvera par exemple une classe `Container` héritant d'`Interface` pour vérifier la présence d'une méthode `__contains__`.

Les méthodes nécessaires pour se conformer au type seront inscrites dans un attribut de classe `__methods__`.
Notre classe `Interface` définira la méthode `__subclasshook__` pour s'assurer que toutes les méthodes de la séquence `__methods__` sont présentes dans la classe.

La méthode `__subclasshook__` se déroulera en 3 temps :

* Premièrement, appeler l'implémentation parente *via* `super`, et retourner `False` si elle a retourné `False`. En effet, si la classe parente dit que le type n'est pas un sous-type, on est sûr qu'il n'en est pas un. Mais si la méthode parente retourne `True` ou `NotImplemented`, le doute peut persister ;
* Dans un second temps, nous récupérerons la liste de toutes les méthodes à vérifier. Il ne s'agit pas seulement de l'attribut `__methods__`, mais de cet attribut ainsi que celui de toutes les classes parentes ;
* Et finalement, nous testerons que chacune des méthodes est présente dans la classe, afin de retourner `True` si elle le sont toutes, et `NotImplemented` sinon.

Le deuxième point va nous amener à explorer le *MRO*, à l'aide de la méthode de classe `mro`, et de concaténer les attributs `__methods__` de toutes les classes (*via* la fonction `sum`).
Afin de toujours récupérer une séquence, nous utiliserons `getattr(cls, '__methods__', ())`, qui nous retournera un *tuple* vide si l'attribut `__methods__` n'est pas présent.

Quant au 3ème point, la *builtin* `all` va nous permettre de vérifier que chaque nom de méthode est présent dans la classe, et qu'il s'agit d'un *callable* et donc d'une méthode.

Notre classe `Interface` peut alors se présenter comme suit.

```python
import abc

class Interface(abc.ABC):
    # Attribut `__methods__` vide pour montrer sa structure
    __methods__ = ()

    @classmethod
    def __subclasshook__(cls, subcls):
        # Appel au __subclasshook__ parent
        ret = super().__subclasshook__(cls, subcls)
        if not ret:
            return ret
        # Récupération de toutes les méthodes
        all_methods = sum((getattr(c, '__methods__', ()) for c in cls.mro()), ())
        # Vérification de la présence des méthodes dans la classe
        if all(callable(getattr(subcls, meth, None)) for meth in all_methods):
            return True
        return NotImplemented
```

Nous pouvons dès lors créer nos nouvelles classes hérités d'`Interface` avec leurs propres attributs `__methods__`.

```python
class Container(Interface):
    __methods__ = ('__contains__',)

class Sized(Interface):
    __methods__ = ('__len__',)

class SizedContainer(Sized, Container):
    pass

class Subscriptable(Interface):
    __methods__ = ('__getitem__',)

class Iterable(Interface):
    __methods__ = ('__iter__',)
```

Et qui fonctionnent comme prévu.

```python
>>> isinstance([], Iterable)
True
>>> isinstance([], Subscriptable)
True
>>> isinstance([], SizedContainer)
True
>>> gen = (x for x in range(10))
>>> isinstance(gen, Iterable)
True
>>> isinstance(gen, Subscriptable)
False
>>> isinstance(gen, SizedContainer)
False
```
