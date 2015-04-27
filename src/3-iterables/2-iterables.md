## Utilisation des iterables

### Python et les itérables

Ce concept d'itérateurs est utilisé par Python dans une grande liste des ses [builtins](https://docs.python.org/3/library/functions.html). Plutôt que de vous forcer à utiliser une liste, Python vous permet de fournir un objet itérable, pour `sum`, `max` ou `map` par exemple.

Je vous propose de tester cela avec un itérable basique, qui nous permettra de réaliser un `range` simplifié.

```python
class MyRange:
    def __init__(self, size):
        self.size = size

    def __iter__(self):
        return MyRangeIterator(self)

class MyRangeIterator:
    def __init__(self, my_range):
        self.current = 0
        self.max = my_range.size

    def __next__(self):
        if self.current >= self.max:
            raise StopIteration
        ret = self.current
        self.current += 1
        return ret
```

Maintenant, testons notre objet, et premièrement d'itérer dessus à l'aide d'un `for`:

```python
>>> MyRange(5)
<__main__.MyRange object at 0x7fcf3b0e8f28>
>>> for i in MyRange(5):
...     print(i)
... 
0
1
2
3
4
```

Voilà pour l'itération, mais maintenant, testons quelques autres *builtins* dont je parlais plus haut:

```python
>>> sum(MyRange(5)) # sum réalise la somme de tous les éléments, soit 0 + 1 + 2 + 3 + 4
10
>>> max(MyRange(5)) # max retour la plus grande valeur
4
>>> map(str, MyRange(5)) # Ici, map retournera chaque valeur convertie en str
<map object at 0x7f8b81226cf8>
```

Mmmh, que s'est-il passé ? En fait, `map` ne retourne pas une liste, mais un nouvel itérateur. Si nous voulons en voir le contenu, nous pouvons itérer dessus… ou plus simplement, convertir le résultat en liste:

```python
>>> list(map(str, MyRange(5))
['0', '1', '2', '3', '4']
```

Vous l'aurez compris, `list` prend aussi n'importe quel itérateur, tout comme `zip` ou `str.join` par exemple.

```python
>>> list(MyRange(5))
[0, 1, 2, 3, 4]
>>> list(zip(MyRange(5), 'abcde')) # Les chaînes sont aussi des itérables
[(0, 'a'), (1, 'b'), (2, 'c'), (3, 'd'), (4, 'e')]
>>> ', '.join(map(str, MyRange(5)))
'0, 1, 2, 3, 4'
```

J'en resterai là pour les exemples, sachez seulement que beaucoup de fonctions sont compatibles. Seules celles nécessitant des propriétés spécifiques de l'objet ne le seront pas par défaut, comme la fonction `reversed`.

### Retour sur `iter`

Nous avons vu dans la section précédente la fonction `iter`, qui crée un itérateur à partir d'un itérable. Sachez que ce n'est pas sa seule utilité: elle peut aussi créer un itérateur à partir d'une fonction et d'une valeur de fin: c'est à dire que la fonction sera appelée tant que la valeur de fin n'a pas été retournée, par exemple:

```python
>>> n = 0
>>> def iter_func():
...     global n
...     n += 1
...     return n
... 
>>> for i in iter(iter_func, 10):
...     print(i)
... 
1
2
3
4
5
6
7
8
9
```
