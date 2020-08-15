from entity.beverage import Beverage
from entity.beverage_machine import BeverageMachine
from entity.ingredient import Ingredient
from entity.inventory import Inventory
from reader import IReader
from reader.json_reader import JSONReader
from reader.schema import JSONInput


def execute_demo_order(reader: IReader, source, inv_refill_time, inv_fetch_time):
    """
        param:reader - IReader implementation to be used for
            reading the input. Could be replaced by appropriate
            data source.
        param:source - object or file name to read from
    """
    try:
        # get input data using reader & source
        inp = reader.read(source)

        # create inventory
        inventory = Inventory(refill_time=inv_refill_time,
                              fetch_time=inv_fetch_time)

        # refilll inventory with ingredients
        inventory.refill(
            ingredients={
                Ingredient(ingredient):
                inp["machine"]["total_items_quantity"][ingredient]
                for ingredient in inp["machine"]["total_items_quantity"]})

        # create coffee machine
        machine = BeverageMachine(
            no_of_outlets=inp["machine"]["outlets"]["count_n"])

        # pool or queue orders for preparation
        # Here, we are using FIFO. An actual controller can have
        # different mechanism of queueing the orders. It could have
        # some refill actions being performed on inventory in between
        order_prep_pool = []
        for bev_name in inp["machine"]["beverages"]:
            order_future = machine.prepare_beverage(
                beverage=Beverage(
                    name=bev_name,
                    ingredients={
                        Ingredient(ingredient):
                        inp["machine"]["beverages"][bev_name][ingredient]
                        for ingredient in inp["machine"]["beverages"][bev_name]
                    }),
                inventory=inventory
            )
            order_prep_pool.append(order_future)

        # dispense prepared orders & obtain results
        order_results = []
        for order in order_prep_pool:
            machine_response = machine.dispense_beverage(order)
            order_results.append(machine_response)

        return order_results

    except Exception as exc:
        print(exc)


if __name__ == "__main__":
    # demo or sample executor for sample input
    # for full application Controller can be implemented to
    # start a machine & expose it using HTTP or
    # here i
    reader = JSONReader(schema=JSONInput)
    results = execute_demo_order(
        reader, source="./input/input.json", inv_refill_time=-1, inv_fetch_time=-1)
    if results:
        print('\n'.join(results))

    Inventory.reset()
