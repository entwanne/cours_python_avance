### Modules `operator` et `functools`

Passons maintenant à la présentation de deux modules, contenant deux collections de *callables*.

#### `operator`

Ce premier module, [`operator`](https://docs.python.org/3/library/operator.html) regroupe l'ensemble des opérateurs Python sous forme de fonctions.
Ainsi, une addition pourrait se formuler par :

```python
>>> import operator
>>> operator.add(3, 4)
7
```

Outre les opérateurs habituels, nous en trouvons d'autres sur lesquels nous allons nous intéresser plus longuement, dont la particularité est de retourner des *callables*.

##### `itemgetter`

`itemgetter` permet de récupérer un élément précis depuis un indexable, à la manière de l'opérateur `[]`.

```python
>>> get_second = operator.itemgetter(1) # Récupère le 2ème élément de l'indexable donné en argument
>>> get_second([5, 8, 0, 3, 1])
8
>>> get_second('abcdef')
b
>>> get_second(range(3,10))
4
>>> get_x = operator.itemgetter('x')
>>> get_x({'x': 5, 'y': 1})
5
```

##### `methodcaller`

`methodcaller` permet d'appeler une méthode prédéterminée d'un objet, avec ses arguments.

```python
>>> dash_spliter = operator.methodcaller('split', '-')
>>> dash_spliter('a-b-c-d')
['a', 'b', 'c', 'd']
>>> append_b = operator.methodcaller('append', 'b')
>>> l = [0, 'a', 4]
>>> append_b(l)
>>> l
[0, 'a', 4, 'b']
```

#### `functools`

Je tenais ensuite à évoquer le module [`functools`](https://docs.python.org/3/library/functools.html), et plus particulièrement la fonction `partial` : celle-ci permet de réaliser un appel partiel de fonction.

Imaginons que nous ayons une fonction prenant divers paramètres, mais que nous voudrions fixer le premier : l'application partielle de la fonction nous créera un nouveau *callable* qui, quand il sera appelé avec de nouveaux arguments, nous renverra le résultat de la première fonction avec l'ensemble des arguments.

Par exemple, prenons une fonction de journalisation `log` prenant quatre paramètres, un niveau de gravité, un type, un object, et un message descriptif :

```python
def log(level, type, item, message):
    print('[{}]<{}>({}): {}'.format(level.upper(), type, item, message))
```

Une application partielle reviendrait à avoir une fonction `warning` tel que chaque appel `warning('foo', 'bar', 'baz')` équivaudrait à `log('warning', 'foo', 'bar', 'baz')`.
Ou encore une fonction `warning_foo` avec `warning_foo('bar', 'baz')` équivalent à l'appel précédent.

Nous allons la tester avec une fonction du module `operator` : la fonction de multiplication. En appliquant partiellement `5` à la fonction `operator.mul`, `partial` nous retourne une fonction réalisant la multiplication par 5 de l'objet passé en paramètre.

```python
>>> from functools import partial
>>> mul_5 = partial(operator.mul, 5)
>>> mul_5(3)
15
>>> mul_5('z')
'zzzzz'
>>> warning = partial(log, 'warning')
>>> warning('overflow', 100, 'number is too large')
[WARNING]<overflow>(100): number is too large
>>> overflow = partial(log, 'warning', 'overflow')
>>> overflow(-1, 'number is too low')
[WARNING]<overflow>(-1): number is too low
```

Le module `functools` comprend aussi la fonction `reduce`, un outil tiré du fonctionnel permettant de transformer un itérable en une valeur unique.
Pour cela, elle itère sur l'ensemble et applique une fonction à chaque valeur, en lui précisant la valeur courante et le résultat précédent.

Imaginons par exemple que nous disposions d'une liste de nombres `[5, 8, 0, 3, 1]` et que nous voulions en calculer la somme. Nous savons faire la somme de deux nombres, il s'agit d'une addition, donc de la fonction `operator.add`.

`reduce` va nous permettre d'appliquer `operator.add` sur les deux premiers éléments (`5 + 8 = 13`), réappliquer la fonction avec ce premier résultat et le prochain élément de la liste (`13 + 0 = 13`), puis avec ce résultat et l'élément suivant (`13 + 3 = 16`), et enfin, sur ce résultat et le dernier élément (`16 + 1 = 17`).

Ce processus se résume en :

```python
>>> from functools import reduce
>>> reduce(operator.add, [5, 8, 0, 3, 1])
17
```

qui revient donc à faire

```python
>>> operator.add(operator.add(operator.add(operator.add(5, 8), 0), 3), 1)
17
```

Bien sûr, en pratique, `sum` est déjà là pour répondre à ce problème.
