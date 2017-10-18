from typing import Dict

__author__ = "Austin Drenski"
__project__ = "GE-Gravity.ModelDevelopment"
__created__ = "10-4-2017"
__altered__ = "10-18-2017"
__version__ = "1.2.0"


class Country(object):
    """
    Represents a country record for use in a gravity model.
    """

    @property
    def name(self):
        return self.__name

    @property
    def expenditure_share(self):
        return self.__expenditure_share

    @property
    def output_share(self):
        return self.__output_share

    @property
    def import_trade_costs(self):
        return self.__import_trade_costs

    @property
    def export_trade_costs(self):
        return self.__export_trade_costs

    # @property
    # def import_cost_by_expenditure_share(self):
    #     return self.__import_cost_by_expenditure_share

    # @property
    # def export_cost_by_output_share(self):
    #     return self.__export_cost_by_output_share

    __slots__ = [
        "__name",
        "__expenditure_share",
        "__output_share",
        "__import_trade_costs",
        "__export_trade_costs",
        "import_cost_by_expenditure_share",
        "export_cost_by_output_share"
    ]

    def __init__(self, name: str, expenditure_share: float, output_share: float, import_trade_costs: Dict[str, float], export_trade_costs: Dict[str, float]) -> None:
        if not isinstance(name, str):
            raise ValueError("name")

        if not isinstance(expenditure_share, float):
            raise ValueError("expenditure_share")

        if not isinstance(output_share, float):
            raise ValueError("output_share")

        if not isinstance(import_trade_costs, dict):
            raise ValueError("import_trade_costs")

        if not isinstance(export_trade_costs, dict):
            raise ValueError("export_trade_costs")

        if expenditure_share < 0:
            raise ValueError("expenditure_share")

        if output_share < 0:
            raise ValueError("output_share")

        if any((v < 0 for v in import_trade_costs.values())):
            raise ValueError("import_trade_costs")

        if any((v < 0 for v in export_trade_costs.values())):
            raise ValueError("export_trade_costs")

        self.__name = name
        self.__expenditure_share = expenditure_share
        self.__output_share = output_share
        self.__import_trade_costs = import_trade_costs
        self.__export_trade_costs = export_trade_costs
        self.import_cost_by_expenditure_share = dict([(key, expenditure_share * value) for key, value in import_trade_costs.items()])
        self.export_cost_by_output_share = dict([(key, output_share * value) for key, value in export_trade_costs.items()])

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return f"(name='{self.name}', expenditure_share='{self.expenditure_share}', output_share='{self.output_share}')"
