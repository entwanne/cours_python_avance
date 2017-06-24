### TP : Une liste chaînée en Python

#### Présentation

Nous avons, dans les paragraphes précédents, créé un proxy autour d'une liste pour découvrir le fonctionnement des méthodes décrites.

Dans ce TP, pas à pas, nous créerons notre propre type de liste, à savoir une liste chaînée, c'est-à-dire composée de maillons reliés entre eux. Très courantes dans des langages bas-niveau tels que le C, elles le sont beaucoup moins en Python.

La différence avec le type `deque` du module `collections` est que nos listes seront simplement chaînées : un maillon n'aura connaissance que du maillon suivant, pas du précédent.

En plus de nos méthodes d'accès aux éléments, nous implémenterons les méthodes `insert` et `append` afin d'ajouter facilement des éléments à notre liste.

#### Bases

Nous appellerons donc notre classe `Deque` et, à la manière de `list`, le constructeur pourra prendre un objet pour pré-remplir notre liste.

Notre liste sera composée de maillons, et nous aurons donc une seconde classe, très simple, pour représenter un maillon : `Node`. un maillon possède une valeur (`value`), un maillon suivant (`next`), et… c'est tout. `next` pouvant être à `None` si l'on est en fin de liste.

La liste ne gardera qu'une référence vers le premier maillon, et vers le dernier (deux extrémités, *double-ended*).

Une seule chose à laquelle penser : quand nous instancions notre maillon, nous voulons que celui-ci référence le maillon suivant. Mais aussi, et surtout, que le maillon précédent le référence. Ainsi, le `next` du maillon précédent devra pointer vers notre nouveau maillon.

```python
class Node:
    def __init__(self, value, next=None):
        self.value = value
        self.next = next
```

Et notre classe `Deque`, qui contiendra une référence vers le premier et le dernier maillon, tout en itérant sur le potentiel objet passé au constructeur pour initialiser la liste.

```python
class Deque:
    def __init__(self, iterable=()):
        self.first = None # Premier maillon
        self.last = None # Dernier maillon
        for element in iterable:
            self.append(element)
```

Notre classe `Node` étant achevée, toutes les méthodes qui seront données par la suite seront à ajouter à la classe `Deque`.

#### `append` et `insert`

Si vous avez tenté d'instancier notre liste pour le moment (en lui précisant un paramètre), vous avez remarqué que celle-ci levait une erreur : en effet, nous appelons une méthode `append` qui n'est actuellement pas définie.

C'est par celle-ci que nous allons commencer, car son comportement est très simple : nous créons un nouveau noeud que nous ajoutons à la fin de la liste. Cela peut se résumer en :

- Créer un `Node` avec la valeur spécifiée en paramètre, et `None` comme maillon suivant ;
- Lier le nouveau maillon à l'actuel dernieer maillon ;
- Faire pointer la fin de liste sur ce nouveau maillon ;
- Et, ne pas oublier, dans le cas où notre liste est actuellement vide, de faire pointer le début de liste sur ce maillon.

```python
def append(self, value):
    node = Node(value, None)
    if self.last is not None:
        self.last.next = node
    self.last = node
    if self.first is None:
        self.first = node
```

Vient maintenant la méthode `insert`, qui permet d'insérer une nouvelle valeur à n'importe quel endroit de la liste. Nous allons pour cela nous aider d'une première méthode `get_node` pour récupérer un maillon dans la liste (un objet de type `Node`, donc, pas sa valeur), qui nous servira encore beaucoup par la suite.

Cette méthode prendra un nombre en paramètre, correspondant à l'indice du maillon que nous voulons extraire, et itérera sur les maillons de la liste jusqu'à arriver à celui-ci. Nous nous contenterons pour le moment de gérer les nombres positifs. Nous lèverons de plus une erreur si l'indice ne correspond à aucun maillon.

```python
def get_node(self, n):
    node = self.first
    while n > 0 and node is not None:
        node = node.next
        n -= 1
    if node is None:
        raise IndexError("list index out of range")
    return node
```

Notre méthode `insert` prend deux paramètres : la position et la valeur à insérer. Cette méthode aura trois comportements, suivant que l'on cherche à insérer la valeur en tête de liste, en fin, ou au milieu.

