# Métaclasses

Il vous est peut-être arrivé de lire qu'en Python tout était objet. Il faut cependant nuancer quelque peu : tout ne l'est pas, une instruction n'est pas un objet par exemple. Mais toutes les valeurs que l'on peut manipuler sont des objets.

À quoi peut-on alors reconnaître un objet ? Cela correspond à tout ce qui peut être stocké dans une variable. Ainsi, les nombres, les chaînes de caractère, les fonctions ou même les classes sont des objet. Et ce sont ici ces dernières qui nous intéressent.

En Python, tout objet a un type. Quel est donc le type d'une classe ?

```python
>>> type(object)
<class 'type'>
```

En effet, `type` est un peu plus complexe que ce que l'on pourrait penser, nous y reviendrons plus tard.

Une classe est donc une instance de la classe `type`. Une classe qui permet d'instancier des classes est appelée une métaclasse.


### À quoi sert une métaclasse ?

Une métaclasse permet donc de créer des classes, mais pourquoi faire ?


### Héritage et instanciation

Nous avions l'habitude de créer des classes en héritant d'une classe existante, mais pas en en instanciant une.
J'aimerais ici revenir sur ces concepts d'héritage et d'instanciation.

Les classes (ou *type objects*) sont un ensemble d'objets qui possèdent quelques caractéristiques communes :

- Elles héritent d'`object` (mis à part `object` lui-même) ;
- Elles sont des instances plus ou moins directes de `type` ;
- Elles peuvent être instanciées ;
- On peut en hériter.

```python
>>> int.__bases__ # int hérite d'object
(<class 'object'>,)
>>> type(int) # int est une instance de type
<class 'type'>
>>> int() # on peut instancier int
0
>>> class A(int): pass # on peut en hériter
```

`type` étant une classe, elle possède les mêmes caractéristiques.

```python
>>> type.__bases__ # type hérite d'object
(<class 'object'>,)
>>> type(type) # type est une instance de type
<class 'type'>
>>> class A(type): pass # on peut en hériter
```

Nous verrons par la suite comment nous pouvons instancier `type`.

Toutes les classes étant des instances de `type`, on en déduit qu'il faut passer par `type` pour toute construction de classe.
Une métaclasse est donc une classe héritant de `type`.

Même quand nous créons une classe par héritage, c'est en interne un appel à `type` qui est réalisé.

- http://www.cafepy.com/article/python_types_and_objects
