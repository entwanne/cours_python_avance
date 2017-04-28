### Simplifions-nous la vie avec la `contextlib`

La [`contextlib`](https://docs.python.org/3/library/contextlib.html) est un module de la bibliothèque standard comportant divers outils ou gestionnaires de contexte bien utiles.

Par exemple, une classe, `ContextDecorator`, permet de transformer un gestionnaire de contexte en décorateur, et donc de pouvoir l'utiliser comme l'un ou comme l'autre.
Cela peut s'avérer utile pour créer un module qui mesurerait le temps d'exécution d'un ensemble d'instructions : on peut vouloir s'en servir via `with`, ou via un décorateur autour de notre fonction à mesurer.

Cet outil s'utilise très facilement, il suffit que notre gestionnaire de contexte hérite de `ContextDecorator`.

```python
from contextlib import ContextDecorator
import time

class spent_time(ContextDecorator):
    def __enter__(self):
        self.start = time.time()
    def __exit__(self, *_):
        print('Elapsed {:.3}s'.format(time.time() - self.start))
```

Et à l'utilisation :

```python
>>> with spent_time():
...   print('x')
...
x
Elapsed 0.000106s
>>> @spent_time()
... def func():
...     print('x')
...
>>> func()
x
Elapsed 0.000108s
```

Intéressons-nous maintenant à `contextmanager`. Il s'agit d'un décorateur capable de transformer une fonction génératrice en *context manager*.
Cette fonction génératrice devra disposer d'un seul et unique `yield`.
Tout ce qui est présent avant le `yield` sera exécuté en entrée, et ce qui se situe ensuite s'exécutera en sortie.

```python
>>> from contextlib import contextmanager
>>> @contextmanager
... def context():
...     print('enter')
...     yield
...     print('exit')
...
>>> with context():
...     print('during')
...
enter
during
exit
```

Attention tout de même, une exception levée dans le bloc d'instructions du `with` remonterait jusqu'au générateur, et empêcherait donc l'exécution du `__exit__`.

```python
>>> with context():
...     raise Exception
...
enter
Traceback (most recent call last):
  File "<stdin>", line 2, in <module>
Exception
```

Il convient donc d'utiliser un `try`/`finally` si vous souhaitez vous assurer que la fin du générateur sera toujours exécutée.

```python
>>> @contextmanager
... def context():
...     try:
...         print('enter')
...         yield
...     finally:
...         print('exit')
...
>>> with context():
...     raise Exception
...
enter
exit
Traceback (most recent call last):
  File "<stdin>", line 2, in <module>
Exception
```

Enfin, le module contient divers gestionnaires de contexte, qui sont :

* [`closing`](https://docs.python.org/3/library/contextlib.html#contextlib.closing) qui permet de fermer automatiquement un objet (par sa méthode `close`) ;
* [`suppress`](https://docs.python.org/3/library/contextlib.html#contextlib.suppress) afin de supprimer certaines exceptions survenues dans un contexte ;
* [`redirect_stdout`](https://docs.python.org/3/library/contextlib.html#contextlib.redirect_stdout) pour rediriger temporairement la sortie standard du programme.