- Dans le premier cas, il nous faudra créer un nouveau maillon, avec `self.first` comme maillon suivant, puis faire pointer `self.first` sur ce nouveau maillon ;
- Dans les deux autres, il faudra repérer le maillon précédent à l'aide de `get_node`, puis insérer notre maillon à la suite de celui-ci ;
- Dans tous les cas, il faudra faire pointer `self.last` vers notre maillon si celui-ci est en fin de liste.

```python
def insert(self, i, value):
    if not i:
        node = Node(value, next=self.first)
        self.first = node
    else:
        prev = self.get_node(i - 1)
        node = Node(value, prev.next)
	prev.next = node
    if node.next is None:
        self.last = node
```

#### `__contains__`

Pour faire de notre liste un conteneur, il nous faut implémenter l'opération `in` et donc la méthode `__contains__`. Celle-ci, à la manière de `get_node`, itérera sur tous les maillons jusqu'à en trouver un correspondant à la valeur passée en paramètre et ainsi retourner `True`.
Si la valeur n'est pas trouvée après avoir itéré sur toute la liste, il convient alors de retourner `False`.

```python
def __contains__(self, value):
    node = self.first
    while node is not None:
        if node.value == value:
            return True
        node = node.next
    return False
```

#### `__len__`

Nous souhaitons maintenant pouvoir calculer la taille de notre liste. La méthode `__len__` sera aussi très similaire aux précédentes, elle itère simplement du début à la fin en comptant le nombre de noeuds.

```python
def __len__(self):
    node = self.first
    size = 0
    while node is not None:
        node = node.next
        size += 1
    return size
```

#### `__getitem__` et `__setitem__`

Dans un premier temps, implémentons ces deux méthodes sans tenir compte des `slice`. Une grande part du travail est déjà réalisé par `get_node` :

```python
def __getitem__(self, key):
    return self.get_node(key).value

def __setitem__(self, key, value):
    self.get_node(key).value = value
```

Puis vient la gestion des `slice`. Rappelons-nous ce que contient un `slice`, à savoir un indice de début, un indice de fin et un pas. Cela ne vous rappelle pas quelque chose ? Si, c'est exactement ce à quoi correspond `range`. À ceci près que les valeurs `None` n'ont aucune signification pour les `range`.

Mais l'objet `slice` possède une méthode `indices`, qui, en lui donnant la taille de notre ensemble, retourne les paramètres à passer à `range` (en gérant de plus pour nous les indices négatifs).

Nous pouvons ainsi obtenir un `range` à l'aide de l'expression `range(*key.indices(len(self)))` (en considérant que `key` est un objet de type `slice`). Il ne nous reste donc plus qu'à itérer sur le `range`, et :

- Créer une nouvelle liste contenant les éléments extraits dans le cas d'un `__getitem__` ;
- Modifier un à un les éléments dans le cas d'un `__setitem__`.

```python
def __getitem__(self, key):
    if isinstance(key, slice):
        new_list = Deque()
        indices = range(*key.indices(len(self)))
        for i in indices:
            new_list.append(self[i])
        return new_list
    else:
        return self.get_node(key).value

def __setitem__(self, key, value):
    if isinstance(key, slice):
        indices = range(*key.indices(len(self)))
        for i, v in zip(indices, value):
            self[i] = v
    else:
        self.get_node(key).value = value

```

Si vous ne comprenez pas bien ce que fait la fonction `zip`, celle-ci assemble deux listes (nous verrons dans le chapitre suivant que c'est un peu plus large que cela), de la manière suivante :

```python
>>> list(zip([1, 2, 3], ['a', 'b', 'c']))
[(1, 'a'), (2, 'b'), (3, 'c')]
```

#### Aller plus loin

Ce TP touche à sa fin, mais pour aller plus loin, voici une liste non exhaustive de fonctionnalités qu'il nous reste à implémenter :

- Gérer des nombres négatifs pour l'indexation ;
- Gérer les cas de `__setitem__` où la liste de valeurs a une taille différente de la taille du `slice` ;
- Implémenter la méthode `__delitem__` pour gérer la suppression de maillons, attention toutefois pour la gestion des `slice`, les indices seront invalidés après chaque suppression ;
- Implémenter les méthodes spéciales `__str__` et `__repr__` pour afficher facilement notre liste.
