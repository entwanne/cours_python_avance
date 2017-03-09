### `for` `for` lointain

Les itérables et le mot-clef `for` sont intimement liés. C'est à partir de ce dernier que nous itérons sur les objets.

Mais comment cela fonctionne en interne ? Je vous propose de regarder ça pas à pas, en nous aidant d'un objet de type `list`.

```python
>>> numbers = [1, 2, 3, 4, 5]
```

La première opération réalisée par le `for` est d'appeler la fonction `iter` avec notre objet.
`iter` retourne un itérateur. L'itérateur est l'objet qui va se déplacer le long de l'itérable.

```python
>>> iter(numbers)
<list_iterator object at 0x7f26896c0940>
```

Puis, pas à pas, le `for` appelle `next` en lui précisant l'itérateur :

```python
>>> iterator = iter(numbers)
>>> next(iterator)
1
>>> next(iterator)
2
>>> next(iterator)
3
>>> next(iterator)
4
>>> next(iterator)
5
>>> next(iterator)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
StopIteration
```

Qu'est-ce que ce `StopIteration` ? Il s'agit d'une exception, levée par l'itérateur quand il arrive à sa fin, qui signifie que nous en sommes arrivés au bout, et donc que la boucle doit cesser. `for` attrape cette exception pour nous, ce qui explique que nous ne la voyons pas survenir dans une boucle habituelle.

Ainsi, le code suivant :

```python
for number in numbers:
    print(number)
```

Peut se remplacer par celui-ci :

```python
iterator = iter(numbers)
while True:
    try:
        number = next(iterator)
    except StopIteration:
        break
    print(number)
```

En interne, `iter` fait appel à la méthode `__iter__` de l'itérable, et `next` à la méthode `__next__` de l'itérateur. Ces deux méthodes ne prennent aucun paramètre. Ainsi :

- Un itérable est un objet possédant une méthode `__iter__` retournant un itérateur ;
- Un itérateur est un objet possédant une méthode `__next__` retournant la valeur suivante à chaque appel, et levant une exception de type `StopIteration` en fin de course.

La [documentation Python](https://docs.python.org/3/glossary.html#term-iterator) indique aussi qu'un itérateur doit avoir une méthode `__iter__` où il se retourne lui-même, les itérateurs étant ainsi des itérables à part entièe.


#### Le cas des indexables

En début du chapitre, j'ai indiqué que notre liste `Deque` était aussi un itérable. Pourtant, nous ne lui avons pas implémenté de méthode `__iter__` permettant de la parcourir.

Il s'agit en fait d'une particularité des indexables, et de la fonction `iter` qui est capable de créer un itérateur à partir de ces derniers.
Cet itérateur se contentera d'appeler `__getitem__` sur notre objet avec des indices successifs, partant de 0 et continuant jusqu'à ce que la méthode lève une `IndexError`.

Dans notre cas, ça nous évite donc d'implémenter nous-même `__iter__`, mais ça complexifie aussi les traitements. Souvenez-vous de notre méthode `__getitem__` : elle parcourt la liste jusqu'à l'élément voulu.
Ainsi, pour accéder au premier maillon, on parcourt un élément, on en parcourt deux pour accéder au second, etc.
Donc pour itérer sur une liste de 5 éléments, on va devoir parcourir `1 + 2 + 3 + 4 + 5` soit 15 maillons, là où 5 seraient suffisants.
C'est pourquoi nous reviendrons sur `Deque` en fin de chapitre pour lui intégrer sa propre méthode `__iter__`.
