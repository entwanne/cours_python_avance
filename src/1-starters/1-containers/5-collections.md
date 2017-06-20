### Module `collections`

Avant d'en terminer avec les conteneurs, je voulais vous présenter le [module `collections`](https://docs.python.org/3/library/collections.html).
Ce module, parfois méconnu, comprend différents conteneurs utiles de la bibliothèque standard, que je vais essayer de vous présenter brièvement.

#### `namedtuple`

Les *tuples* nommés (ou *named tuples*), sont très semblables aux *tuples*, dont ils héritent.
Ils ajoutent simplement la possibilité de référencer les champs du *tuple* par un nom plutôt que par un index, pour gagner en lisibilité.

On instancie `namedtuple` pour créer un nouveau type de *tuples* nommés.
`namedtuple` prend en paramètre le nom du type et la liste des noms de champs.

```python
>>> from collections import namedtuple
>>> Point2D = namedtuple('Point2D', ['x', 'y'])
>>> p = Point2D(3, 5)
>>> p.x
3
>>> p.y
5
>>> p[0]
3
>>> p
Point2D(x=3, y=5)
>>> Point2D(x=1, y=2)
Point2D(x=1, y=2)
```

#### `deque`

Les *queues* à deux extrémités (ou *double-ended queues* contracté en *deques*), sont des objets proches des listes de Python, mais avec une structure interne différente.

Plutôt qu'avoir un tableau d'éléments, les éléments sont vus comme des maillons liés les uns aux autres.

L'intérêt des *deques* par rapport aux listes est d'offrir de meilleures performances pour l'insertion/suppression d'éléments en tête et queue de liste, mais moins bonnes pour l'accès à un élément en milieu de liste.
Elles peuvent donc être indiquées pour gérer des piles ou des files.

Pour bénéficier de ces optimisations, les *deques* sont pourvues de méthodes `appendleft`, `extendleft` et `popleft` qui travaillent sur l'extrêmité gauche de la séquence, en plus des habituelles `append`/`extend`/`pop` qui travaillent sur celle de droite.

```python
>>> from collections import deque
>>> d = deque([1, 2, 3])
>>> d
deque([1, 2, 3])
>>> d.append(4)
>>> d.appendleft(0)
>>> d
deque([0, 1, 2, 3, 4])
>>> d.popleft()
0
>>> d.popleft()
1
>>> d.extendleft([1, 0])
>>> d
deque([0, 1, 2, 3, 4])
>>> d[0], d[1], d[-1]
(0, 1, 4)
>>> d[-1] = 5
>>> d
deque([0, 1, 2, 3, 5])
```

Les *deques* ont aussi la possibilité d'être limitées en taille, en supprimant les éléments les plus à droite lors d'une insertion à gauche et inversement.
Cela permet la réalisation de tampons circulaires.

```python
>>> d = deque([], 2)
>>> d
deque([], maxlen=2)
>>> d.append(1)
>>> d.append(2)
>>> d
deque([1, 2], maxlen=2)
>>> d.append(3)
>>> d
deque([2, 3], maxlen=2)
>>> d.appendleft(1)
>>> d
deque([1, 2], maxlen=2)
>>> d.maxlen
2
```

#### `ChainMap`

Les `ChainMap` sont des structures de données permettant de grouper (chaîner) plusieurs dictionnaires (ou *mappings*) sans les fusionner, ce qui leur permet de se tenir à jour.
Elles se comportent comme des dictionnaires et s'occupent de rechercher les éléments dans les *mappings* qui lui ont été donnés à la construction.
Lors de l'insertion de nouveaux éléments, ceux-ci sont ajoutés au premier *mapping*.

```python
>>> from collections import ChainMap
>>> d1 = {'a': 0, 'b': 1}
>>> d2 = {'b': 2, 'c': 3}
>>> d3 = {'d': 4}
>>> c = ChainMap(d1, d2, d3)
>>> c
ChainMap({'b': 1, 'a': 0}, {'c': 3, 'b': 2}, {'d': 4})
>>> c['a'], c['b'], c['c'], c['d']
(0, 1, 3, 4)
>>> c['e'] = 5
>>> c
ChainMap({'e': 5, 'b': 1, 'a': 0}, {'c': 3, 'b': 2}, {'d': 4})
>>> d1
{'e': 5, 'b': 1, 'a': 0}
>>> d2['f'] = 6
>>> c['f']
6
```

Les `ChainMap` ajoutent quelques fonctionnalités pratiques :

* L'attribut `maps` pour obtenir la liste des *mappings* ;
* La méthode `new_child` pour créer un nouveau `ChainMap` à partir de l'actuel, ajoutant un dictionnaire à gauche ;
* L'attribut `parents` pour obtenir les « parents » de l'actuel, c'est-à-dire le `ChainMap` composé des mêmes *mappings* excepté le plus à gauche.

