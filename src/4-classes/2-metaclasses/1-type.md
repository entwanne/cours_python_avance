### Quel est donc ce `type` ?

Ainsi, vous l'aurez compris, `type` n'est pas utile que pour connaître le type d'un objet.
Dans l'utilisation que vous connaissiez, `type` prend un unique paramètre, et en retourne le type.

Pour notre autre utilisation, ses paramètres sont au nombre de 3 :

- `name` -- une chaîne de caractères représentant le nom de la classe à créer ;
- `bases` -- un tuple contenant les classes dont nous héritons (`object` est implicite) ;
- `dict` -- le dictionnaire des attributs et méthodes de la nouvelle classe.

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
```

Nous avons ici une classe `A`, strictement équivalente à la suivante :

```python
class A:
    x = 4
```

Voici maintenant un exemple plus complet, avec héritage et méthodes.

```python
>>> B = type('B', (int,), {})
>>> B()
0
>>> B = type('B', (int,), {'next': lambda self: self + 1})
>>> B(5).next()
6
>>> def C_prev(self):
...     return self - 1
...
>>> C = type('C', (B,), {'prev': C_prev})
>>> C(5).prev()
4
>>> C(5).next()
6
```
