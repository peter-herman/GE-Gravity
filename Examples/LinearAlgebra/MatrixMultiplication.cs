using Xunit;

namespace MatrixMultiplication
{
    /// <summary>
    /// This class demonstrates a simple implementation of A * b where A is an m*n matrix and b is an n*1 vector.
    /// </summary>
    public static class MatrixMultiplication
    {
        /// <summary>
        /// Calculates the matrix product of A and b.
        /// </summary>
        /// <param name="a">
        /// The m*n matrix.
        /// </param>
        /// <param name="b">
        /// The n*1 vector.
        /// </param>
        /// <returns>
        /// The matrix product defined as A * b.
        /// </returns>
        public static double[] MatrixProduct(double[][] a, double[] b)
        {
            // Guard clauses ommitted for brevity.
            
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

        
        /// <summary>
        /// A unit test of MatrixProduct using the arrange-act-assert style.
        /// </summary>
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
            Assert.Equal(expected, result);
        }
    }
}