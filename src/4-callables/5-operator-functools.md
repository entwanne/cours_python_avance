## Modules `operator` et `functools`

Je vais maintenant vous présenter deux modules, regroupant deux collections de *callables*.

### `operator`

Ce module regroupe l'ensemble des opérateurs python sous forme de fonctions, ainsi, une addition pour se formuler par:

```python
>>> import operator
>>> operator.add(3, 4)
7
```

Outre les opérateurs habituels, nous en trouvons d'autres sur lesquels nous allons nous intéresser plus longuement, dont la particularité est de retourner des *callables*.

#### `itemgetter`

`itemgetter` permet de récupérer un élément précis depuis un indexable, à la manière de l'opérateur `[]`.

```python
>>> get_second = operator.itemgetter(1) # Récupère le 2ème élément de l'indexable donné en paramètre
>>> get_second([5, 8, 0, 3, 1])
8
>>> get_second('abcdef')
b
>>> get_second(range(3,10))
4
>>> get_x = operator.itemgetter('x')
>>> get_name({'x': 5, 'y': 1})
5
```

#### `methodcaller`

`methodcaller` permet d'appeler une méthode prédéterminée d'un objet, avec des paramètres eux aussi déterminés:

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

### `functools`

Nous allons maintenant évoquer le module `functools`, et plus particulièrement la fonction `partial`: celle-ci permet de réaliser un appel partiel de fonction.

Imaginons que nous ayons une fonction prenant divers paramètres, mais que nous voudrions fixer le premier: l'application partielle de la fonction nous créera un nouveau *callable* qui, quand il sera appelé, nous renverra le résultat de la première fonction avec le paramètre fixé.

Nous allons la tester avec une fonction du module `operator`: la fonction de multiplication. En appliquant partiellement `5` à la fonction `operator.mul`, `partial` nous retourne une fonction réalisant la multiplication par 5 de l'objet passé en paramètre.

```python
>>> from functools import partial
>>> mul_5 = partial(operator.mul, 5)
>>> mul_5(3)
15
>>> mul_5('z')
'zzzzz'
```

Ce module comprend aussi la fonction `reduce`, un outil tiré du fonctionnel permettant de transformer un itérable en une valeur unique, en appliquant une fonction prenant un élément et le dernier résultat.

Imaginons par exemple que nous disposions d'une liste de nombres `[5, 8, 0, 3, 1]` et que nous voulions en calculer la somme. Nous savons faire la somme de deux nombres, il s'agit d'une addition, donc de la fonction `operator.add`.

`reduce` va nous permettre d'appliquer `operator.add` sur les deux premiers éléments (`5 + 8 = 13`), réappliquer la fonction avec ce premier résultat et le prochain élément de la liste (`13 + 0 = 13`), puis avec ce résultat et l'élément suivant (`13 + 3 = 16`), et enfin, sur ce résultat et le dernier élément (`16 + 1 = 17`).

Ce processus se résume en:

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
