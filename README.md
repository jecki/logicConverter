logicConverter
==============

logicConverter - Converts logical formulae between different notations.

This software is open source software under the Apache 2.0-License.

Copyright 2016-2022  Eckhart Arnold <arnold@badw.de>, Bavarian Academy of Sciences and Humanities

First use case is going to be the translation of formulae in the historical 
notation of the "Principia Mathematica" as used by Bertrand Russel and Rudolf Carnap
into notations used by contemporary text-books as well as modern computer algebra
systems.

Status
------

As of now, logicConverter is in an early pre-alpha-stage and serves as best as a rough proof of concept.
It can convert some formulars from the Principia Mathematica into:

  1. Abstract Syntax Trees (AST) which conserve the structure of the principia-notation
  2. Logical Syntax Trees (LST) which represent the "mathematical object" described in
     the principia-notation, but do not conserve the notational structure of the principia
  3. Modern-notation-representations of the "mathematical objects" described in the
     principia-notation
  4. TeX-representation of the original principia mathematica notation 

Have a look at "Example.md" to see what this means or run the "tst_principia_grammar.py"-script 
in this directory by typing "python tst_principia_grammar.py" on the command line to produce 
some examples in the "tests_grammar/REPORT" sub-directory!

Requires the latest development branch of [DHParser](https://gitlab.lrz.de/badw-it/DHParser/-/tree/development)!

License
-------

logi is open source software under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0)

Copyright 2022 Eckhart Arnold <arnold@badw.de>, Bavarian Academy of Sciences and Humanities

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    https://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
