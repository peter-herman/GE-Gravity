from typing import Dict

__author__ = "Austin Drenski"
__project__ = "GE-Gravity.ModelDevelopment"
__created__ = "10-4-2017"
__altered__ = "10-11-2017"
__version__ = "1.1.0"


class Country(object):
    """
    Represents a country record for use in a gravity model.
    """

    __slots__ = [
        "name",
        "expenditure_share",
        "output_share",
        "import_trade_costs",
        "export_trade_costs",
        "import_cost_by_expenditure_share",
        "export_cost_by_output_share"
    ]

    def __init__(self, name: str, expenditure_share: float, output_share: float, import_trade_costs: Dict[str, float], export_trade_costs: Dict[str, float]) -> None:
        self.name = name
        self.expenditure_share = expenditure_share
        self.output_share = output_share
        self.import_trade_costs = import_trade_costs
        self.export_trade_costs = export_trade_costs
        self.import_cost_by_expenditure_share = dict([(key, expenditure_share * value) for key, value in import_trade_costs.items()])
        self.export_cost_by_output_share = dict([(key, output_share * value) for key, value in export_trade_costs.items()])

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return "(name='{0}', expenditure_share='{1}', output_share='{2}')".format(self.name, self.expenditure_share,
                                                                                  self.output_share)
