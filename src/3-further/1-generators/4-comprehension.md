### Listes et générateurs en intension

#### Listes en intension

Vous connaissez probablement déjà les listes en intension (*comprehension lists*), mais je vais me permettre un petit rappel.

Les listes en intension sont une syntaxe courte pour définir des listes à partir d'un itérable et d'une expression à appliquer sur chaque élément (un peu à la manière de `map`, qui lui ne permet que d'appeler un *callable* pour chaque l'élément).

Une expression étant en Python tout ce qui possède une valeur (même `None`), c'est à dire ce qui n'est pas une instruction (`if`, `while`, etc.).
Il faut noter que les ternaires sont des expressions (`a if predicat() else b`), et peuvent donc y être utilisés.

Ainsi,

```python
>>> squares = [x**2 for x in range(10)]
>>> squares
[0, 1, 4, 9, 16, 25, 36, 49, 64, 81]
```

sera l'équivalent de

```python
squares = []
for x in range(10):
    squres.append(x**2)
```

ou encore de

```python
squares = list(map(lambda x: x**2, range(10)))
```

Le gain en lisibilité est net.

Cette syntaxe permet aussi d'appliquer des filtres, à la manière de `filter`. Par exemple si nous ne voulions que les carrés supérieurs à 10 :

```python
>>> [x**2 for x in range(10) if x**2 >= 10]
[16, 25, 36, 49, 64, 81]
```

Une liste en intension peut directement être passée en paramètre à une fonction.

```python
>>> sum([x**2 for x in range(10)])
285
```

Étant des expressions, elles peuvent être imbriquées dans d'autres listes en intension :

```python
>>> [[x + y for x in range(5)] for y in range(3)]
[[0, 1, 2, 3, 4], [1, 2, 3, 4, 5], [2, 3, 4, 5, 6]]
```

Enfin, il est possible de parcourir plusieurs niveaux de listes dans une seule liste en intension :

```python
>>> matrix = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
>>> [elem + 1 for line in matrix for elem in line]
[1, 2, 3, 4, 5, 6, 7, 8, 9]
```

Vous noterez que les `for` se placent dans l'ordre des dimensions que nous voulons explorer : d'abord les lignes, puis les éléments qu'elles contiennent.

#### Générateurs en intension

De la même manière que pour les listes, nous pouvons définir des générateurs en intension (*generator expressions*) :

```python
>>> squares = (x**2 for x in range(10))
>>> squares
<generator object <genexpr> at 0x7f8b8a9a7090>
```

Et nous pouvons les utiliser tel que les autres itérables.

```python
>>> list(squares)
[0, 1, 4, 9, 16, 25, 36, 49, 64, 81]
>>> list(squares) # En gardant à l'esprit qu'ils se consumment
[]
```

Et pour finir, il est possible de simplifier encore la syntaxe quand un générateur en intension est seul paramètre d'une fonction :

```python
>>> sum((x**2 for x in range(10)))
285
>>> sum(x**2 for x in range(10)) # Une paire de parenthèses est retirée
285
```
