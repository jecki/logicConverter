Parsing the Principia
=====================

Scientific Editions of historical texts that contain mathematical or
logical formulae pose specific challenges for the editor. The
typesetting may be complicated because ready-to-use solution for
typesetting formulae only support modern notations, the historical
notations may not be accessible to modern readers, reading and typing
formulae without errors can require considerably more attention on the
side of the editor than editing prose text.

At the same time digital technologies vastly expand the possibilities
not only for capturing and entering formulae into an edition but also
for presenting them to the readers or even re-using them in different
contexts.

In the following, I am going to discuss how parsers and converters for
logical formulae in particular can help creating rich digital editions
of texts that are full of formulaic content. The discussion has a
theoretical and practical part. In the theoretical part I discuss how
these technologies can be used to enhance digital editions as well as
what for and why (in my opinion) they should be used. In the practical
part I explain step by step how to build a parser and converter for
logical formulae following the now historical notation of Russell and
Peano with the Python programming language. If you are only interested
in a little lesson on how to write a formal grammar for a logical
notation and how to derive a parser and converter from this grammar,
you can directly skip to the second, the practical part.



