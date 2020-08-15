class Beverage(object):
    """
        Beverage is an entity that provides runtime definition
        of beverages or drinks available with the coffee machine
    """

    def __init__(self, name, ingredients):
        """
        param:name - string for identification of beverage
        param:ingredients - dict{<Ingredient>:<int(quantity)>} defines
            recipe for the beverage
        """
        self.name = name
        self._ingredients = ingredients

    def get_recipe(self):
        return self._ingredients
