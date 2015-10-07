## L'attribut de Dana

Que font réellement `getattr`, `setattr` et `delattr` ? Elles appellent des méthodes spéciales de l'objet.
`setattr` et `delattr` sont les cas les plus simples, la correspondance est faite avec les méthodes `__setattr__` et `__delattr__` de l'objet. Ces deux méthodes prennent respectivement les mêmes paramètres (en plus de `self`) que les fonctions auxquelles elles correspondent. `__setattr__` prendra donc le nom de l'attribut et sa nouvelle valeur, et `__delattr__` le nom de l'attribut.

Quant à `getattr`, la chose est un pleu complexe, car deux méthodes spéciales lui correspondent : `__getattribute__` et `__getattr__`. Ces deux méthodes prennent en paramètre le nom de l'attribut.
La première est appelée lors de la récupération de tout attribut. La seconde est réservée aux cas où l'attribut n'existe pas (si `__getattribute__` lève une `AttributeError` par exemple).
Par défaut, `__getattribute__` se charge de retourner les attributs contenus dans `__dict__`. Si vous voulez ajouter des attributs dynamiques, il vous faut donc plutôt passer par `__getattr__`.

Ainsi, pour définir dynamiquement un attribut, il nous suffit de coupler ces méthodes, tout en pensant à y utiliser `super` pour faire appel au comportement par défaut dans le cas où nous agissons sur un attribut « normal ».

```python
class Temperature:
    def __init__(self):
        self.value = 0

    def __getattr__(self, name):
        if name == 'celsius':
            return self.value
        if name == 'fahrenheit':
            return self.value * 1.8 + 32
        return super().__getattr__(name)

    def __setattr__(self, name, value):
        if name == 'celsius':
            self.value = value
        elif name == 'fahrenheit':
            self.value = (value - 32) / 1.8
	else:
            super().__setattr__(name, value)
```

Et à l'utilisation :

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

### dict et slots

Le `__dict__` dont je parle plus haut est le dictionnaire contenant les attributs d'un objet Python. Par défaut, il contient tous les attributs que vous définissez sur un objet (si vous ne modifiez pas le fonctionnement de `setattr`).
En effet, chaque fois que vous créez un attribut (`foo.bar = value`), celui-ci est enregistré dans le dictionnaire des attributs de l'objet (`foo.__dict__['bar'] = value`). La méthode `__getattribute__` de l'objet se contente donc de rechercher l'attribut dans le dictionnaire de l'objet et de ses parents (type de l'objet et classes dont ce type hérite).

Les slots sont une seconde manière de procéder, en vue de pouvoir optimiser le stockage de l'objet. Par défaut, lors de la création d'un objet, le dictionnaire `__dict__` est créé afin de pouvoir y stocker l'ensemble des attributs. Si la classe définit un énumérable `__slots__` contenant l'ensemble des attributs possibles de l'objet, le `__dict__` n'aura plus besoin d'être instancié lors de la création d'un nouvel objet.
Notez tout de même que si votre classe définit un `__slots__`, vous ne pourrez plus par défaut définir d'attributs autres sur l'objet que ceux décrits dans les slots.

Je vous invite à consulter la section de la documentation consacrée aux slots pour plus d'informations :

* https://docs.python.org/3/reference/datamodel.html#slots

### MRO

J'évoquais précédemment le comportement de `__getattribute__`, qui consiste à consulter le dictionnaire de l'objet puis de ces parents. Ce mécanisme est appelé *method resolution order* ou plus généralement *MRO*.

Chaque classe que vous définissez possède une méthode `mro`. Elle retourne une liste contenant l'ordre des classes à interroger lors de la résolution d'un appel sur l'objet.
C'est ce *MRO* qui définit la priorité des classes parentes lors d'un héritage multiple (quelle classe interroger en priorité), c'est encore lui qui est utilisé lors d'un appel à `super`, afin de savoir à quelle classe `super` fait référece.
En interne, la méthode `mro` fait appel à l'attribut `__mro__` de la classe.

Le comportement par défaut de `foo.__getattribute__('bar')` est donc assez simple :
1. On recherche dans `foo.__dict__` la présence d'une clef `'bar'`, dont on retourne la valeur si la clef existe ;
2. On recherche dans les `__dict__` de toutes les classes référencées par `type(foo).mro()`, en s'arrêtant à la première valeur trouvée ;
3. On lève une exception `AttributeError` si l'attribut n'a pu être trouvé.

Pour bien comprendre le fonctionnement du *MRO*, je vous propose de regarder quelques exemples d'héritage.

Premièrement, définissons quelques classes :

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
(<class 'toto.A'>, <class 'object'>)
>>> B.mro()
(<class 'toto.B'>, <class 'toto.A'>, <class 'object'>)
>>> C.mro()
(<class 'toto.C'>, <class 'object'>)
>>> D.mro()
(<class 'toto.D'>, <class 'toto.A'>, <class 'toto.C'>, <class 'object'>)
>>> E.mro()
(<class 'toto.E'>, <class 'toto.B'>, <class 'toto.A'>, <class 'toto.C'>, <class 'object'>)
>>> F.mro()
(<class 'toto.F'>, <class 'toto.D'>, <class 'toto.E'>, <class 'toto.B'>, <class 'toto.A'>, <class 'toto.C'>, <class 'object'>)
>>> G.mro()
(<class 'toto.G'>, <class 'toto.E'>, <class 'toto.B'>, <class 'toto.D'>, <class 'toto.A'>, <class 'toto.C'>, <class 'object'>)
```

On constate bien que les classes les plus à gauche sont proritaires lors d'un héritage, mais aussi que le mécanisme de *MRO* évite la présence de doublons dans la hiérarchie.

Si vous souhaitez en connaître davantage sur le *MRO*, c'est plutôt vers la documentation de python 2.3 qu'il faut s'orienter :

* https://www.python.org/download/releases/2.3/mro/
