## Simplifions-nous la vie avec la `contextlib`

Vous pourriez trouver une similitude entre les décorateurs et les gestionnaires de contextes : dans les deux cas, on cherche à exécuter quelque chose avant et après un bloc d'instructions.

Il existe dans la `contextlib` un outil qui les rapproche. Une classe, `ContextDecorator`, permet de transformer un gestionnaire de contexte en décorateur, et donc de pouvoir l'utiliser comme l'un ou comme l'autre.
Cela peut s'avérer utile pour créer un module qui mesurerait le temps d'exécution d'un ensemble d'instructions : on peut vouloir sans servir via `with`, ou via un décorateur autour de notre fonction à mesurer.

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

Et s'utilise comme suit :

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

De nombreux autres outils sont encore présents dans cette bibliothèque pour simplifier l'écriture de gestionnaires de contexte plus complexes.
Intéressons-nous maintenant à `contextmanager`. Il s'agit d'un décorateur capable de transformer une fonction génératrice en *context manager*.
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

Attention tout de même, une exeption levée dans le bloc d'instructions du `with` remonterait jusqu'au générateur, et empêcherait donc l'exécution du `__exit__`.

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
