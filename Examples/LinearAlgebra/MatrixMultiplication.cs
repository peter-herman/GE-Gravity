using Xunit;

namespace MatrixMultiplication
{
    public static class MatrixMultiplication
    {
        public static double[] MatrixProduct(double[][] a, double[] b)
        {
            double[] result = new double[a.Length];

            for (int i = 0; i < a.Length; i++)
            {
                double sum = 0.0;

                for (int j = 0; j < a[i].Length; j++)
                {
                    sum += a[i][j] * b[j];
                }

                result[i] = sum;
            }

            return result;
        }

        public static void Test()
        {
            // Arrange
            double[][] a = 
                new double[][]
                {
                    new double[] { 1.0, 2.0, 3.0 }, 
                    new double[] { 4.0, 5.0, 6.0 }
                };
            
            double[] b = 
                new double[] { 1.0, 2.0, 3.0 };
            
            double[] expected = 
                new double[] { 14.0, 32.0 };
            
            // Act
            double[] result = MatrixProduct(a, b);

            // Assert
            Assert.Equals(expected, result);
        }
    }
}