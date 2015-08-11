CategorizeSignals
=================

Assign categories to posts based on a regular expression search

Properties
----------
-   **Attribute to Set**: Attribute to set *Category to Assign* to on Signal.
-   **Match String**: String to evaluate each regex pattern against.
-   **Categories**: List of categories and regex patterns.
    -   **Category to Assign**: Category to append to *Attribute to Set* if there is a match.
    -   **Regular Expression Patterns**: List of regular expression patterns. The category is considered a match if any of these patterns are found in the *Match String*.

Dependencies
------------
None

Commands
--------
None

Input
-----
Any list of signals.

Output
------
Same list of signals as input with the added attribute *Attribute to Set* as defined in the configuration. *Attribute to Set* is a list with a category appended to it for each matching *Category* with a corresponding matching *Regular Expression Pattern*.

If *Attribute to Set* already exists on the input signal and it is not a list then the blocks logs an error and the signal is not modified.
