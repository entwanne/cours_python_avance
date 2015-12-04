## Envelopper une fonction

Une fonction, ça n'est pas seulement un bout de code avec des paramètres. C'est aussi un nom (des noms, avec ceux des paramètres), une documentation (*docstring*), des annotations, etc.
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
```

Alors, que voit-on ? Pas grand chose.
Le nom qui apparaît est celui de `decorated`, les paramètres sont `*args` et `**kwargs` (sans annotations), et nous avons aussi perdu notre *docstring*.
Autant dire qu'il ne reste rien pour comprendre ce que fait la fonction.

### Rappel sur les annotations

Vous avez pu trouver étrange les deux `int` placés derrière les paramètres `a` et `b` dans la ligne de définition de notre fonction, et celui placé à la fin : il s'agit d'annotations Python.
Les annotations n'ont aucune utilité à proprement parler, je veux dire par là que Python ne s'en sert pas, il se contente de les stocker.
Mais vous pouvez choisir de leur donner un sens, nous le ferons dans le TP suivant.
Une utilisation courante est de préciser dans les annotation les types des paramètres et le type de retour.

Tout ce qu'il y a à savoir pour le moment, c'est qu'une annotation peut-être n'importe quel objet Python (ici nous annotons avec l'objet `<class 'int'>`, le type entier, donc.
Les annotations sont utilisabes pour toutes fonctions et méthodes (mais pas pour les lambdas par exemple). Les paramètres peuvent être annotés en leur ajoutant un `:` suivi de l'annotation.
La fonction dans son ensemble peut-être annotée à l'aide d'un `->` derrière la liste des paramètres de la définition.

### `functools`

Revenons-en à notre problème de perte d'informations. Plus tôt dans ce cours, je vous parlais du module [`functools`](https://docs.python.org/3/library/functools.html).
Il ne nous a pas encore révélé tous ses mystères.

Nous allons dans ce chapitre nous intéresser aux fonctions `update_wrapper` et `wraps`. Ces fonctions vont nous permettre de copier les informations d'une fonction vers une nouvelle.

`update_wrapper` prend en premier paramètre la fonction à laquelle ajouter les informations et en second celle dans laquelle les puiser. Pour reprendre notre exemple précédent, il nous faudrait faire :

```python
import functools

def decorator(f):
    def decorated(*args, **kwargs):
        return f(*args, **kwargs)
    functools.update_wrappers(decorated, f) # Nous copions les informations de `f` dans `decorated`
    return decorated
```

Mais une autre fonction nous sera bien plus utile car plus concise, et recommandée par la documentation Python pour ce cas, il s'agit de `wraps`, qui retourne un décorateur lorsqu'appelé avec une fonction.

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
