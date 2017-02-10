### Module `abc`

Pour rappel, le module `abc` donne accès à la classe `ABC` qui permet par héritage de construire une classe abstraite, et au décorateur `abstractmethod` pour définir des méthodes abstraites.

Une autre classe importante réside dans ce module, `ABCMeta`, une métaclasse donc, type de toutes les classes abstraites.
C'est `ABCMeta` qui s'occupe de référencer l'ensemble des méthodes abstraites définies dans la classe.

Mais outre le fait de pouvoir spécifier les méthodes à implémenter, les classes abstraites de Python ont un autre but : définir une interface.
Vous connaissez probablement `isinstance`, qui permet de vérifier qu'un objet est du bon type ; peut-être moins `issubclass`, pour vérifier qu'une classe est une sous-classe d'une autre.

```python
>>> isinstance(4, int)
True
>>> isinstance(4, str)
False
>>> issubclass(int, object)
True
>>> issubclass(int, str)
False
```

Ces deux fonctions sont en fait des opérateurs, qui font appel à des méthodes spéciales, et sont à ce titre surchargeables, comme nous le verrons par la suite.

+ `ABC.register`
