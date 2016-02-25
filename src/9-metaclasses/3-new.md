## Le vrai constructeur

En Python, la méthode spéciale `__init__` est souvent appelée constructeur de l'objet.
Il s'agit en fait d'un abus de langage : `__init__` ne construit pas l'objet, elle intervient après la création de ce dernier pour l'initialiser.

Le vrai constructeur d'une classe est `__new__`.
Cette méthode prend la classe en premier paramètre (le paramètre `self` n'existe pas encore puisque l'objet n'est pas créé), et doit retourner l'objet nouvellement créé (contrairement à `__init__`).
Les autres paramètres sont identiques à ceux reçus par `__init__`.

C'est aussi `__new__` qui est chargée d'appeler l'initialiseur `__init__` (ce que fait `object.__new__` par défaut, en lui passant aussi la liste d'arguments).

Certains objets en Python ne sont pas mutables (modifiables), tels que les nombres, les chaînes de caractères ou les *tuples*, et ne peuvent donc pas avoir de méthode `__init__` pour initialiser l'objet.
Pour ces classes, ainsi que celles qui en héritent, il est impératif de passer par `__new__` pour gérer les paramètres de construction d'un objet.

```python
>>> class A:
...     def __new__(cls):
...         print('création')
...         return super().__new__(cls)
...     def __init__(self):
...         print('initialisation')
...
>>> A()
création
initialisation
<__main__.A object at 0x7ffb15ef9048>
```

Nous choisissons ici de faire appel à `object.__new__` dans notre constructeur (via `super`), mais nous n'y sommes pas obligés.
Rien ne nous oblige non plus — mise à part la logique — à retourner un objet du bon type.
