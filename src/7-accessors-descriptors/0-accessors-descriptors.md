# Accesseurs et descripteurs

En Python, tout est dynamique, vous pouvez donc interférer à peu près n'importe où. Ainsi, par exemple, quand on accède à l'attribut `bar` d'un objet `toto` via `foo.bar`, divers mécanismes entrent en jeu pour nous fournir la valeur demandée.

Nous allons découvrir dans ce chapitre quels sont ces mécanismes, et comment les manipuler.

Sachez premièrement que `foo.bar` revient à exécuter

* `getattr(foo, 'bar')`

Il s'agit là de la lecture, deux fonctions sont équivalents pour la modification et la suppression :

* `setattr(foo, 'bar', value)` pour `foo.bar = value`
* `delattr(foo, 'bar')` pour `del foo.bar`
