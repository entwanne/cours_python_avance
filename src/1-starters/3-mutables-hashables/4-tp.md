### TP : Égalité entre listes

Nous allons maintenant nous intéresser à l'implémentation de l'opérateur d'égalité entre listes.
Nos listes, mutables, deviendront par conséquent non-hashables.
Nous reviendrons vers la fin de ce cours sur l'implémentation de listes immutables.

L'opérateur d'égalité correspond donc à la méthode spéciale `__eq__`, recevant en paramètre l'objet auquel `self` est comparé.
La méthode retourne ensuite `True` si les objets sont égaux, `False` s'ils sont différents, et `NotImplemented` si la comparaison ne peut être faite.

`NotImplemented` est une facilité de Python pour gérer les opérateurs binaires.
En effet, dans une égalité `a == b` par exemple, on ne peut pas savoir lequel de `a` ou `b` redéfinit la méthode `__eq__`.
L'interpréteur va alors tester en premier d'appeler la méthode de `a` :

* Si la méthode retourne `True`, les objets sont égaux ;
* Si elle retourne `False`, ils sont différents ;
* Si elle retourne `NotImplemented`, alors l'interpréteur appellera la méthode `__eq__` de `b` pour déterminer le résultat ;
* Si les deux méthodes retournent `NotImplemented`, les objets sont différents.

Dans notre méthode, nous allons donc premièrement vérifier le type du paramètre.
S'il n'est pas du type attendu (`Deque`), nous retournerons `NotImplemented`.

Nous comparerons ensuite la taille des listes, si la taille diffère, les listes sont nécessairement différentes.
Dans l'idéal, nous devrions éviter cette comparaison car elle est coûteuse (elle nécessite de parcourir entièrement chacune des listes), mais nous pouvons la conserver dans le cadre de l'exercice.

Enfin, nous itérerons simultanément sur nos deux listes pour vérifier que tous les éléments sont égaux.

```python
def __eq__(self, other):
    if not isinstance(other, Deque):
        return NotImplemented
    if len(self) != len(other):
        return False
    for elem1, elem2 in zip(self, other):
        if elem1 != elem2:
            return False
    return True
```

C'est l'heure du test !

```python
>>> d = Deque([0, 1])
>>> d == Deque([0, 1])
True
>>> d == Deque([0, 1, 2])
False
>>> d == Deque([1, 2])
False
>>> d == 0
False
>>> d.append(2)
>>> d == Deque([0, 1])
False
>>> d == Deque([0, 1, 2])
True
```

Et comme nous pouvons le constater, notre `Deque` a perdu son pouvoir d'hashabilité.

```python
>>> hash(d)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: unhashable type: 'Deque'
```
