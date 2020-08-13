from concurrent.futures import ProcessPoolExecutor
from .inventory import Inventory


def _execute(beverage, inventory):
    try:
        inventory.get_ingredients(ingredients=beverage.get_recipe())
        return f'{beverage.name} is prepared'

    except Exception as exc:
        return f'{beverage.name} cannot be prepared because {str(exc)}'


class BeverageMachine(object):
    def __init__(self, no_of_outlets):
        self.no_of_outlets = no_of_outlets
        self._beverage_maker = ProcessPoolExecutor(max_workers=no_of_outlets)

    def prepare_beverage(self, beverage, inventory):
        return self._beverage_maker.submit(_execute, beverage, inventory)
