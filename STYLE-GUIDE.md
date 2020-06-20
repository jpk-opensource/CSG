# CSG Style Guide

This is the CSG Style Guide. It governs the coding style of this project. Make sure that you adhere to these guidelines, before submitting a pull-request.

### Python Code

* Indentation is 4 **spaces**.

* Each substantial new function **must** have a doc-string at the beginning of the function. Doc-strings should only be used for this purpose.

* There should be no space after function name and parameter list.

* The following operators must have spaces wrapping around them:

   `=, +=, -=, /=, *=, //=, *, **, /, //, +, -, ==, >, <, >=, <=  `

* Commas should have at least one space following them.

* Wherever possible, comments should precede the line/lines that it is explaining, ie.

  ```python
  some_var = 5  # Avoid this type of comment wherever possible
  
  # This is preferrable
  some_other_var = 6
  ```

* Please try to adhere to the 80-character line length limit. This makes it easier to have multiple terminals/text-editors open, without unnecessary line-wrapping. This is the rationale for the comment style as well.

* Important variables should be named properly. Use underscores as word separators. Please avoid camel-case in identifiers, ie.

  ```python
  # Avoid this:
  someVar = 20
  
  # Use this instead:
  some_var = 20
  ```

* There are exceptions of course. Don't name counters `this_is_a_loop_counter`, and temporary variables `this_is_a_temporary_variable`. `i` and `tmp` would suffice.
* Avoid global variables.
* Strip all trailing white-spaces

### Example

The following snippet of code follows all the above guidelines.

```python
def some_function(param1, param2):
    """
    some_function():
    	Useless function that returns param1 after
    	running a useless loop to make param1 = param2
    """
    # Loop until equal
    while param1 < param2:
        param1 += 1
    
    return param1
```