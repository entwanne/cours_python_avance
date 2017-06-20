### Altérer un générateur avec `send`

Maintenant que nous savons créer des générateurs, nous allons voir qu'il est possible de communiquer avec eux après leur création.

Pour cela, les générateurs sont dotés d'une méthode `send`. Le paramètre reçu par cette méthode sera transmis au générateur.
Mais comment le reçoit-il ?

Au moment où il arrive sur une instruction `yield`, le générateur se met en pause. Lors de l'itération suivante, l'exécution reprend au niveau de ce même `yield`.
Quand ensuite vous appelez la méthode `send` du générateur, en lui précisant un argument, l'exécution reprend ; et `yield` retourne la valeur passée à `send`.

Attention donc, un appel à `send` produit une itération supplémentaire dans le générateur. `send` retourne alors la valeur de la prochaine itération comme le ferait `next`.

```python
>>> gen = fibonacci(10)
>>> next(gen)
0
>>> next(gen)
1
>>> gen.send('test') # Le send consomme une itération
1
>>> next(gen)
2
```

Comme je le disais, une valeur peut-être retournée par l'instruction `yield`, c'est-à-dire dans le corps même de la fonction génératrice.
Modifions quelque peu notre générateur `fibonacci` pour nous en apercevoir.

```python
>>> def fibonacci(n, a=0, b=1):
...     for _ in range(n):
...         ret = yield a
...         print('retour:', ret)
...         a, b = b, a + b
...
>>> gen = fibonacci(10)
>>> next(gen)
0
>>> next(gen)
retour: None
1
>>> gen.send('test')
retour: test
1
>>> next(gen)
retour: None
2
```

Nous pouvons voir que lors de notre premier `next`, aucun retour n'est imprimé : c'est normal, le générateur n'étant encore jamais passé dans un `yield`, nous ne sommes pas encore arrivés jusqu'au premier appel à `print` (qui se trouve après le premier `yield`).

Cela signifie aussi qu'il est impossible d'utiliser `send` avant le premier `yield` (puisqu'il n'existe aucun précédent `yield` qui retournerait la valeur).

```python
>>> gen = fibonacci(10)
>>> gen.send('test')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: can´t send non-None value to a just-started generator
```

Pour comprendre un peu mieux l'intérêt de `send`, nous allons implémenter une file (*queue*) par l'intermédiaire d'un générateur. Celle-ci sera construite à l'aide des arguments donnés  à l'appel, retournera le premier élément à chaque itération (en le retirant de la file).
On pourra aussi ajouter de nouveaux éléments à cette *queue* *via* `send`.

```python
def queue(*args):
    elems = list(args)
    while elems:
        new = yield elems.pop(0)
        if new is not None:
            elems.append(new)
```

Testons un peu pour voir.

```python
>>> q = queue('a', 'b', 'c')
>>> next(q)
'a'
>>> q.send('d')
'b'
>>> next(q)
'c'
>>> next(q)
'd'
```

Et si nous souhaitons itérer sur notre file :

```python
>>> q = queue('a', 'b', 'c')
>>> for letter in q:
...     if letter == 'a':
...         q.send('d')
...     print(letter)
...
'b'
a
c
d
```

Que se passe-t-il ? En fait, `send` consommant une itération, le `b` n'est pas obtenu via le `for`, mais en retour de `send`, et directement imprimé sur la sortie de l'interpréteur (avant même le `print` de `a` puisque le `send` est fait avant).

Nous pouvons assigner le retour de `q.send` afin d'éviter que l'interpréteur n'en imprime le résultat, mais cela ne changerait pas tellement le problème : nous ne tomberons jamais sur `'b'` dans nos itérations du `for`.

Pour obtenir le comportement attendu, nous pourrions avancer dans les itérations uniquement si le dernier `yield` a renvoyé `None` (un `yield` renvoyant `None` étant considéré comme un `next`).
Comment faire cela ? Par une boucle qui exécute `yield` jusqu'à ce qu'il retourne `None`. Ce `yield` n'aura pas de paramètre spécifique, cette valeur étant celle retournée ensuite par `send`, elle ne nous intéresse pas ici.

Ainsi, les `send` ne consommeront qu'une itération de la sous-boucle, tandis que les « vraies » itérations seront réservées aux `next`.

```python
def queue(*args):
    elems = list(args)
    while elems:
        new = yield elems.pop(0)
        while new is not None:
            elems.append(new)
            new = yield
```

```python
>>> q = queue('a', 'b', 'c')
>>> for letter in q:
...     if letter == 'a':
...         q.send('d')
...     print(letter)
...
a
b
c
d
```
