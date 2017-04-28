### TP : Arguments positionnels

Nous avons vu avec les signatures qu'il existait en Python des paramètres *positional-only*,
c'est à dire qui ne peuvent recevoir que des arguments positionnels.

Mais il n'existe à ce jour aucune syntaxe pour écrire en Python une fonction avec des paramètres *positional-only*.
Il est seulement possible, comme nous l'avons fait au TP précédent, de récupérer les arguments positionnels avec `*args` et d'en extraire les valeurs qui nous intéressent.

Nous allons alors développer un décorateur pour pallier à ce manque.
Ce décorateur modifiera la signature de la fonction reçue pour transformer en *positional-only* ses `n` premiers paramètres.
`n` sera un paramètre du décorateur.

Python nous permet de redéfinir la signature d'une fonction, en assignant la nouvelle signature à son attribut `__signature__`.
Mais cette redéfinition n'est que cosmétique (elle apparaît par exemple dans l'aide de la fonction).
Ici, nous voulons que la modification ait un effet.

Nous créerons donc une fonction *wrapper*, qui se chargera de vérifier la conformité des arguments avec la nouvelle signature.

Nous allons diviser le travail en deux parties :

* Dans un premier temps, nous réaliserons une fonction pour réécrire une signature ;
* Puis dans un second temps, nous écrirons le code du décorateur.

#### Réécriture de la signature

La première fonction, que nous appellerons `signature_set_positional`, recevra en paramètres une signature et un nombre `n` de paramètres à passer en *positional-only*.
La fonction retournera une signature réécrite.

Nous utiliserons donc les méthodes `replace` de la signature et des paramètres, pour changer le positionnement des paramètres ciblés, et mettre à jour la liste des paramètres de la signature.

La fonction itérera sur les `n` premiers paramètres, pour les convertir en *positional-only*.

On distinguera trois cas :

* Le paramètre est déjà *positional-only*, il n'y a alors rien à faire ;
* Le paramètre est *positional-or-keyword*, il peut être transformé ;
* Le paramètre est d'un autre type, il ne peut pas être transformé, on lèvera alors une erreur.

Puis une nouvelle signature sera créée et retournée avec cette nouvelle liste de paramètres.

```python
def signature_set_positional(sig, n):
    params = list(sig.parameters.values()) # Liste des paramètres
    if len(params) < n:
        raise TypeError('Signature does not have enough parameters')
    for i, param in zip(range(n), params): # Itère sur les n premiers paramètres
        if param.kind == param.POSITIONAL_ONLY:
            continue
        elif param.kind == param.POSITIONAL_OR_KEYWORD:
            params[i] = param.replace(kind=param.POSITIONAL_ONLY)
        else:
            raise TypeError('{} parameter cannot be converted to POSITIONAL_ONLY'.format(param.kind))
    return sig.replace(parameters=params)
```

#### Décorateur paramétré

Passons maintenant à `positional_only`, notre décorateur paramétré.
Pour rappel, un décorateur paramétré est une fonction qui retourne un décorateur.
Et un décorateur est une fonction qui reçoit une fonction et retourne une fonction.

Le décorateur proprement dit se chargera de calculer la nouvelle signature et de l'appliquer à la fonction décorée.
Il créera aussi un *wrapper* à la fonction, lequel se chargera de vérifier la correspondance des arguments avec la signature.

Nous n'oublierons pas d'appliquer `functools.wraps` à notre *wrapper* pour récupérer les informations de la fonction initiale.

```python
import functools
import inspect

def positional_only(n):
    def decorator(f):
        sig = signature_set_positional(inspect.signature(f), n)
        @functools.wraps(f)
        def decorated(*args, **kwargs):
            bound = sig.bind(*args, **kwargs)
            return f(*bound.args, **bound.kwargs)
        decorated.__signature__ = sig
        return decorated
    return decorator
```

Voyons maintenant l'utilisation.

```python
>>> @positional_only(2)
... def addition(a, b):
...     return a + b
...
>>> print(inspect.signature(addition))
(a, b, /)
>>> addition(3, 5)
8
>>> addition(3, b=5)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: 'b' parameter is positional only, but was passed as a keyword
```

```python
>>> @positional_only(1)
... def addition(a, b):
...     return a + b
...
>>> addition(3, 5)
8
>>> addition(3, b=5)
8
>>> addition(a=3, b=5)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: 'a' parameter is positional only, but was passed as a keyword
```
