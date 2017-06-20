### TP : Vérification de signature

Afin de nous exercer un peu sur les signatures, nous allons créer une fonction vérifiant la validité d'un ensemble d'arguments.
Cette fonction, `signature_check`, recevra en paramètres la signature à tester, et tous les arguments positionnels et nommés de l'appel.

#### Prototype

On pourrait à première vue la prototyper ainsi.

```python
def signature_check(signature, *args, **kwargs):
    ...
```

Mais ce serait oublier que `signature` peut aussi posséder un paramètre nommé `signature`, qui ne pourrait alors être testé.
Nous allons donc plutôt récupérer la signature à tester depuis `*args`.

```python
def signature_check(*args, **kwargs):
    signature, *args = args # Soit signature = args[0] et args = list(args[1:])
    ...
```

Passons maintenant au contenu de notre fonction.
Celle-ci va devoir itérer sur les paramètres, pour leur faire correspondre les arguments.
On lèvera des `TypeError` en cas de non-correspondance ou de manque/surplus d'arguments.

Le plus simple est de procéder en consommant la liste `args` et le dictionnaire `kwargs`.
Les arguments seront supprimés chaque fois qu'une correspondance sera faite avec un paramètre.

S'il reste des arguments après itération de tous les paramètres, c'est qu'il y a surplus.
On lèvera donc une erreur pour l'indiquer.

On obtient alors un premier squelette.

```python
def signature_check(*args, **kwargs):
    sig, *args = args
    for param in sig.parameters.values():
        ...
    if args:
        raise TypeError('too many positional arguments')
    if kwargs:
        raise TypeError('too many keyword arguments')
```

#### Paramètres

Attachons-nous maintenant à remplacer ces points de suspension par le traitement des paramètres.
Pour rappel, on retrouve 5 sortes de paramètres, qui seront traitées différemment.

##### `VAR_POSITIONAL`

Si un paramètre `VAR_POSITIONAL` est présent, il aura pour effet de consommer tous les arguments restant, c'est-à-dire de vider `args`.

```python
if param.kind == param.VAR_POSITIONAL:
    args.clear()
```

##### `VAR_KEYWORD`

De même ici, mais en vidant `kwargs`, puisque tous les arguments nommés sont consommés.

```python
elif param.kind == param.VAR_KEYWORD:
    kwargs.clear()
```

##### `POSITIONAL_ONLY`

Passons aux choses sérieuses avec les paramètres `POSITIONAL_ONLY`.
Les arguments correspondant à ce type de paramètres se trouveront nécessairement dans `args`.

Deux cas sont cependant à distinguer :

* Si la liste `args` n'est pas vide, nous en consommons le premier élément ;
* Si elle est vide, il faut alors vérifier que le paramètre possède une valeur par défaut.

En effet, si aucun argument n'est reçu, le paramètre prend sa valeur par défaut.
Mais s'il ne possède aucune valeur par défaut, il faut alors lever une erreur : le paramètre est manquant.

```python
elif param.kind == param.POSITIONAL_ONLY:
    if args:
        del args[0]
    elif param.default == param.empty: # Ni argument ni valeur par défaut
        raise TypeError("Missing '{}' positional argument".format(param.name))
```

##### `KEYWORD_ONLY`

On retrouve ici un code semblable au *positional-only*, mais en s'intéressant à `kwargs` plutôt qu'à `args`.
Le même cas d'erreur est à traiter si le paramètre n'est associé à aucune valeur.

```python
elif param.kind == param.KEYWORD_ONLY:
    if param.name in kwargs:
        del kwargs[param.name]
    elif param.default == param.empty:
        raise TypeError("Missing '{}' keyword argument".format(param.name))
```

##### `POSITIONAL_OR_KEYWORD`

Le dernier cas, le plus complexe, est celui des paramètres pouvant recevoir arguments positionnels ou nommés.
Nous devrons alors tester la présence d'un argument dans chacun des deux conteneurs.

Nous serons confrontés à un nouveau cas d'erreur : si un paramètre est associé à la fois à un argument positionnel et à un nommé.

