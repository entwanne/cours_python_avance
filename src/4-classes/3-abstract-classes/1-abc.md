### Module `abc`

Pour rappel, le module [`abc`](https://docs.python.org/3/library/abc.html) donne accès à la classe `ABC` qui permet par héritage de construire une classe abstraite, et au décorateur `abstractmethod` pour définir des méthodes abstraites.

Une autre classe importante réside dans ce module, `ABCMeta`.
`ABCMeta` est la métaclasse de la classe `ABC`, et donc le type de toutes les classes abstraites.
C'est `ABCMeta` qui s'occupe de référencer dans l'ensemble `__abstractmethods__`[^abstractmethods]
les méthodes abstraites définies dans la classe.

Mais outre le fait de pouvoir spécifier les méthodes à implémenter, les classes abstraites de Python ont un autre but : définir une interface.
Vous connaissez probablement `isinstance`, qui permet de vérifier qu'un objet est du bon type ;
peut-être moins `issubclass`, pour vérifier qu'une classe *hérite* d'une autre.

```python
>>> isinstance(4, int) # 4 est un int
True
>>> isinstance(4, str) # 4 n'est pas une str
False
>>> issubclass(int, object) # int hérite d'object
True
>>> issubclass(int, str) # int n'hérite pas de str
False
```

Ces deux fonctions sont en fait des opérateurs, qui font appel à des méthodes spéciales, et sont à ce titre surchargeables, comme nous le verrons par la suite.

J'ai utilisé plus haut le terme « hérite » pour décrire l'opérateur `issubclass`.
C'est en fait légèrement différent, `issubclass` permet de vérifier qu'une classe est une sous-classe (ou sous-type) d'une autre.

Quand une classe hérite d'une autre, elle en devient un sous-type (sauf cas exceptionnels[^subclasscheck]).
Mais elle peut aussi être sous-classe de classes dont elle n'hérite pas.

C'est le but de la méthode `register` des classes `ABC`.
Elle sert à enregistrer une classe comme sous-type de la classe abstraite.

Imaginons une classe abstraite `Sequence` correspondant aux types de séquences connus (`str`, `list`, `tuple`)[^sequence].
Ces types sont des *builtins* du langage, il ne nous est pas pas possible de les redéfinir pour les faire hériter de `Sequence`.
Mais la méthode `register` de notre classe abstraite `Sequence` va nous permettre de les enregistrer comme sous-classes.

```python
>>> import abc
>>> class Sequence(abc.ABC):
...     pass
...
>>> Sequence.register(str)
<class 'str'>
>>> Sequence.register(list)
<class 'list'>
>>> Sequence.register(tuple)
<class 'tuple'>
>>> isinstance('foo', Sequence)
True
>>> isinstance(42, Sequence)
False
>>> issubclass(list, Sequence)
True
>>> issubclass(dict, Sequence)
False
```

[^abstractmethods]: L'ensemble `__abstractmethods__` est ensuite analysé pour savoir si une classe peut être instanciée, le constructeur d'`object` levant une erreur dans le cas échéant.
[^subclasscheck]: Voir à ce propos la section « `issubclass` ».
[^sequence]: Pour rappel, une séquence est un objet *indexable* et *sliceable*.
