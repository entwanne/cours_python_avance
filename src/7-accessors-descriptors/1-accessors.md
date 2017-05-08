## L'attribut de Dana

Que font réellement `getattr`, `setattr` et `delattr` ? Elles appellent des méthodes spéciales de l'objet.

`setattr` et `delattr` sont les cas les plus simples, la correspondance est faite avec les méthodes `__setattr__` et `__delattr__`.
Ces deux méthodes prennent les mêmes paramètres (en plus de `self`) que les fonctions auxquelles elles correspondent. `__setattr__` prendra donc le nom de l'attribut et sa nouvelle valeur, et `__delattr__` le nom de l'attribut.

Quant à `getattr`, la chose est un peu plus complexe, car deux méthodes spéciales lui correspondent : `__getattribute__` et `__getattr__`. Ces deux méthodes prennent en paramètre le nom de l'attribut.
La première est appelée lors de la récupération de tout attribut. La seconde est réservée aux cas où l'attribut n'a pas été trouvé (si `__getattribute__` lève une `AttributeError`).

Ces méthodes sont chargées de retourner la valeur de l'attribut demandé.
Il est en cela possible d'implémenter des attributs dynamiquement, en modifiant le comportement des méthodes : par exemple une condition sur le nom de l'attribut pour retourner une valeur particulière.

Par défaut, `__getattribute__` retourne les attributs définis dans l'objet (contenus dans son dictionnaire `__dict__` que nous verrons plus loin), et lève une `AttributeError` si l'attribut ne l'est pas.
`__getattr__` n'est pas présente de base dans l'objet, et n'a donc pas de comportement par défaut.
Il est plutôt conseillé de passer par cette dernière pour implémenter nos attributs dynamiques.

Ainsi, il nous suffit de coupler les méthodes de lecture, d'écriture, et/ou de suppression pour disposer d'attributs dynamiques.
Il faut aussi penser à relayer les appels au méthodes parentes *via* `super` pour utiliser le comportement par défaut quand on ne sait pas gérer l'attribut en question.

Le cas de `__getattr__` est un peu plus délicat : n'étant pas implémentée dans la classe `object`, il n'est pas toujours possible de relayer l'appel.
Il convient alors de travailler au cas par cas, en utilisant `super` si la classe parente implémente `__getattr__`, ou en levant une `AttributeError` sinon.

```python
class Temperature:
    def __init__(self):
        self.value = 0

    def __getattr__(self, name):
        if name == 'celsius':
            return self.value
        if name == 'fahrenheit':
            return self.value * 1.8 + 32
        raise AttributeError(name)

    def __setattr__(self, name, value):
        if name == 'celsius':
            self.value = value
        elif name == 'fahrenheit':
            self.value = (value - 32) / 1.8
        else:
            super().__setattr__(name, value)
```

Et à l'utilisation :

```python
>>> t = Temperature()
>>> t.celsius = 37
>>> t.celsius
37
>>> t.fahrenheit
98.6 # Ou valeur approximative
>>> t.fahrenheit = 212
>>> t.celsius
100.0
```

### *dict* et *slots*

