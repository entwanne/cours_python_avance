## `for` `for` lointain

Les itérables et le mot-clef `for` sont intimement liées. C'est à partir de ce dernier que nous itérons sur les objets.

Vous connaissez probablement déjà de nombreux itérables: les `str`, les `tuple`, les `list`, les `dict` et les `set` sont sans doute les plus courants.

Mais comment cela fonctionne-t-il en interne ? Je vous propose de regarder ça pas à pas, en nous aidant d'un objet de type `list`.

```python
>>> numbers = [1, 2, 3, 4, 5]
```

La première opération réalisée par le `for` est d'appeler la fonction `iter` sur l'objet:

```python
>>> iter(numbers)
<list_iterator object at 0x7f26896c0940>
```

Puis, pas à pas, le `for` appelle `next` en lui précisant l'itérateur:

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

Qu'est-ce que ce `StopIteration` ? Il s'agit d'une exception, levée par l'itérateur quand il arrive à sa fin, qui signifie que nous en sommes arrivés au bout, et donc que la boucle doit cesser. `for` attrape cette exception pour nous, ce qui explique que nous ne la voyons pas survenir lors d'une boucle habituelle.

Ainsi, le code suivant:

```python
for number in numbers:
    print(number)
```

Peut se remplacer par celui-ci:

```python
iterator = iter(numbers)
while True:
    try:
        number = next(iterator)
    except StopIteration:
        break
    print(number)
```

En interne, `iter` fait appel à la méthode `__iter__` de l'objet, et `next` à la méthode `__next__` de l'itérateur. Ces deux méthodes ne prennent aucun paramètre.

- Un itérable est donc un objet possédant une méthode `__iter__` retournant un itérateur.
- Un itérateur est donc un objet possédant une méthode `__next__` retournant la valeur suivante à chaque appel, et levant une exception de type `StopIteration` en fin de course.
