### TP : Itérateur sur listes chaînées

Revenons sur nos listes chaînées afin d'y implémenter le protocole des itérables.
Notre classe `Deque` a donc besoin d'une méthode `__iter__` retournant un itérateur, que nous appellerons simplement `DequeIterator`.

```python
def __iter__(self):
    return DequeIterator(self)
```

Cet itérateur contiendra une référence vers un maillon, puis, à chaque appel à `__next__`, renverra la valeur du maillon courant, tout en prenant soin de passer au maillon suivant pour le prochain appel. `StopIteration` sera levée si le maillon courant vaut `None`.

On ajoutera aussi `__iter__` dans l'itérateur, comme vu plus tôt, dans le cas où cet itérateur serait utilisé comme itérable.

```python
class DequeIterator:
    def __init__(self, deque):
        self.current = deque.first

    def __next__(self):
        if self.current is None:
            raise StopIteration
        value = self.current.value
        self.current = self.current.next
        return value

    def __iter__(self):
        return self
```

Testons maintenant notre implémentation…

```python
>>> for i in Deque([1, 2, 3, 4, 5]):
...     print(i)
...
1
2
3
4
5
```

… Ça marche !
