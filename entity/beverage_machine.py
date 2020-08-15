from concurrent.futures import ThreadPoolExecutor

from .errors import InventoryLowException, InventoryFetchException
from .inventory import Inventory


def _prepare(beverage, inventory):
    """
    Prepares the beverage if all the ingredients in the recipe are
    available in inventory in sufficient amount

    result - string notifying the user about the beverage preparation
    or failures
    """

    try:
        # check if required inventory is available & required ingredients
        # from it, otherwise capture the exception of failure
        # and notify client accordingly (abstracting the information of
        # failure appropriately)
        inventory.get_ingredients(ingredients=beverage.get_recipe())
        return f'{beverage.name} is prepared'

    except InventoryLowException as exc:
        return f'{beverage.name} cannot be prepared because {str(exc)}'

    except InventoryFetchException:
        return f'Machine Failure: {beverage.name} cannot be prepared, could not fetch inventory. please report!'

    except Exception:
        return f'Machine Failure: {beverage.name} cannot be prepared, please retry!'


class BeverageMachine(object):
    """
    Beverage Machine is an entity for drink machine to prepare
    and dispense beverage from depending upon the inventory.
    It uses ThreadPoolExecutor
    """

    def __init__(self, no_of_outlets):
        """
        param:no_of_outlets - int for defining no of outlets in a machine
        """
        self.no_of_outlets = no_of_outlets
        self._beverage_maker = ThreadPoolExecutor(max_workers=no_of_outlets)

    def prepare_beverage(self, beverage, inventory):
        """
        param:beverage - Beverage to be prepared
        param:inventory - current state of inventory

        result - orders futures to be used for dispensing beverage

        This function employs ThreadPoolExecutor to parallely prepare
        incoming orders depending on the no of outlets & inventory
        using _prepare function
        """
        return self._beverage_maker.submit(_prepare, beverage, inventory)

    def dispense_beverage(self, order_future):
        """
        param:order_future - Concurrent.futures value corresponding an
        order in the order pool

        result - string informing status of beverage that was to be
        prepared
        """
        return order_future.result()