```python
>>> c.maps
[{'e': 5, 'b': 1, 'a': 0}, {'c': 3, 'b': 2, 'f': 6}, {'d': 4}]
>>> c.new_child()
ChainMap({}, {'e': 5, 'b': 1, 'a': 0}, {'c': 3, 'b': 2, 'f': 6}, {'d': 4})
>>> c.new_child({'a': 7})
ChainMap({'a': 7}, {'e': 5, 'b': 1, 'a': 0}, {'c': 3, 'b': 2, 'f': 6}, {'d': 4})
>>> c.parents
ChainMap({'c': 3, 'b': 2, 'f': 6}, {'d': 4})
```

Les `ChainMap` se révèlent alors très utiles pour gérer des contextes / espaces de noms imbriqués,
comme [présenté dans la documentation](https://docs.python.org/3/library/collections.html#chainmap-examples-and-recipes).

#### `Counter`

Les compteurs (`Counter`) sont des dictionnaires un peu spéciaux qui servent à compter les éléments.

```python
>>> from collections import Counter
>>> c = Counter([1, 2, 3, 1, 3, 1, 5])
>>> c
Counter({1: 3, 3: 2, 2: 1, 5: 1})
>>> c[3]
2
>>> c[4]
0
>>> c[5] += 1
>>> c
Counter({1: 3, 3: 2, 5: 2, 2: 1})
>>> c + Counter({1: 2, 2: 3})
Counter({1: 5, 2: 4, 3: 2, 5: 2})
>>> c - Counter({1: 2, 2: 3})
Counter({3: 2, 5: 2, 1: 1})
```

On retrouve quelques méthodes utiles pour manipuler les compteurs.

```python
>>> list(c.elements())
[1, 1, 1, 2, 3, 3, 5, 5]
>>> c.most_common()
[(1, 3), (3, 2), (5, 2), (2, 1)]
>>> c.most_common(2)
[(1, 3), (3, 2)]
>>> c.update({5: 1})
>>> c
Counter({1: 3, 5: 3, 3: 2, 2: 1})
>>> c.subtract({2: 4})
>>> c
Counter({1: 3, 5: 3, 3: 2, 2: -3})
>>> +c # éléments positifs
Counter({1: 3, 5: 3, 3: 2})
>>> -c # éléments négatifs
Counter({2: 3})
```

#### `OrderedDict`

Les dictionnaires ordonnées (`OrderedDict`) sont comme leur nom l'indique des dictionnaires où l'ordre d'insertion des éléments est conservé, et qui sont itérés dans cet ordre.

Certaines implémentations (pypy, CPython 3.6) disposent de dictionaires ordonnés par défaut, mais il est préférable de passer par `OrderedDict` pour s'en assurer.

Depuis Python 3.6[^article36], on peut construire un dictionnaire ordonné de la manière suivante :

```python
>>> from collections import OrderedDict
>>> d = OrderedDict(b=0, a=1, c=2)
```

Dans les versions précédentes du langage, l'ordre des paramètres nommés n'étant pas assuré, il faut plutôt procéder avec un conteneur ordonné en paramètre.

```python
>>> d = OrderedDict([('b', 0), ('c', 2), ('a', 1)])
```

Le dictionnaire ordonné est sinon semblable à tout autre dictionnaire.

```python
>>> d['d'] = 4
>>> d['c'] = 5
>>> for key, value in d.items():
...     print(key, value)
...
b 0
c 5
a 1
d 4
```

[^article36]: Je vous invite à consulter cet article sur la sortie de Python 3.6
pour en savoir plus sur les nouveautés apportées par cette version :
<https://zestedesavoir.com/articles/1540/sortie-de-python-3-6/>

#### `defaultdict`

Voyons maintenant un dernier type de dictionnaires, les `defaultdict` (dictionnaires à valeurs par défaut).
Les compteurs décrits plus haut sont un exemple de dictionnaires à valeurs par défaut : quand un élément n'existe pas, c'est `0` qui est retourné.

Les `defaultdict` sont plus génériques que cela.
Lors de leur construction, ils prennent en premier paramètre une fonction qui servira à initialiser les éléments manquants.

```python
>>> from collections import defaultdict
>>> d = defaultdict(lambda: 'x')
>>> d[0] = 'a'
>>> d[1] = 'b'
>>> d[2]
'x'
>>> d
defaultdict(<function <lambda> at 0x7ffa55be42f0>, {0: 'a', 1: 'b', 2: 'x'})
```

#### *Wrappers*

Enfin, 3 classes (`UserDict`, `UserList` et `UserString`) sont présentes dans ce module.
Elles permettent par héritage de créer vos propres types de dictionnaires, listes ou chaînes de caractères, pour leur ajouter des méthodes par exemple.
Elles gardent une référence vers l'objet qu'elles étendent dans leur attribut `data`.

```python
>>> from collections import UserList
>>> class MyList(UserList):
...     def head(self):
...         return self.data[0]
...     def queue(self):
...         return self.data[1:]
...
>>> l = MyList([1, 2, 3])
>>> l.append(4)
>>> l
[1, 2, 3, 4]
>>> l.head()
1
>>> l.queue()
[2, 3, 4]
```

Ces classes datent cependant d'un temps ~~que les moins de 20 ans ne peuvent pas connaître~~ où il était impossible d'hériter des types `dict`, `list` ou `str`.
Elles ont depuis perdu de leur intérêt.
