# namespace: matrix_multiplication

def matrix_multiplication(a, b):
    result = [None] * len(a)

    for i in range(len(a)):
        sum = 0.0

        for j in range(len(b)):
            sum += a[i][j] * b[j]

        result[i] = sum

    return result


def test():
    # Arrange
    a = [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]]

    b = [1.0, 2.0, 3.0]

    expected = [14.0, 32.0]

    # Act
    result = matrix_multiplication(a, b)

    # Assert
    assert expected == result