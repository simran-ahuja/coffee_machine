from threading import RLock

from .errors import (InventoryFetchException,
                     InventoryLowException, InventoryRefillException)


class Inventory(object):
    """
    Inventory entity is used to manage stock in the system.
    Actions like refilling & fetching from inventory are Critical
    Section Problem. Thus, Inventory has maintains a lock for
    performing such actions. The timeout for acquiring such lock
    depends on the constant time expected for these actions. If the
    timeout is set to -1, it is expected to have no upper limit.
    """
    _lock = RLock()
    _ingredients = {}

    def __init__(self, refill_time, fetch_time):
        """
        param:refill_time - define a constant refill timeout
            for inventory. Refilling action can only acquire the
            _lock for this duration
        param:fetch_time - define a constant fetch time for
            inventory. Fetch action can only acquire the
            _lock for this duration
        """
        self.refill_time = refill_time
        self.fetch_time = fetch_time

    @classmethod
    def reset(cls):
        Inventory._ingredients = {}

    def refill(self, ingredients):
        """
        param:ingredients - dict{Ingredient: int<quantity>} to be refilled
        """
        locked = False
        try:
            # acquire lock when available
            locked = Inventory._lock.acquire(
                blocking=True, timeout=self.refill_time)

            # add or update ingredients to inventory
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
            # release the lock if it was acquired
            if locked:
                Inventory._lock.release()

    def get_ingredients(self, ingredients):
        """
        param:ingredients - dict{Ingredient: int<quantity>} to be fetched
        """
        try:
            # acquire lock when available
            locked = Inventory._lock.acquire(
                blocking=True, timeout=self.fetch_time)

            insufficient_ingredients = []
            unavailable_ingredients = []

            # check if required ingredients are available in inventory
            # update insufficient_ingredients if available qty is less
            # than required
            # update unavailable_ingredients if a required ingredient
            # is unavailable in inventory
            for ingredient in ingredients:
                if (not Inventory._ingredients.get(ingredient) or
                        Inventory._ingredients[ingredient] == 0):
                    unavailable_ingredients.append(ingredient)
                elif Inventory._ingredients[ingredient] < ingredients[ingredient]:
                    insufficient_ingredients.append(ingredient)

            # build err_str if ingredients are are unavailable and/or
            # insufficient in qty
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
                # if all ingredients are available in required qty
                # remove them from inventory for preparation
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
            # release the lock if it was acquired
            if locked:
                Inventory._lock.release()
