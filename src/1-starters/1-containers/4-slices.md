### Les *slices*

Les « slices » se traduisent en français par « tranches ». Cela signifie que l'on va prendre notre objet et le découper en morceaux.
Par exemple, récupérer la première moitié d'une liste, ou cette même liste en ne conservant qu'un élément sur deux.

Les *slices* sont une syntaxe particulière pour l'indexation, à l'aide du caractère `:` lors des appels à `[]`.

```python
>>> letters = ('a', 'b', 'c', 'd', 'e', 'f')
>>> letters[0:4]
('a', 'b', 'c', 'd')
>>> letters[1:-2]
('b', 'c', 'd')
>>> letters[::2]
('a', 'c', 'e')
```

Je pense que vous êtes déjà familier avec cette syntaxe. Le *slice* peut prendre jusqu'à 3 nombres :

- Le premier est l'indice de départ (0 si omis) ;
- Le second est l'indice de fin (fin de la liste si omis), l'élément correspondant à cet indice est exclu ;
- Le dernier est le pas, le nombre d'éléments passés à chaque itération (1 par défaut) ;

Parfois moins connu, les *slices* peuvent aussi servir pour la modification et la suppression :

```python
>>> letters = ['a', 'b', 'c', 'd', 'e', 'f']
>>> letters[::2] = 'x', 'y', 'z'
>>> letters
['x', 'b', 'y', 'd', 'z', 'f']
>>> del letters[0:3]
>>> letters
['d', 'z', 'f']
```

Une bonne chose pour nous, même avec les *slices*, ce sont les 3 mêmes méthodes `__getitem__`, `__setitem__` et `__delitem__` qui sont appelées. Cela signifie que la classe `MyList` que nous venons d'implémenter est déjà compatible avec les *slices*.

En fait, c'est simplement que le paramètre `key` passé ne représente pas un nombre, mais est un objet de type `slice` :

```python
>>> s = slice(1, -1)
>>> 'abcdef'[s]
'bcde'
>>> 'abcdef'[slice(None, None, 2)]
'ace'
```

Comme vous le voyez, le slice se construit toujours de la même manière, avec 3 nombres pouvant être omis, ou précisés à `None` pour prendre leur valeur par défaut.

L'objet ainsi construit contient 3 attributs : `start`, `stop`, et `step`.

```python
>>> s = slice(1, 2, 3)
>>> s.start
1
>>> s.stop
2
>>> s.step
3
```

Je vous conseille ce tutoriel de [**pascal.ortiz**](https://zestedesavoir.com/membres/voir/pascal.ortiz/) pour en savoir plus sur les slices : <https://zestedesavoir.com/tutoriels/582/les-slices-en-python/>
