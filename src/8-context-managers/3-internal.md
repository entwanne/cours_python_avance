## Fonctionnement interne

- __enter__, __exit__

Ça, c'est pour le cas d'utilisation, nous étudierons ici le fonctionnement interne.

Les gestionnaires de contexte sont en fait des objets disposant de deux méthodes spéciales : `__enter__` et `__exit__`, qui seront respectivement appelées à l'entrée et à la sortie du bloc `with`.

Le retour de la méthode ̀`__enter__` sera attibué à la variable spécifiée derrière le `as`.

Le bloc `with` est donc un bloc d'instructions très simple, offrant juste un sucre syntaxique autour d'un `try`/`finally`.

`__enter__` ne prend aucun paramètre, contrairement à `__exit__` qui en prend 3 : `exc_type`, `exc_value`, et `traceback` qui correspondent au type de l'exception levée, à sa valeur, et à son *traceback*.
Dans le cas où aucune exception n'est survenue pendant le traitement de la ressource, ces 3 paramètres valent `None`.

Nous pouvons maintenant créer notre propre type de contexte, contentons-nous pour le moment de quelque chose d'assez simple qui afficherait un message à l'entrée et à la sortie.

```python
class MyContext:
    def __enter__(self):
        print('enter')
        return self
    def __exit__(self, exc_type, exc_value, traceback):
        print('exit')
```

À l'utilisation :

```python
>>> with MyContext() as ctx:
...     print(ctx)
...
enter
<__main__.MyContext object at 0x7f23cc446cf8>
exit
```