Le `__dict__` dont je parle plus haut est le dictionnaire contenant les attributs d'un objet Python. Par défaut, il contient tous les attributs que vous définissez sur un objet (si vous ne modifiez pas le fonctionnement de `setattr`).
En effet, chaque fois que vous créez un attribut (`foo.bar = value`), celui-ci est enregistré dans le dictionnaire des attributs de l'objet (`foo.__dict__['bar'] = value`). La méthode `__getattribute__` de l'objet se contente donc de rechercher l'attribut dans le dictionnaire de l'objet et de ses parents (type de l'objet et classes dont ce type hérite).

Les slots sont une seconde manière de procéder, en vue de pouvoir optimiser le stockage de l'objet. Par défaut, lors de la création d'un objet, le dictionnaire `__dict__` est créé afin de pouvoir y stocker l'ensemble des attributs. Si la classe définit un itérable `__slots__` contenant l'ensemble des attributs possibles de l'objet, le `__dict__` n'aura plus besoin d'être instancié lors de la création d'un nouvel objet.
Notez tout de même que si votre classe définit un `__slots__`, vous ne pourrez plus par défaut définir d'attributs autres sur l'objet que ceux décrits dans les slots.

Je vous invite à consulter la section de la documentation consacrée aux slots pour plus d'informations :
<https://docs.python.org/3/reference/datamodel.html#slots>

### MRO

J'évoquais précédemment le comportement de `__getattribute__`, qui consiste à consulter le dictionnaire de l'objet puis de ses parents. Ce mécanisme est appelé *method resolution order* ou plus généralement *MRO*.

Chaque classe que vous définissez possède une méthode `mro`. Elle retourne un *tuple* contenant l'ordre des classes à interroger lors de la résolution d'un appel sur l'objet.
C'est ce *MRO* qui définit la priorité des classes parentes lors d'un héritage multiple (quelle classe interroger en priorité), c'est encore lui qui est utilisé lors d'un appel à `super`, afin de savoir à quelle classe `super` fait référence.
En interne, la méthode `mro` fait appel à l'attribut `__mro__` de la classe.

Le comportement par défaut de `foo.__getattribute__('bar')` est donc assez simple :

1. On recherche dans `foo.__dict__` la présence d'une clef `'bar'`, dont on retourne la valeur si la clef existe ;
2. On recherche dans les `__dict__` de toutes les classes référencées par `type(foo).mro()`, en s'arrêtant à la première valeur trouvée ;
3. On lève une exception `AttributeError` si l'attribut n'a pu être trouvé.

Pour bien comprendre le fonctionnement du *MRO*, je vous propose de regarder quelques exemples d'héritage.

Premièrement, définissons plusieurs classes :

```python
class A: pass
class B(A): pass
class C: pass
class D(A, C): pass
class E(B, C): pass
class F(D, E): pass
class G(E, D): pass
```

Puis observons.

```python
>>> object.mro()
(<class 'object'>,)
>>> A.mro()
(<class '__main__.A'>, <class 'object'>)
>>> B.mro()
(<class '__main__.B'>, <class '__main__.A'>, <class 'object'>)
>>> C.mro()
(<class '__main__.C'>, <class 'object'>)
>>> D.mro()
(<class '__main__.D'>, <class '__main__.A'>, <class '__main__.C'>, <class 'object'>)
>>> E.mro()
(<class '__main__.E'>, <class '__main__.B'>, <class '__main__.A'>, <class '__main__.C'>,
<class 'object'>)
>>> F.mro()
(<class '__main__.F'>, <class '__main__.D'>, <class '__main__.E'>, <class '__main__.B'>,
<class '__main__.A'>, <class '__main__.C'>, <class 'object'>)
>>> G.mro()
(<class '__main__.G'>, <class '__main__.E'>, <class '__main__.B'>, <class '__main__.D'>,
<class '__main__.A'>, <class '__main__.C'>, <class 'object'>)
```

On constate bien que les classes les plus à gauche sont proritaires lors d'un héritage, mais aussi que le mécanisme de *MRO* évite la présence de doublons dans la hiérarchie.

On remarque qu'en cas de doublon, les classes sont placées le plus loin possible du début de la liste : par exemple, `A` est placée après `B` et non après `C` dans le *MRO* de `E`.

Cela peut nous poser problème dans certains cas.

```python
>>> class H(A, B): pass
...
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: Cannot create a consistent method resolution
order (MRO) for bases B, A
```

En effet, nous cherchons à hériter d'abord de `A` en la plaçant à gauche, mais `A` étant aussi la mère de `B`, le *MRO* souheterait la placer à la fin, ce qui provoque le conflit.

Tout fonctionne très bien dans l'autre sens :

```python
>>> class H(B, A): pass
...
```
