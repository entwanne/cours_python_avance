### Décorateurs paramétrés

Nous avons vu comment appliquer un décorateur à une fonction, nous pourrions cependant vouloir paramétrer le comportement de ce décorateur.
Dans notre exemple précédent (`print_decorator`), nous affichons du texte avant et après l'appel de fonction. Mais que faire si nous souhaitons modifier ce texte (pour en changer la langue, utiliser un autre terme que « fonction ») ?

Nous ne voulons pas avoir à créer un décorateur différent pour chaque phrase possible et imaginable. Nous aimerions pouvoir passer nos chaînes de caractères à notre décorateur pour qu'il s'occupe de les afficher au moment opportun.

En fait, `@` ne doit pas nécessairement être suivi d'un nom d'objet, des arguments peuvent aussi s'y ajouter à l'aide de parenthèses (comme on le ferait pour un appel).
Mais le comportement peut vous sembler étrange au premier abord.

Par exemple, pour utiliser un tel décorateur paramétré :

```python
@param_print_decorator('call {} with args({}) and kwargs({})', 'ret={}')
def test_func(x):
    return x
```

Il nous faudra posséder un *callable* `param_print_decorator` qui, quand il sera appelé, retournera un décorateur qui pourra ensuite être appliqué à notre fonction.
Un décorateur paramétéré n'est ainsi qu'un *callable* retournant un décorateur simple.

Le code de `param_print_decorator` ressemblerait ainsi à :

```python
def param_print_decorator(before, after): # Décorateur paramétré
    def decorator(function): # Décorateur
        def new_function(*args, **kwargs): # Fonction qui remplacera notre fonction décorée
            print(before.format(function.__name__, args, kwargs))
            ret = function(*args, **kwargs)
            print(after.format(ret))
            return ret
        return new_function
    return decorator
```
