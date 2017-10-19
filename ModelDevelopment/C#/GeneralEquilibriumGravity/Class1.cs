using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Linq;
using JetBrains.Annotations;

namespace GeneralEquilibriumGravity
{
    public class ModelResult
    {
        public string Country { get; }
        
        public double InwardResistance { get; }
        
        public double OutwardResistance { get; }
    }

    public class Country
    {
        public string Name { get; }
    }
    
    /// <summary>
    /// Represents a gravity model.
    /// </summary>
    public class Model : IEquatable<Model>
    {
        /// <summary>
        /// The collection of countries in the model.
        /// </summary>
        [NotNull]
        [ItemNotNull]
        private readonly Country[] _countries;

        /// <summary>
        /// The equation representing the model.
        /// </summary>
        [NotNull]
        private readonly Func<Country[], double[], double[]> _equation;
        
        /// <summary>
        /// The number of countries in the model.
        /// </summary>
        public int Count => _countries.Length;

        /// <summary>
        /// The collection of countries in the model.
        /// </summary>
        [NotNull]
        [ItemNotNull]
        public IEnumerable<Country> Countries =>  _countries;

        /// <summary>
        /// True if the previous solution was successful; otherwise false.
        /// </summary>
        public bool IsValid { get; private set; }

        /// <summary>
        /// The index of the country to which the results are normalized.
        /// </summary>
        public int NormalizedIndex => Array.IndexOf(_countries, NormalizedName);
        
        /// <summary>
        /// The name of the country to which the results are normalized.
        /// </summary>
        [NotNull]
        public string NormalizedName { get; }
        
        /// <summary>
        /// The time elapsed during the previous solution.
        /// </summary>
        public double Elapsed { get; private set; }

        /// <summary>
        /// Constructs a model from the given inputs.
        /// </summary>
        /// <param name="countries">
        /// The collection of countries in the model.
        /// </param>
        /// <param name="normalizedName">
        /// THe name of the country to which the results are normalized.
        /// </param>
        /// <param name="equation">
        /// The equation representing the model.
        /// </param>
        /// <exception cref="ArgumentNullException" />
        public Model([NotNull][ItemNotNull] IEnumerable<Country> countries, [NotNull] string normalizedName, [NotNull] Func<Country[], double[], double[]> equation)
        {
            if (countries is null)
            {
                throw new ArgumentNullException(nameof(countries));
            }
            if (normalizedName is null)
            {
                throw new ArgumentNullException(nameof(normalizedName));
            }
            if (equation is null)
            {
                throw new ArgumentNullException(nameof(equation));
            }
               
            _countries = countries.ToArray();
            _equation = equation;
            NormalizedName = normalizedName;
        }

        /// <summary>
        /// Solves the model.
        /// </summary>
        /// <returns></returns>
        [NotNull]
        [ItemNotNull]
        public IEnumerable<ModelResult> Solve()
        {

            return Enumerable.Empty<ModelResult>();
        }

