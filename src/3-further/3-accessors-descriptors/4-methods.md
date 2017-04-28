### Les méthodes

Les méthodes en Python vous réservent aussi bien des surprises. Si vous avez déjà rencontré les termes de méthodes de classe (*class methods*), méthodes statiques (*static methods*), ou méthodes préparées (*bound methods*), vous avez pu vous demander comment cela fonctionnait.

En fait, les méthodes sont des descripteurs vers les fonctions que vous définissez à l'intérieur de votre classe. Elles sont même ce qu'on appelle des *non-data descriptors*, c'est à dire des descripteurs qui ne définissent ni *setter*, ni *deleter*.

Définissons une simple classe `A` possédant différents types de méthodes.

```python
class A:
    def method(self):
        return self
    @staticmethod
    def staticmeth():
        pass
    @classmethod
    def clsmeth(cls):
        return cls
```

Puis observons à quoi correspondent les différents accès à ces méthodes.

```python
>>> a = A() # on crée une instance `a` de `A`
>>> A.method # méthode depuis la classe
<function A.method at 0x7fd412ad5f28>
>>> a.method # méthode depuis l'instance
<bound method A.method of <__main__.A object at 0x7fd412a3ad68>>
>>> A.staticmeth # méthode statique depuis la classe
<function A.staticmeth at 0x7fd412a41048>
>>> a.staticmeth # depuis l'instance
<function A.staticmeth at 0x7fd412a41048>
>>> A.clsmeth # méthode de classe depuis la classe
<bound method type.clsmeth of <class '__main__.A'>>
>>> a.clsmeth # depuis l'instance
<bound method type.clsmeth of <class '__main__.A'>>
```

On remarque que certains accès retournent des fonctions, et d'autres des *bound methods*, mais quelle différence ?
En fait, la différence survient lors de l'appel, pour le passage du premier paramètre.

Ne vous êtes-vous jamais demandé comment l'objet courant arrivait dans `self` lors de l'appel d'une méthode ? C'est justement parce qu'il s'agit d'une *bound method*.
C'est en fait une méthode dont le premier paramètre est déjà préparé, et qu'il n'y aura donc pas besoin de spécifier à l'appel.
C'est le descripteur qui joue ce rôle, il est le seul à savoir si vous utilisez la méthode depuis une instance ou depuis la classe (`instance` valant `None` dans ce second cas), et connaît toujours le premier paramètre à passer (`instance`, `owner`, ou rien).
Il peut ainsi construire un nouvel objet (*bound method*), qui lorsqu'il sera appelé se chargera de relayer l'appel à la vraie méthode en lui ajoutant ce paramètre.

Le même comportement est utilisé pour les méthodes de classes, où la classe de l'objet doit être passée en premier paramètre (`cls`).
Le cas des méthodes statiques est en fait le plus simple, il ne s'agit que de fonctions qui ne prennent pas de paramètres spéciaux, donc qui ne nécessitent pas d'être décorées par le descripteur.

On remarque aussi que, `A.method` retournant une fonction et non une méthode préparée, il nous faudra indiquer une instance lors de l'appel.

Pour rappel, voici comment s'utilisent ces différentes méthodes :

```python
>>> A.method(a)
<__main__.A object at 0x7fd412a3ad68>
>>> a.method()
<__main__.A object at 0x7fd412a3ad68>
>>> A.staticmeth()
>>> a.staticmeth()
>>> A.clsmeth()
<class '__main__.A'>
>>> a.clsmeth()
<class '__main__.A'>
```
