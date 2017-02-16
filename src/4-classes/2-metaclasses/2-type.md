### Quel est donc ce `type` ?

Ainsi, vous l'avez bien compris, `type` n'est pas utile que pour connaître le type d'un objet.
`type` est une métaclasse, et sert donc à créer de nouvelles classes.

Dans l'utilisation que vous connaissez, `type` prend un unique paramètre, et en retourne le type.

Pour notre autre utilisation, ses paramètres sont au nombre de 3 :

- Une chaîne de caractères représentant le nom de la classe ;
- Un tuple contenant les classes dont nous héritons (`object` est implicite) ;
- Le dictionnaire des attributs et méthodes de la classe.

```python
>>> type('A', (), {})
<class '__main__.A'>
>>> A = type('A', (), {'x': 4})
>>> A.x
4
>>> A().x
4
>>> type(A)
<class 'type'>
>>> type(A())
<class '__main__.A'>
>>> B = type('B', (int,), {})
>>> B()
0
>>> B = type('B', (int,), {'test': lambda self: self + 1})
>>> B(5).test()
6
```
