### TP : `map`

Dans ce TP, nous allons réaliser un équivalent de la fonction `map`, que nous appellerons `my_map`.

Pour rappel, `map` permet d'appliquer une fonction sur tous les éléments d'un itérable.
Elle reçoit en paramètres la fonction à appliquer et l'itérable,
et retourne un nouvel itérable correspondant à l'application de la fonction sur chacune des valeurs de l'itérable d'entrée.

Un générateur se prête donc très bien à cet exercice : nous ferons de `my_map` une fonction génératrice.

Elle se contentera dans un premier temps d'itérer sur l'entrée, et de *yelder* le résultat obtenu pour chaque élément.

```python
def my_map(f, iterable):
    for item in iterable:
        yield f(item)
```

Cette implémentation répond très bien à la problématique initiale.

```python
>>> for x in my_map(lambda x: x*2, range(10)):
...     print(x)
...
0
2
4
6
8
10
12
14
16
18
```

Seulement, pour aller un peu plus loin et mettre en pratique ce que nous avons vu dans le chapitre, nous allons faire en sorte de pouvoir changer la fonction `f` en cours de route.

Pour ce faire, nous communiquerons avec notre générateur à l'aide de sa méthode `send`.
Nous voulons donc que chaque fois que `yield` retourne autre chose que `None`, cette valeur soit utilisée comme nouvelle fonction.

Une approche simpliste serait la suivante :

```python
def my_map(f, iterable):
    for item in iterable:
        ret = yield f(item)
        if ret is not None:
            f = ret
```

Mais comme `send` provoque une itération supplémentaire du générateur, elle a l'inconvénient de faire perdre des valeurs.
(les valeurs ne sont pas vraiment perdues, mais sont les valeurs de retour de `send`)

```python
>>> gen = my_map(lambda x: x+1, range(10))
>>> for x in gen:
...     print('Got', x)
...     if x == 5:
...         gen.send(lambda x: x+2)
...
Got 1
Got 2
Got 3
Got 4
Got 5
7
Got 8
Got 9
Got 10
Got 11
```

L'affichage du `7` étant dû à l'interpréteur interactif qui affiche la valeur de retour du `send`.

Pour palier à ce petit problème, nous pouvons dans notre générateur *yielder* `None` quand une fonction a été reçue.
Ainsi, le retour du `send` sera le `None` transmis par `yield`, et la valeur ne sera pas perdue.

Nous réécrivons alors notre générateur en conséquence.

```python
def my_map(f, iterable):
    for item in iterable:
        ret = yield f(item)
        if ret is not None:
            f = ret
            yield None
```

Et observons la correction.

```python
>>> gen = my_map(lambda x: x+1, range(10))
>>> for x in gen:
...     print('Got', x)
...     if x == 5:
...         gen.send(lambda x: x+2)
...
Got 1
Got 2
Got 3
Got 4
Got 5
Got 7
Got 8
Got 9
Got 10
Got 11
```

Mais notre générateur reste sujet à un problème plus subtil : des pertes se produisent si nous appelons `yield` plusieurs fois d'affilée.

```python
>>> gen = my_map(lambda x: x+1, range(10))
>>> for x in gen:
...     print('Got', x)
...     if x == 5:
...         gen.send(lambda x: x+2)
...         gen.send(lambda x: x*2)
...
Got 1
Got 2
Got 3
Got 4
Got 5
7
Got 8
Got 9
Got 10
Got 11
```

En effet, lors du premier `send`, nous retrons dans la condition du générateur pour arriver sur le `yield None`, valeur retournée par `send`.
Mais nous ne nous inquiétons pas de savoir ce que retourne ce second `yield` (en l'occurrence, la fonction envoyée par le second `send`, qui n'est jamais prise en compte).

Vous l'aurez compris, il nous suffira donc de mettre en place une boucle autour du `yield None` et n'en sortir qu'une fois qu'il aura retourné `None`.
Chaque valeur différente sera enregistrée comme nouvelle fonction `f`.

```python
def my_map(f, iterable):
    for value in iterable:
        newf = yield f(value)
        while newf is not None:
            f = newf
            newf = yield None
```

Cette fois-ci, plus de problèmes !

```python
>>> gen = my_map(lambda x: x+1, range(10))
>>> for x in gen:
...     print('Got', x)
...     if x == 5:
...         gen.send(lambda x: x+2)
...         gen.send(lambda x: x*2)
...
Got 1
Got 2
Got 3
Got 4
Got 5
Got 10
Got 12
Got 14
Got 16
Got 18
```
