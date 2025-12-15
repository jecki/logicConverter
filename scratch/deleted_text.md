# 1

As it is a bit difficult to read such a verbose syntax-tree, it is probably the right time to introduce a few simple techniques to streamline the output of the parser. The present syntax-tree appears to be unnecessarily verbose in several respects. (Feel free to skip the following list for now, in case you are not particularly interested in the details of the high art of tree-trimming):

1. The concrete syntax-tree faithfully records every character from the source text including the **whitespace** characters, which were only used to make the formula more readable. These are found in "anonymous" nodes named ":Whitespace". It might sound like a contradictio in adiecto than an anonymous node should have a name. It is anonymous in the sense that it does not bear the name of a particular rule in the grammar that generated this node, but only the class name for the kind of parser that generated the node precceded by a colon ":" which is the marker by which DHParser distinguishes "named" nodes from "anonymous" nodes. (If you till do not like the term "anynomous", you can also think of these nodes as going "incongnito" with resepct to the set of symbols defined in the grammar.) 

    ":Whitespace"-nodes (can) appear wherever there is a tilde sign "~" in the grammar. It is actually true for *any* grammar that the ":Whitespace"-nodes that appear in the concrete syntax-tree can safely (i.e. without loss of any relevant content) be dropped from the tree - as long as the convention has been observed faithfully that the tilde sign is reserved for insignificant whitespace. 

    Be aware that whitespace is not necessarily insignificant. If you parse a piece of prose text, the whitespace between words is highly relevant: While "2 + 4 * 3" is essentially the same as "2+4*3", "Tell all the truth but tell it slant" is not the same as "Tellallthetruthbuttellitslant". The designer of a grammar should be careful to use the tilde sign "~" only for whitespace that is insignificant and to introduce a new symbol, at best a short simple symbol like L or S, for whitespace that is relevant.

2. But it is not only the nodes representing insignificant whitespace that can be dropped. Also, the **tokens** with the signs for the four basic arithmetic operations, "+", "-", "*" and ":", can safely be dropped from the syntax-tree as well, because the information they carry is already contained in the name of their parent node, e.g "addition", "substraction", "multiplcation" and "division". This would not have been possible with the earlier iterations of the grammar, because there we only had expression or term-branches, but in order to decide whether an expression branch in the syntax-tree represents an addition or a substraction, we would still have to look at the token (i.e. the ":Text"-node) among its children.

    In fact, we can drop all string literals from the syntax-tree, because our string literals are either basic arithmetic operations or **delimiters**, namely, the parentheses for grouping. (Generally, delmiters are demarkation signs for structural entities in a serialized data structure. Of course, just like in the case of other tokens, delimiters can only be dropped if the structural entities they demark are represented as independent entities in the syntax-tree. However, other than in the case of non-delimiter tokens, this is almost naturally the case and therefore harder to get wrong.) 

    Note that while it is certainly not generally true that all ":Text"-nodes stemming from string literals can be dropped, it is usually possible to write a grammar in such a way that string literals are only used for disposable entities (like delimiters) and regular expressions are used for all those parts of the source text that are still needed in the abstract syntax-tree. This is, by the way, also the reason why the zero in the rule for "number" was defined as the regular expression `/[0]/` instead of the simple string literal `"0"` in the grammar above. 

