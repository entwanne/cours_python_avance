### Annotations

Commençons par les annotations.
Il se peut que vous ne les ayez jamais rencontrées, il s'agit d'une fonctionnalité relativement nouvelle du langage.

Les annotations sont des informations de types que l'on peut ajouter sur les paramètres et le retour d'une fonction.

Prenons une fonction d'addition entre deux nombres.

```python
def addition(a, b):
    return a + b
```

Nous avons destiné cette fonction à des calculs numériques, mais nous pourrions aussi l'appeler avec des chaînes de caractères.
Les annotations vont nous permettre de préciser le type des paramètres attendus, et le type de la valeur de retour.

```python
def addition(a: int, b: int) -> int:
    return a + b
```

Leur définition est assez simple : pour annoter un paramètre, on le fait suivre d'un `:` et on ajoute le type attendu.
Pour annoter le retour de la fonction, on ajoute `->` puis le type derrière la liste des paramètres.

Attention cependant, les annotations ne sont là qu'à titre indicatif.
Rien n'empêche de continuer à appeler notre fonction avec des chaînes de caractères.

À ce titre, on notera aussi que donner des types comme annotations n'est qu'une convention.
Annoter des paramètres avec des chaînes de caractères ne provoquera pas d'erreur par exemple.

#### Utilité des annotations

Si elles ne sont là qu'à titre indicatif, les annotations sont surtout utiles dans un but de documentation.
Elles sont le meilleur moyen en Python de documenter les types des paramètres et de retour d'une fonction.

Elles apparaissent d'ailleurs dans l'aide de la fonction fournie par `help`.

```python
>>> help(addition)
Help on function addition in module __main__:

addition(a:int, b:int) -> int
```

Les annotations ne sont pas censées avoir d'autre utilité lors de l'exécution d'un programme Python.
Elles ne sont pas destinées à vérifier au *runtime* le type des paramètres par exemple.
La définitition d'annotations ne doit normalement rien changer sur le déroulement du programme.

Toutefois, les annotations ont l'utilité que l'on veut bien leur donner.
Il existe des outils d'analyse statique tels que `mypy` qui peuvent en tirer partie.
Ces outils n'exécutent pas le code, mais se contentent de vérifier que les types utilisés n'entrent pas en conflit avec les annotations.

#### Des types plus complexes (module `typing`)

Nous avons défini une fonction addition opérant sur deux nombres, mais l'avons annotée comme ne pouvant recevoir que des nombres entiers (`int`).

En effet, les annotations utilisées jusqu'ici étaient plutôt simples.
Mais elles peuvent accueillir des expressions plus complexes.

Le [module `typing`](https://docs.python.org/3/library/typing.html) nous présente une collection de classes pour composer des types.
Ce module a été introduit dans Python 3.5, et n'est donc pas disponible dans les versions précédentes du langage.

Dans notre fonction `addition`, nous voudrions en fait que les `int`, `float` et `complex` soient admis.
Nous pouvons pour cela utiliser le type `Union` du module `typing`.
Il nous permet de définir un ensemble de types valides pour nos paramètres, et s'utilise comme suit.

```python
Number = Union[int, float, complex]

def addition(a: Number, b: Number) -> Number:
    return a + b
```

Nous définissons premièrement un type `Number` comme l'ensemble des types `int`, `float` et `complex` *via* la syntaxe `Union[...]`.
Puis nous utilisons notre nouveau type `Number` au sein de nos annotations.

Outre `Union`, le module `typing` présente d'autres types génériques pour avoir des annotations plus précises.
Nous pourrions avoir, par exemple :

* `List[str]` -- Une liste de chaînes de caractères ;
* `Sequence[str]` -- Une séquence (liste/*tuple*/etc.) de chaînes de caractères ;
* `Callable[[str, int], str]` -- Un *callable* prenant deux paramètres de types `str` et `int` respectivement, et retournant un objet `str` ;
* Et bien d'autres à découvrir dans la [documentation du module](https://docs.python.org/3/library/typing.html).

Attention encore, le module `typing` ne doit servir que dans le cadre des annotations.
Les types fournis par ce module ne doivent pas être utilisées au sein d'expressions avec `isinstance` ou `issubclass`.

Dans le cas précis de notre fonction `addition`, nous aurions aussi pu utiliser le type `Number` du [module `numbers`](https://docs.python.org/3/library/numbers.html).
Nous y reviendrons plus tard dans ce cours, mais il s'agit d'un type qui regroupe et hiérarchise tous les types numériques.

#### Annotations de variables

Les annotations sont ici abodées sous l'angle des fonctions et de leurs paramètres.
Mais il est à noter que depuis Python 3.6, il est aussi possible d'annoter les variables et attributs.

La syntaxe est la même que pour les paramètres de fonction.
Encore une fois, les annotations sont là à titre indicatif, et pour les analyseurs statiques.
Elles sont toutefois stockées dans le dictionnaire `__annotations__` du module ou de la classe qui les contient.

```python
max_value : int = 10 # Définition d'une variable max_value annotée comme int
min_value : int      # Annotation seule, la variable n'est pas définie dans ce cas
```

Un petit coup d'œil à la variable `__annotations__` et aux variables annotées.

```python
>>> __annotations__
{'max_value': <class 'int'>, 'min_value': <class 'int'>}
>>> max_value
10
>>> min_value
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
NameError: name 'min_value' is not defined
```
