# CSG Style Guide

This is the CSG Style Guide. It governs the coding style of this project.
Make sure that you adhere to these guidelines, before submitting a
pull-request.

### Python Code

[PEP 8](https://www.python.org/dev/peps/pep-0008/) is followed wherever
appropriate. Here are the highlights:

* Indentation is 4 **spaces**.

* Each substantial new function **must** have a doc-string at the
beginning of the function. Doc-strings should only be used for this
purpose.

* There should be no space after function name and parameter list.

* Use type hints.

* The following operators must have spaces wrapping around them:

   `= += -= /= *= //= * ** / // + - == > < >= <= ->`

* Commas should have at least one space following them.

* Please try to adhere to the 79-character line length limit.
This makes it easier to have multiple terminals/text-editors open,
without unnecessary line-wrapping.

* Important variables should be named properly. Use snake case,
ie. underscores as word separators. Do not use camelCase/PascalCase.

  ```python
  # Avoid this:
  someVar = 20
  SomeVar = 20

  # Use this instead:
  some_var = 20
  ```

  There are exceptions of course. Don't name counters
  `this_is_a_loop_counter`, and temporary variables
  `this_is_a_temporary_variable`. `i` and `tmp` would suffice.

* Wherever possible, break up the definition of a dictionary into
multiple lines, as follows:
  ```python
  some_dict = {
      "key1": "val1",
      "key2": "val2",
      "key3": "val3",
      "key4": "val4"
  }
  ```
* Avoid global variables.
* Strip all trailing white-spaces.

### Example

The following snippet of code follows all the above guidelines.

```python
def some_function(param1: int, param2: int) -> int:
    """
    some_function():
    	Useless function that returns param1 after
    	running a useless loop to make param1 = param2
    """

    # Loop until equal
    while param1 != param2:
        if param1 < param2:
            param1 += 1
        else:
            param1 -= 1

    return param1
```