3. Apart from dropping unneeded nodes, entirely, another class of typical tree-simplifications revolves around dissolving nodes by adding or moving their content to other nodes and, thus, eliminating a layer in the hierarchy or merging siblings without dropping any content. A most obvious case is that of a named node containing a single anonymous child, e.g. `(number (:RegExp "2"))` which can safely be reduced to `(number "2")`. This simplification is so "safe" that DHParser does it without even asking. If you pay close attention, you will notice that the very last "factor"-node in the syntax-tree above contains a number node that directly stores the numeral value, while the other number nodes in the tree have two children (":Regexp" and ":Whitespace"). That is, because the last number was not followed by any whitespace and DHParser could, therefore, reduce the nested `(:RegExp "2")` to its parent number-node. ("Reducing" here means taking the content of a single child and then dropping the child node itself, while "replacing" would bean that the child node replaces the parent node. In the first case the child node is dissolved, in the second case it is the parent that gets dissolved.)

    Once the whitespace has been dropped from the syntax-tree, the other ":RegExp"-nodes can also be reduced to their parent number-node. Only, DHParser won't do so without having been explicitly instructed to do so, because this involves changes to the content-string of the tree. (The "content" of the tree is the merged text-content of all its leaf-nodes, i.e. those nodes that nod have children.)

    Replacing the parent nodes by sole child nodes makes sense in all cases where the parent node stems from a grammar rule that resembles an exclusive collective term like, in our example, "expression", "term" and "factor". (Exclusive here means that none of the alternatives by which it is defined occurs in the definition of any other collective term in the grammar - which can easily be verified.) 

If we apply all possible reductions and replacements subsequently from the inside out, the syntax-tree will greatly be simplified. In our case this is all we need to do to arrive at a proper abstract syntax-tree for arithmetic formulae. Now, while it is possible to apply all these tree-trimming techniques after the parser has produced the concrete syntax-tree, it would be much more efficient to do so while parsing already, so that the unneeded nodes are not even produced in the first place. For this purpose DHParser allows to ammend the grammar with annotations (or "directives") in order to simplify the syntax-tree already while parsing. This works with all of the tree-trimming techniques described above. Other tree-trimming techniques not described here can only be applied after the syntax-tree has been produced. Therefore, in typical real-world applications which are more complex than the simple arithmetic example presented here, usually a mixture of "early" and "late" tree-trimming will be used. We will see this when writing a parser for the Russell-Peano notation. For our arithmetic example, however, adding the following two directives at the top of the grammar will suffice: 

    @drop = whitespace, strings
    @hide = expression, term, factor

The directive `@drop = whitespace, strings` instructs DHParser to drop all nodes produced by the tilde sign "~" in the grammar, which is reserved for insignificant whitespace, as well as all nodes produced by string literals in the grammar. Please observe that "whitespace" and "strings" are class names, not symbol names. (In case you are wondering how to instruct DHParser to drop nodes produced by a rule "whitespace" that has been defined in the grammar, the answer is that you cannot. You either have to drop these nodes after parsing or you have to give it a different name. As DHParser distinguishes upper and lower case letters, naming it "Whitespace" would have been sufficient. The same goes for "strings", "regexps" and "backticked" and thats all. DHParser will warn you about possible conflicts.)

The directive `@hide = expression, term, factor` instructs DHParser to replace by a single child or reduce to its parent if a single child (whatever of these two is possible) any node with the name "expression", "term" or "factor". Essentially this directive instructs DHParser to tread nodes with these names just like anonymous nodes. Let's see how these two instructions lead to a greatly simplified syntax-tree:

    (formulae (subtraction (subtraction (number "5") (number "2")) (number "1")))


# 2

Now, there is one last rule that, however, instead of trimming the tree, simplifies writing the grammar by reducing visual noise. You might have noticed that after ever string literal the tilde sign `~` for insignificant whitespace follows. Specifically, for string-literals DHParser allows adding the directive `@literalws = right` which instructs DHParser when generating a parser from a grammar to assume insignificant whitespace on the right-hand side of every string-literal. Thus, our fully streamlined grammar reads:

      @literalws = right                  # silently eat whitespace to the right of any string literal
      @drop = whitespace, strings         # drop insignificant whitespace and all string literals
      @hide = expression, term, factor, group # replace these by their (single) child
      
      formulae = ~ expression { expression }
      
      expression = addition | subtraction | term
        addition    = expression "+" term
        subtraction = expression "-" term
      
      term       = multiplication | division | factor
        multiplication = term "*" factor
        division       = term ":" factor
      
      factor = group | number
        group  = "(" expression ")"
        number = /0/~ | /[1-9]/ { /[0-9]/ } ~