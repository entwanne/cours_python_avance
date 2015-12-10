# Accesseurs et descripteurs

L'expression `foo.bar` est en apparence très simple : on accède à l'attribut `bar` d'un objet `foo`.
Cependant, divers mécanismes entrent en jeu pour nous retourner cette valeur, nous permettant d'accéder à des attributs définis à la volée.

Nous allons découvrir dans ce chapitre quels sont ces mécanismes, et comment les manipuler.

Sachez premièrement que `foo.bar` revient à exécuter

* `getattr(foo, 'bar')`

Il s'agit là de la lecture, deux fonctions sont équivalentes pour la modification et la suppression :

* `setattr(foo, 'bar', value)` pour `foo.bar = value`
* `delattr(foo, 'bar')` pour `del foo.bar`