        /// <summary>
        /// Returns a string that represents the current object.
        /// </summary>
        /// <returns>
        /// A string that represents the current object.
        /// </returns>
        public override string ToString()
        {
            return $"(NormalizedName: {NormalizedName}, Success: {IsValid}, Elapsed: {Elapsed})";
        }

//        def solve(self, x0: Sequence[float] = None, method: str = "hybr", tol: float = 1e-8, xtol: float = 1e-8, maxfev: int = 1400) -> Sequence[ModelResult]:
//    
//            if x0 is None:
//                x0 = np.ones(2 * len(self.__countries))
//    
//            if not isinstance(x0, np.ndarray):
//                x0 = np.asarray(x0)
//    
//            if len(x0) != 2 * len(self.__countries):
//                raise ValueError(f"Expected sequence of {2 * len(self.__countries)} values, but received {len(x0)} values.")
//    
//            start = time()
//    
//            results = root(fun=self.__equation, x0=x0, method=method, tol=tol, options={"xtol": xtol, "maxfev": maxfev})
//    
//            self.__time_elapsed = time() - start
//            self.__is_valid = results.success
//    
//            return self.__normalize_baseline(results.x)
//    
//        def __wrap_equation(self, equation: Callable[[List[Country], List[float]], List[float]]) -> Callable[[List[float]], List[float]]:
//            """
//            This function wraps the user-defined delegate to handle normalizing to the specified country.
//            :param equation: The user-defined delegate.
//            :return: A function suitable for use in the solve() function.
//            """
//    
//            bound_function = partial(equation, self.__countries)
//            normalized_index = self.normalized_index
//    
//            def __wrapped_function(x: List[float]) -> List[float]:
//                x[normalized_index] = 1.0
//                result = bound_function(x)
//                result[normalized_index] = 0.0
//                return result
//    
//            return __wrapped_function
//    
//        def __normalize_baseline(self, results: Sequence[float]) -> Sequence[ModelResult]:
//            """
//            This function takes the raw results from the optimization routine and constructs a list of tuples to return to the user.
//            :param results: The results of the optimization.
//            :return: A list of tuples containing inward and outward multilateral resistance terms by country.
//            """
//    
//            if not isinstance(results, list):
//                results = list(results)
//    
//            count = len(self.__countries)
//    
//            inward_resistances = (x for x in results[:count])
//    
//            outward_resistances = (x for x in results[count:])
//    
//            names = (x.name for x in self.__countries)
//    
//            return [ModelResult(x[0], x[1], x[2]) for x in iter(zip(names, inward_resistances, outward_resistances))]
        
        /// <summary>
        /// Indicates whether the current object is equal to another object of the same type.
        /// </summary>
        /// <param name="other">
        /// An object to compare with this object.
        /// </param>
        /// <returns>
        /// True if the current object is equal to the <paramref name="other" /> parameter; otherwise, false.
        /// </returns>
        public bool Equals(Model other)
        {
            if (ReferenceEquals(null, other))
            {
                return false;
            }
            if (ReferenceEquals(this, other))
            {
                return true;
            }
            
            return _countries.Equals(other._countries) && _equation.Equals(other._equation) && string.Equals(NormalizedName, other.NormalizedName);
        }

        /// <summary>
        /// Determines whether the specified object is equal to the current object.
        /// </summary>
        /// <param name="obj">
        /// The object to compare with the current object.
        /// </param>
        /// <returns>
        /// True if the specified object  is equal to the current object; otherwise, false.
        /// </returns>
        public override bool Equals(object obj)
        {
            if (ReferenceEquals(null, obj))
            {
                return false;
            }
            if (ReferenceEquals(this, obj))
            {
                return true;
            }
            
            return obj.GetType() == GetType() && Equals((Model) obj);
        }

        /// <summary>
        /// Serves as the default hash function.
        /// </summary>
        /// <returns>
        /// A hash code for the current object.
        /// </returns>
        public override int GetHashCode()
        {
            unchecked
            {
                int hashCode = _countries.GetHashCode();
                hashCode = (hashCode * 397) ^ _equation.GetHashCode();
                hashCode = (hashCode * 397) ^ NormalizedName.GetHashCode();
                return hashCode;
            }
        }

        /// <summary>
        /// Returns a value that indicates whether the values of two <see cref="GeneralEquilibriumGravity.Model"/> objects are equal.
        /// </summary>
        /// <param name="left">
        /// The first value to compare.
        /// </param>
        /// <param name="right">
        /// The second value to compare.
        /// </param>
        /// <returns>
        /// True if the <paramref name="left" /> and <paramref name="right" /> parameters have the same value; otherwise, false.
        /// </returns>
        public static bool operator ==(Model left, Model right)
        {
            return Equals(left, right);
        }

        /// <summary>
        /// Returns a value that indicates whether two <see cref="GeneralEquilibriumGravity.Model" /> objects have different values.
        /// </summary>
        /// <param name="left">
        /// The first value to compare.
        /// </param>
        /// <param name="right">
        /// The second value to compare.
        /// </param>
        /// <returns>
        /// True if <paramref name="left" /> and <paramref name="right" /> are not equal; otherwise, false.
        /// </returns>
        public static bool operator !=(Model left, Model right)
        {
            return !Equals(left, right);
        }
    }
}