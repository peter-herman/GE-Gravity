# Unit Testing Examples

This directory contains examples on how to structure class files and write unit tests to accompany them.

## Why write unit tests?

Unit tests are similar to the concept of writing a mathematical proof. Well-written unit tests serve as a proof that your code is robust.

## But I write good code. Why should I bother?

Unit tests are like seat belts. Even if you trust your code, write them as an insurance policy against external failures.

## Getting started

It is common to structure a unit test with three sections:
- _Arrange_:
  - Construct local resources for the test.
- _Act_:
  - Perform some action that tests a single piece of logic.
- _Assert_:
  - Verify that the action returned the expected result.