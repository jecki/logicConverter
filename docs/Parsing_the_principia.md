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
what for and why (in my opinion) they should be used. 

The discussion will mostly focus on historical texts making use of
formal logic in the Russell-Peano-Notation that was common in the first
half of the 20th century before it morphed into the notation that is
customary today. Some notable works that made use of the
Russell-Peano-Notation are Bertrand Russell's and Alfred North
Whitehead's "Principia Mathematica", Rudolf Carnaps "Der logische Aufbau
der Welt" und "Logische Syntax der Sprache" and Willard van Ornam Quines
Inroduction to Logic. However, much of what is said will also apply to
other kinds of mathematical formulae.

In the practical part I explain step by step how to build a parser and
converter for logical formulae following the now historical notation of
Russell and Peano with the Python programming language. If you are only
interested in a little lesson on how to write a formal grammar for a
logical notation and how to derive a parser and converter from this
grammar, you can directly skip to the second, the practical part.



Editing formulae digitally
--------------------------

There are many ways in which digital technologies can enhance the
capabilities of editors dealing with formulaic content. Among others:

1. Digital technologies allow to present one and the same text in
   several different forms within one and the same edition.

2. They furthermore simplify producing these different versions
   by partly or fully automizing the conversion process.

3. They enable other forms of (re-)use than, even this may still be the
   considered the most important one, just being consumed by human
   readers. For example, the mathematical or logical could be exported
   data-formats for computer-algebra-systems or proof-verifiers. 

Each of these will (briefly) be discussed in the following.

### Offering the formulaic content in different shapes

The purpose of scientific editions in general is to deliver historical
works in a form that makes them directly accessible and readily usable
(in a scientific context) to contemporary readers. Before digital
technology was available this often required editors to make difficult
decision on how far the shape of a historical text should be modernized
to suite different groups of potential readers. And this often used to
be an either-or question. 

If we think of a logical text or a philosophical text containing a lot
of formal logic, then historically interested readers will probably
prefer to read the formulae in its original form, while readers mostly
interested in the systematic content might find a modernized form of the
formulae much more convenient. The same is probably also true for
new-comers or students who will probably find the modernized form easier
to understand an thus prefer it at least on first reading.

Luckily a digital edition can easily serve both groups of readers by
presenting several versions of the same text, a version that preserves
the historical form and shape of the formulae and a version where these
have been cast in a modernized form. If it had been intended to produce
a modern version at all, the extra work required will be moderate,
because the historical form will most likely be produced during editing,
anyway, as a first stage towards the final version. (And a good
rationale, read "economic justification", for adding the production of a
modernized version to the edition-project is that if more than one
reader is interested in such a version than its best if the required
work to produce one is only done once, by the editor, and this properly,
instead of every user tinkering withe a makeshift modernization by him-
or herself. After all, this is the point of an edition-project, or
isn't it?) 

### Automatizing the conversions with parsing-technology

Still, producing several versions of a text (or its formulaic content
for that matter) requires extra work. But this again, is a challenge
that can very well be met with digital technology. I believe that at
least as long as the different forms are historically, or, rather,
paradigmatically not too remote from each other, the required conversion
of formulae can be performed by the computer. At least for the
Russell-Peano-Notation and contemporary logical notation this is most
certainly possible as I shall demonstrate in the practical part. It can
be achieved with ordinary parser technology like
parsing-expression-grammars (PEGs). (Beware, though, despite being
well-established and in this sense "ordinary", PEGs require quite a 
bit of practice before they are fully mastered.)

### Providing machine-readable formulae
