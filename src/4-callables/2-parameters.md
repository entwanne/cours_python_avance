## Paramètres de fonctions

### Paramètres et arguments

Revenons un peu aux paramètres de fonctions (et plus généralement de *callables*). Les paramètres sont décrits lors de la définition de la fonction, ils possèdent un nom, et potentiellement une valeur par défaut.

Il faut les distinguer des arguments: les arguments sont les valeurs passées lors de l'appel.

```python
def function(a, b, c, d=1, e=2):
    return
```

`a`, `b`, `c`, `d` et `e` sont les paramètres de la fonction `function`. `a`, `b` et `c` n'ont pas de valeur par défaut, il faut donc en préciser explicitement lors de l'appel, pour que celui-ci soit valide. Les paramètres avec valeur par défaut se placent obligatoirement après les autres.

```python
function(3, 4, d=5, c=3)
```

Nous sommes là dans un appek de fonction, donc les valeurs sont des arguments.
`3` et `4` sont des arguments positionnels, car ils sont repérés par leur position, et seront donc associés aux deux premiers paramètres de la fonction (`a` et `b`).
`d=5` et `c=3` sont des arguments nommés, car la valeur est précédée du nom du paramètre associé. Ils peuvent ainsi être placés dans n'importe quel ordre (pour peu qu'ils soient placés après les arguments positionnels).

Voici enfin différents cas d'appels posant problème:

```python
>>> function(1) # Pas assez d'arguments
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: function() missing 2 required positional arguments: 'b' and 'c'
>>> function(1, 2, 3, 4, 5, 6) # Trop d'arguments
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: function() takes from 3 to 5 positional arguments but 6 were given
>>> function(1, b=2, 3) # Mélange d'arguments positionnels et nommés
  File "<stdin>", line 1
SyntaxError: non-keyword arg after keyword arg
>>> function(1, 2, b=3, c=4) # b est à la fois positionnel et nommé
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: function() got multiple values for argument 'b'
```

### L'opérateur `splat`

- `*` et `**`: différents de l'addition et de l'exponentiation
- `func(parametres_sans, valeur_par_defaut, *args, avec='valeur', par='defaut', **kwargs)` -> positionnels dans `args`, nommés dans `kwargs` (`*args` peut être placé avant, après, ou au milieu des paramètres avec valeur par défaut)`
- `func(*[1,2,3], **{'test': 4})` lors de l'appel

Autres utilités du splat:

- `a, b, *_ = 0, 1, 2, 3, ...`
- `a, *_, b = 0, 1, ..., 9, 10`
