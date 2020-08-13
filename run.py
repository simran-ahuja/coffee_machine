from entity.beverage import Beverage
from entity.beverage_machine import BeverageMachine
from entity.ingredient import Ingredient
from entity.inventory import Inventory
from reader import IReader
from reader.json_reader import JSONReader
from reader.schema import JSONInput


def execute(reader: IReader):
    try:
        inp = reader.read()
        inventory = Inventory()

        inventory.refill(
            ingredients={
                ingredient:
                inp["machine"]["total_items_quantity"][ingredient]
                for ingredient in inp["machine"]["total_items_quantity"]})
        machine = BeverageMachine(
            no_of_outlets=inp["machine"]["outlets"]["count_n"])

        order_prep_pool = []
        for bev_name in inp["machine"]["beverages"]:
            response = machine.prepare_beverage(
                beverage=Beverage(
                    name=bev_name,
                    ingredients={
                        ingredient:
                        inp["machine"]["beverages"][bev_name][ingredient]
                        for ingredient in inp["machine"]["beverages"][bev_name]
                    }),
                inventory=inventory
            )
            order_prep_pool.append(response)

        results = []
        for order in order_prep_pool:
            machine_response = order.result()
            results.append(machine_response)

        return results

    except Exception as exc:
        print(exc)


if __name__ == "__main__":
    reader = JSONReader(schema=JSONInput)
    results = execute(reader)
    if results:
        print('\n'.join(results))
