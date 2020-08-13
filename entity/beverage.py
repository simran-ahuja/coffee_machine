class Beverage(object):
    def __init__(self, name, ingredients):
        self.name = name
        self._ingredients = ingredients

    def get_recipe(self):
        return self._ingredients
