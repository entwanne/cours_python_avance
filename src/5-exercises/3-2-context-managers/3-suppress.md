### Suppression d'erreurs

**Pré-requis : Gestionnaires de contexte**

Vous pensiez en avoir terminé avec `contextlib` ? Que nenni !
Ce module présente beaucoup de gestionnaires de contexte assez simples à réimplémenter, il est donc idéal pour les exercices.

Intéressons-nous maintenant à `suppress`, qui permet d'ignorer des exceptions, comme pourrait le faire un `try`/`except`.
En effet, les deux exemples de codes qui suivent sont équivalents.

```python
from contextlib import suppress

with suppress(TypeError):
    print(1 + '2')
```

```python
try:
    print(1 + '2')
except TypeError:
    pass
```

Nous l'avons vu, les erreurs qui surviennent dans un contexte sont transmises à la méthode `__exit__` du gestionnaire, qui peut choisir d'annuler l'exception en retournant `True`.
Tout ce que nous avons à faire est donc de vérifier si une exception est survenue et si cette dernière est du bon type, puis retourner `True` si ces deux conditions sont respectées.

Pour vérifier que l'exception est du bon type, il nous suffira de faire appel à `issubclass` et tester que le pramètre `exc_type` est un sous-type de celui passé à la construction du gestionnaire.

Le code de notre gestionnaire de contexte se présente alors comme suit.

```python
class suppress:
    def __init__(self, exc_type):
        self.exc_type = exc_type

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_value, traceback):
        return exc_type is not None and issubclass(exc_type, self.exc_type)
```

Je vous laisse expérimenter et vérifier que notre classe répond bien aux attentes.
Une petite subtilité tout de même : `suppress` peut normalement s'utiliser en spécifiant plusieurs types d'exception à annuler.

```python
with suppress(TypeError, ValueError, IndexError):
    print(1 + '2')
```

Étant donné qu'`issubclass` peut prendre un *tuple* en second paramètre, la modification du code de notre gestionnaire de contexte sera très rapide.

```python
class suppress:
    def __init__(self, *exc_types):
        self.exc_types = exc_types

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_value, traceback):
        return exc_type is not None and issubclass(exc_type, self.exc_types)
```
