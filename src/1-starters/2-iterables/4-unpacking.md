### L'*unpacking*

Une fonctionnalité courante de Python, liée aux itérables, est celle de 'l*unpacking*.
Il s'agit de l'opération qui permet de décomposer un itérable en plusieurs variables.

Prenons `values` une liste de 3 valeurs, il est possible en une ligne d'assigner chaque valeur à une variable différente.

```python
>>> values = [1, 3, 5]
>>> a, b, c = values
>>> a
1
>>> b
3
>>> c
5
```

J'utilise ici une liste `values`, mais tout type d'itérable est accepté, on pourrait avoir un `range` ou un `set` par exemple.
L'itérable n'a pas besoin d'être une séquence comme la liste.

```python
>>> a, b, c = range(1, 6, 2)
>>> a, b, c = {1, 3, 5} # l'ordre n'est pas assuré dans ce dernier cas
```

C'est aussi cette fonctionnalité qui est à l'origine de l'assignement multiple et de l'échange de variables.

```python
>>> x, y = 10, 20
>>> x
10
>>> y
20
>>> x, y = y, x
>>> x
20
>>> y
10
```

En effet, nous avons dans ces deux cas, à gauche comme à droite du signe `=`, des *tuples*.
Et celui de droite est décomposé pour correspondre aux variables de gauche.

Je parle de *tuples*, mais on retrouve la même chose avec des listes.
Les assignations suivantes sont d'ailleurs équivalentes.

```python
>>> x, y = 10, 20
>>> (x, y) = (10, 20)
>>> [x, y] = [10, 20]
```

#### Structures imbriquées

Les cas d'*unpacking* sont les plus simples : nous avons un itérable à droite et un ensemble « plat » de variables à gauche.
Je dis « plat » parce qu'il n'y a qu'un niveau.

Mais il est possible de faire bien plus que cela, en décomposant aussi des itérables imbriqués les uns dans les autres.

```python
>>> a, ((b, c, d), e), (f, g) = [0, (range(1, 4), 5), '67']
>>> a
0
>>> b
1
>>> c
2
>>> d
3
>>> e
5
>>> f
'6'
>>> g
'7'
```

#### Opérateur *splat*

Mais on peut aller encore plus loin avec l'opérateur *splat*.
Cet opérateur est représenté par le caractère `*`.

À ne pas confondre avec la multiplication, opérateur binaire entre deux objets, il s'agit ici d'un opérateur unaire : c'est à dire qu'il n'opère que sur un objet, en se plaçant devant.

Utilisé à gauche lors d'une assignation, il permet de récupérer plusieurs éléments lors d'une décomposition.

```python
>>> head, *tail = range(10)
>>> head
0
>>> tail
[1, 2, 3, 4, 5, 6, 7, 8, 9]
>>> head, *middle, last = range(10)
>>> head
0
>>> middle
[1, 2, 3, 4, 5, 6, 7, 8]
>>> last
9
>>> head, second, *middle, last = range(10)
>>> head
0
>>> second
1
>>> middle
[2, 3, 4, 5, 6, 7, 8]
>>> last
9
```

Vous l'avez compris, la variable précédée du *splat* devient une liste, dont la taille s'ajuste en fonction du nombre d'éléments.

Il est donc impossible d'avoir deux variables précédées d'un *splat*, cela mènerait à une ambigüité.
Ou plutôt, devrais-je préciser, un seul par niveau d'imbrication.

```python
>>> *a, (b, *c) = (0, 1, 2, (3, 4, 5))
>>> a
[0, 1, 2]
>>> b
3
>>> c
[4, 5]
```

#### Encore du *splat*

Nous avons vu l'opérateur *splat* utilisé à gauche de l'assignation, mais il est aussi possible depuis Python 3.5 de l'utiliser à droite.
Il aura simplement l'effet inverse, et décomposera un itérable comme si ses valeurs avaient été entrées une à une.

```python
>>> values = *[0, 1, 2], 3, 4, *[5, 6], 7
>>> values
(0, 1, 2, 3, 4, 5, 6, 7)
```

Il est bien sûr possible de combiner les deux.

```python
>>> first, *middle, last = *[0, 1, 2], 3, 4, *[5, 6], 7
>>> first
0
>>> middle
[1, 2, 3, 4, 5, 6]
>>> last
7
```

Pour plus d'informations sur les possibilités étendues de l'opérateur *splat* offertes par Python 3.5 : <https://zestedesavoir.com/articles/175/sortie-de-python-3-5/#2-principales-nouveautes>
