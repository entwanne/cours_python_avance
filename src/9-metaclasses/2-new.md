## Le vrai constructeur

En Python, la méthode spéciale `__init__` est souvent appelée constructeur de l'objet.
Il s'agit en fait d'un abus de langage : `__init__` ne construit pas l'objet, elle intervient après la création de ce dernier pour l'initialiser.

Le vrai constructeur d'une classe est `__new__`.
Cette méthode prend la classe courante en premier paramètre (le paramètre `self` n'existe pas encore puisque l'objet n'est pas créé), et doit retourner l'objet nouvelle créé (contrairement à `__init__`).

C'est aussi `__new__` qui est chargée d'appeler l'initialiseur `__init__` (ce que fait `object.__new__` par défaut, en lui passant le reste de la liste d'arguments).

```python
>>> class A:
...     def __new__(cls, *args, **kwargs):
...         print('création')
...         return super().__new__(cls, *args, **kwargs)
...     def __init__(self):
...         print('initialisation')
...
>>> A()
création
initialisation
<__main__.A object at 0x7ffb15ef9048>
```

Nous choisissons ici de faire appel à `object.__new__` dans notre constructeur (via `super`), mais nous n'y sommes pas obligés.
Nous ne sommes même pas obligés de retourner un objet du bon type (cependant, la logique le veut).
