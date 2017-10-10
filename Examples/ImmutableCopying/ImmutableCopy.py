class MyObject(object):
    __slots__ = [
        "__value",
        "__shocked_value"
    ]

    @property
    def value(self):
        return self.__value

    @property
    def shocked_value(self):
        return self.__shocked_value

    def __init__(self, value: float, shocked_value: float = 0) -> None:
        self.__value = value
        self.__shocked_value = shocked_value

    def shock(self, value: float) -> 'MyObject':
        """
        Returns a new object representing the current object shocked by the value.
        :param value: The value for the shocked value variable.
        :return: A new object representing the current object shocked by the value.
        """
        return MyObject(self.__value, value)

    def clone(self) -> 'MyObject':
        """
        Clones the current object.
        :return: A clone of the current object.
        """
        return MyObject(self.__value, self.__shocked_value)

    def __str__(self) -> str:
        """
        Returns a string representation of the current object.
        :return: a string representation of the current object.
        """
        return self.__repr__()

    def __repr__(self) -> str:
        """
        Returns a string representation of the current object.
        :return: a string representation of the current object.
        """
        return "(value: {0}, shocked_value: {1})".format(self.__value, self.__shocked_value)


a = MyObject(5)
b = a.clone()
c = b.shock(7)

print(a)
print(b)
print(c)

print(a.shocked_value)

a.shocked_value = 10
