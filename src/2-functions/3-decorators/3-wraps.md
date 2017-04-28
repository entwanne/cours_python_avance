### Envelopper une fonction

Une fonction n'est pas seulement un bout de code avec des paramètres. C'est aussi un nom (des noms, avec ceux des paramètres), une documentation (*docstring*), des annotations, etc.
Quand nous décorons une fonction à l'heure actuelle (dans les cas où nous en retournons une nouvelle), nous perdons toutes ces informations annexes.

Un exemple pour nous en rendre compte :

```python
>>> def decorator(f):
...     def decorated(*args, **kwargs):
...         return f(*args, **kwargs)
...     return decorated
...
>>> @decorator
... def addition(a: int, b: int) -> int:
...     "Cette fonction réalise l'addition des paramètres `a` et `b`"
...     return a + b
...
>>> help(addition)
Help on function decorated in module __main__:

decorated(*args, **kwargs)
```

Alors, que voit-on ? Pas grand chose.
Le nom qui apparaît est celui de `decorated`, les paramètres sont `*args` et `**kwargs` (sans annotations), et nous avons aussi perdu notre *docstring*.
Autant dire qu'il ne reste rien pour comprendre ce que fait la fonction.

#### Envelopper des fonctions

Plus tôt dans ce cours, je vous parlais du module [`functools`](https://docs.python.org/3/library/functools.html).
Il ne nous a pas encore révélé tous ses mystères.

Nous allons ici nous intéresser aux fonctions `update_wrapper` et `wraps`.
Ces fonctions vont nous permettre de copier les informations d'une fonction vers une nouvelle.

`update_wrapper` prend en premier paramètre la fonction à laquelle ajouter les informations et celle dans laquelle les puiser en second. Pour reprendre notre exemple précédent, il nous faudrait faire :

```python
import functools

def decorator(f):
    def decorated(*args, **kwargs):
        return f(*args, **kwargs)
    functools.update_wrappers(decorated, f) # Nous copions les informations de `f` dans `decorated`
    return decorated
```

Mais une autre fonction nous sera bien plus utile car plus concise, et recommandée par la documentation Python pour ce cas.
Il s'agit de `wraps`, qui retourne un décorateur lorsqu'appelé avec une fonction.

La fonction décorée par `wraps` prendra les informations de la fonction passée à l'appel de `wraps`.
Ainsi, nous n'aurons qu'à précéder toutes nos fonctions decorées par `@functools.wraps(fonction_a_decorer)`. Dans notre exemple :

```python
import functools

def decorator(f):
    @functools.wraps(f)
    def decorated(*args, **kwargs):
        return f(*args, **kwargs)
    return decorated
```

Vous pouvez maintenant redéfinir la fonction `addition`, et tester à nouveau l'appel à `help` pour constater les différences.
