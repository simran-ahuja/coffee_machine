from multiprocessing import Lock, Value, Manager
from .errors import (InventoryFetchException,
                     InventoryLowException, InventoryRefillException)


class Inventory(object):
    _lock = Lock()
    _manager = Manager()
    _ingredients = _manager.dict()

    def refill(self, ingredients):
        locked = False
        try:
            locked = Inventory._lock.acquire(block=True, timeout=None)

            for ingredient in ingredients:
                if not Inventory._ingredients.get(ingredient):
                    Inventory._ingredients[ingredient] = 0
                Inventory._ingredients[ingredient] = (
                    ingredients[ingredient] + Inventory._ingredients[ingredient])

        except Exception as exc:
            raise InventoryRefillException(
                f'Failed to refill inventory:{str(exc)}'
            )
        finally:
            if locked:
                Inventory._lock.release()

    def get_ingredients(self, ingredients):
        try:
            locked = Inventory._lock.acquire(block=True, timeout=None)
            insufficient_ingredients = []
            unavailable_ingredients = []
            for ingredient in ingredients:
                if (not Inventory._ingredients.get(ingredient) or
                        Inventory._ingredients[ingredient] == 0):
                    unavailable_ingredients.append(ingredient)
                elif Inventory._ingredients[ingredient] < ingredients[ingredient]:
                    insufficient_ingredients.append(ingredient)

            err_str = ''

            if unavailable_ingredients or insufficient_ingredients:

                if unavailable_ingredients:
                    err_str = ', '.join(
                        unavailable_ingredients) + ' is not available'

                if insufficient_ingredients:
                    err_str = (
                        err_str + (' and ' if unavailable_ingredients else ''))
                    err_str = (err_str +
                               ('items ' if len(insufficient_ingredients) > 1
                                else 'item ') +
                               ', '.join(insufficient_ingredients) +
                               ' is not sufficient')

            else:
                for ingredient in ingredients:
                    Inventory._ingredients[ingredient] = (
                        Inventory._ingredients[ingredient] -
                        ingredients[ingredient]
                    )

        except Exception as exc:
            raise InventoryFetchException(
                f'Failed to get ingredients from inventory:{str(exc)}'
            )
        else:
            if err_str:
                raise InventoryLowException(f'{err_str}')
        finally:
            if locked:
                Inventory._lock.release()