```python
else: # POSITIONAL_OR_KEYWORD
    positional = keyword = False
    if args: # Prend valeur dans args
        del args[0]
        positional = True
    if param.name in kwargs: # Prend valeur dans kwargs
        del kwargs[param.name]
        keyword = True
    if positional and keyword:
        raise TypeError("Multiple arguments for parameter '{}'".format(param.name))
    if not positional and not keyword and param.default == param.empty:
        raise TypeError("Missing argument for '{}' parameter".format(param.name))
```

#### Résultat

En mettant bout à bout nos morceaux de code, nous obtenons notre fonction `signature_check` pour tester si des arguments correspondent à une signature.
La fonction ne retourne rien, mais lève une erreur en cas de non-correspondance.

```python
def signature_check(*args, **kwargs):
    sig, *args = args
    for param in sig.parameters.values():
        if param.kind == param.VAR_POSITIONAL: # Consomme tous les positionnels
            args.clear()
        elif param.kind == param.VAR_KEYWORD: # Consomme tous les nommés
            kwargs.clear()
        elif param.kind == param.POSITIONAL_ONLY: # Prend valeur dans args
            if args:
                del args[0]
            elif param.default == param.empty: # Ni argument ni valeur par défaut
                raise TypeError("Missing '{}' positional argument".format(param.name))
        elif param.kind == param.KEYWORD_ONLY: # Prend valeur dans kwargs
            if param.name in kwargs:
                del kwargs[param.name]
            elif param.default == param.empty:
                raise TypeError("Missing '{}' keyword argument".format(param.name))
        else: # POSITIONAL_OR_KEYWORD
            positional = keyword = False
            if args: # Prend valeur dans args
                del args[0]
                positional = True
            if param.name in kwargs: # Prend valeur dans kwargs
                del kwargs[param.name]
                keyword = True
            if positional and keyword:
                raise TypeError("Multiple arguments for parameter '{}'".format(param.name))
            if not positional and not keyword and param.default == param.empty:
                raise TypeError("Missing argument for '{}' parameter".format(param.name))
    if args:
        raise TypeError('too many positional arguments')
    if kwargs:
        raise TypeError('too many keyword arguments')
```

Et pour voir `signature_check` en action :

```python
>>> sig = inspect.signature(lambda a, b: None)
>>> signature_check(sig, 3, 5)
>>> signature_check(sig, 3, b=5)
>>> signature_check(sig, 3)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "signature_check.py", line 37, in signature_check
    raise TypeError("Missing argument for '{}' parameter".format(param.name))
TypeError: Missing argument for 'b' parameter
>>> signature_check(sig, 3, 5, 7)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "signature_check.py", line 39, in signature_check
    raise TypeError('too many positional arguments')
TypeError: too many positional arguments
>>> signature_check(sig, 3, 5, b=5)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "signature_check.py", line 35, in signature_check
    raise TypeError("Multiple arguments for parameter '{}'".format(param.name))
TypeError: Multiple arguments for parameter 'b'
```

```python
>>> sig = inspect.signature(lambda a, *, b: None)
>>> signature_check(sig, 3, 5)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "signature_check.py", line 25, in signature_check
    raise TypeError("Missing '{}' keyword argument".format(param.name))
TypeError: Missing 'b' keyword argument
>>> signature_check(sig, 3, b=5)
>>> signature_check(sig, 3, b=5, c=7)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "signature_check.py", line 41, in signature_check
    raise TypeError('too many keyword arguments')
TypeError: too many keyword arguments
```

```python
>>> sig = inspect.signature(lambda *args, file=sys.stdin: None)
>>> signature_check(sig, 1, 2, 3, 4)
>>> signature_check(sig)
>>> signature_check(sig, 1, 2, 3, 4, file=None)
>>> signature_check(sig, 1, 2, 3, 4, file=None, foo=0)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "signature_check.py", line 41, in signature_check
    raise TypeError('too many keyword arguments')
TypeError: too many keyword arguments
```
