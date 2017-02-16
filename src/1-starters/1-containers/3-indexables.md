### Objets *indexables*

Nous voilà bien avancés, nous savons mesurer la taille d'un objet, mais *quid* des éléments ?

L'accès aux éléments se fait via l'opérateur `[]`. De même que la modification et la suppression, quand celles-ci sont possibles (c'est-à-dire que l'objet est mutable).

```python
>>> numbers = [4, 7, 6]
>>> numbers[2]
6
>>> numbers[1] = 5
>>> numbers
[4, 5, 6]
>>> del numbers[0]
>>> numbers
[5, 6]
```

Le comportement interne est ici régi par 3 méthodes : `__getitem__`, `__setitem__`, et `__delitem__`.

```python
>>> numbers = [4, 7, 6]
>>> numbers.__getitem__(2)
6
>>> numbers.__setitem__(1, 5)
>>> numbers
[4, 5, 6]
>>> numbers.__delitem__(0)
>>> numbers
[5, 6]
```

Comme précédemment, nous pouvons donc implémenter ces méthodes dans un nouveau type. Nous allons ici nous contenter de faire un proxy autour d'une liste existante.

Un proxy[^proxy] est un objet prévu pour se substituer à un autre, il doit donc répondre aux mêmes méthodes, de façon transparente.

[^proxy]: <https://fr.wikipedia.org/wiki/Proxy_(patron_de_conception)>

```python
class MyList:
    def __init__(self, value=()): # Émulation du constructeur de list
        self.internal = list(value)
    def __len__(self): # Sera utile pour les tests
        return len(self.internal)
    def __getitem__(self, key):
        return self.internal[key] # Équivalent à return self.internal.__getitem__(key)
    def __setitem__(self, key, value):
        self.internal[key] = value
    def __delitem__(self, key):
        del self.internal[key]
```

Nous pouvons tester notre objet, celui-ci a bien le comportement voulu :

```python
>>> numbers = MyList('123456')
>>> len(numbers)
6
>>> numbers[1]
'2'
>>> numbers[1] = '0'
>>> numbers[1]
'0'
>>> del numbers[1]
>>> len(numbers)
5
>>> numbers[1]
'3'
```
