class: center, middle

# Programming Meeting 1

Austin Drenski

7 August 2017

---
# Agenda
1. Introduction
2. Objectives
3. Structure
4. Supported languages
5. Programming with Data
6. Programming with Functions

---
# Introduction

---
# GE Gravity Objectives
- Robust solution techniques
- Modular and extensible
- Stable and secure
- Shippable and scriptable
- Traceable and reproducible
- Open and free
---
# Project Structure
- Base libraries
  - Targeting .NET Standard 2.0+

- API server
  - Kestrel server – modern, lightweight, high performance
  - Centrally hosted or locally deployable

- Interactive layer
  - Desktop application
  - Web application
  - Scriptable from any .NET supported language
---
# Project Supported Languages
- C#
  - Object-oriented (OOP)
  - Strongly-typed
  - Compiled
- F#
  - Functional (FP)
  - Strongly-typed
  - Compiled or interpreted
- Python
  - Object-oriented (OOP)
  - Dynamically-typed
  - Interpreted
---
# Project Supported Languages
- C#
  - Object-oriented (OOP) __+ multi-paradigm__
  - Strongly-typed __+ implicit and dynamic typing__
  - Compiled __+ interpreted scripting__
- F#
  - Functional (FP) __+ multi-paradigm__
  - Strongly-typed __+ implicit and dynamic typing__
  - Compiled or interpreted
- Python
  - Object-oriented (OOP) __+ multi-paradigm__
  - Dynamically-typed
  - Interpreted __+ trans-compilation__
---
# Why are we supportting multiple languages?
- The supported languages _approach_ problems differently
- Productivity is programmer-dependent, not the language-dependent
- Pick the language that you are most excited to learn
???
- The idea is for you to find the language that best helps you think about complex problems.
- I enjoy working in C# because everything is _explicit_. Scope, variable type, and outcomes are _known_ at compile time. 
- You may, however, find that the development process in C# is _too_ explicit. If so, F# may appeal to you as a strongly-typed language with the flexibility normally only found in scripted languages.
- And still, you may decide that the problems you need to solve are empheral, and do not benefit from a well-structured solution. In these cases, Python can offer rapid prototyping with acceptable performance margins.
---
# Should you learn all of these languages?
- I will provide support for all of three languages--including translation where necessary.
- I encourage everyone to develop at least a base literacy in each language. 
- This will support team-wide code review and visibility.
- These meetings are intended to develop this base level of understanding, __so questions are encouraged.__
---
# Programming with Data
- Object-oriented programming (OOP):
  - Data are represented by objects that store data and define behavior

- Functional programming (FP):
  - Data are represented by records that store data
  - Functions are applied to data structures
---
# Programming with Data: Classes
- All three languages support OOP with class objects.
- Classes are a definition, objects are an instance of a class definition.
  - _This definition is overly broad, but sufficient for this section. We'll revisit this definition in another presentation._
- Assume that there is a class named `Example` and _instances_ of the class are objects of _type_ `Example`.
---
# Programming with Data: Classes in C#
```c#
/// <summary>
/// Represents an example.
/// </summary>
public class Example
{
    /// <summary>
    /// The value of the example.
    /// </summary>
    public int Value { get; set; }
    
    /// <summary>
    /// Constructs an example with the given value.
    /// </summary>
    /// <param name="value">
    /// The value to be assigned to the example.
    /// </param>
    public Example(int value)
    {
        Value = value;
    }
    
    /// <summary>
    /// Returns true if the value is greater than zero; otherwise false.
    /// </summary>
    public bool HasNonZeroValue()
    {
        return Value > 0;
    }
}
```
???
- Here is an example class--conviently named `Example`--written in C#. This class definition describes a box that holds an integer. 
- That's all objects are in context: boxes that hold values. 
- The difference between objects and arrays--both of which can hold integers--is that the object gives us more __context__ about the stored value. 
---
# Programming with Data: Classes in F#
```f#
/// <summary>
/// Represents an example.
/// </summary>
type Example(value : int) = 
    
    /// <summary>
    /// The value of the example.
    /// </summary>
    member val Value : int = value with get, set
    
    /// <summary>
    /// Returns true if the value is greater than zero; otherwise false.
    /// </summary>
    member this.HasNonZeroValue()
        return Value > 0 
```
???
- Here is the same example class as before, but now translated to F#.
- This definition is equivalent to the example in C#. 
- The __only__ difference is with how the languages describe the world.
---
# Programming with Data: Classes in Python
```python
class Example:
    """
    Represents an example.
    """
    
    def __init__(self, value):
        """
        Constructs an example with the given value.
        :param value: The value to be assigned to the example.
        """
        
        self.value = value
        
    def has_non_zero_value(self):
        """
        Returns true if the value is greater than zero; otherwise false.
        """
        
        return self.value
```
---
# Programming with Functions
- Object-oriented programming (OOP):
  - Methods are members of classes (instance or static)
  - Functions are a type (e.g. a class)

- Functional programming (FP):
  - Functions should be pure (e.g. no side effects)
???
- If you spend any time reading about these concepts on the internet, you will probably find more than a few heated debates between object-oriented and functional purists.
- The key to remember is that both styles have a role to play, which is why aspects of each style appear in _all_ of the languages we are discussing.
- The style you choose should be determined by the buisness case and the algorithm you are implementing.
---
# Programming with Functions
- All three languages support methods on class objects.
- All three languages support lambda functions – more on this later.
- The class Example has an instance method named HasNonZeroValue. 
- Every Example object has its own instance of HasNonZeroValue.
---
