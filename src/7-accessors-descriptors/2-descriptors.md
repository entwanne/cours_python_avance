## Les descripteurs

- __get__, __set__, __delete__

Les descripteurs sont une manière d'affecter des comportements plus évolués lors de la récupération/édition/suppression d'un attribut. Un descripteur est un objet affecté à un attribut, et dont des méthodes spéciales (`__get__`, `__set__`, et `__delete__`) seront appelées lorsque des opérations seront réalisées sur l'attribut.

https://docs.python.org/3/reference/datamodel.html#implementing-descriptors

```python
class Descriptor:
    def __get__(self, instance, owner):
        return 0
```
