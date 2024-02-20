

Test of parser: "database"
==========================


Match-test "M1"
----------------

### Test-code:

    $( Declare the constant symbols we will use $)
        $c 0 + = -> ( ) term wff |- $.
    $( Declare the metavariables we will use $)
        $v t r s P Q $.
    $( Specify properties of the metavariables $)
        tt $f term t $.
        tr $f term r $.
        ts $f term s $.
        wp $f wff P $.
        wq $f wff Q $.
    $( Define "term" and "wff" $)
        tze $a term 0 $.
        tpl $a term ( t + r ) $.
        weq $a wff t = r $.
        wim $a wff ( P -> Q ) $.
    $( State the axioms $)
        a1 $a |- ( t = r -> ( t = s -> r = s ) ) $.
        a2 $a |- ( t + 0 ) = t $.
    $( Define the modus ponens inference rule $)
        ${
            min $e |- P $.
            maj $e |- ( P -> Q ) $.
            mp  $a |- Q $.
        $}
    $( Prove a theorem $)
        th1 $p |- t = t $=
    $( Here is its proof: $)
        tt tze tpl tt weq tt tt weq tt a2 tt tze tpl
        tt weq tt tze tpl tt weq tt tt weq wim tt a2
        tt tze tpl tt tt a1 mp mp
    $.

### AST

    (database
      (outermost_scope_stmt
        (constant_stmt
          (constant
            (MATH_SYMBOL "0"))
          (constant
            (MATH_SYMBOL "+"))
          (constant
            (MATH_SYMBOL "="))
          (constant
            (MATH_SYMBOL "->"))
          (constant
            (MATH_SYMBOL "("))
          (constant
            (MATH_SYMBOL ")"))
          (constant
            (MATH_SYMBOL "term"))
          (constant
            (MATH_SYMBOL "wff"))
          (constant
            (MATH_SYMBOL "|-"))))
      (outermost_scope_stmt
        (stmt
          (variable_stmt
            (variable
              (MATH_SYMBOL "t"))
            (variable
              (MATH_SYMBOL "r"))
            (variable
              (MATH_SYMBOL "s"))
            (variable
              (MATH_SYMBOL "P"))
            (variable
              (MATH_SYMBOL "Q")))))
      (outermost_scope_stmt
        (stmt
          (hypothesis_stmt
            (floating_stmt
              (LABEL "tt")
              (typecode
                (constant
                  (MATH_SYMBOL "term")))
              (variable
                (MATH_SYMBOL "t"))))))
      (outermost_scope_stmt
        (stmt
          (hypothesis_stmt
            (floating_stmt
              (LABEL "tr")
              (typecode
                (constant
                  (MATH_SYMBOL "term")))
              (variable
                (MATH_SYMBOL "r"))))))
      (outermost_scope_stmt
        (stmt
          (hypothesis_stmt
            (floating_stmt
              (LABEL "ts")
              (typecode
                (constant
                  (MATH_SYMBOL "term")))
              (variable
                (MATH_SYMBOL "s"))))))
      (outermost_scope_stmt
        (stmt
          (hypothesis_stmt
            (floating_stmt
              (LABEL "wp")
              (typecode
                (constant
                  (MATH_SYMBOL "wff")))
              (variable
                (MATH_SYMBOL "P"))))))
      (outermost_scope_stmt
        (stmt
          (hypothesis_stmt
            (floating_stmt
              (LABEL "wq")
              (typecode
                (constant
                  (MATH_SYMBOL "wff")))
              (variable
                (MATH_SYMBOL "Q"))))))
      (outermost_scope_stmt
        (stmt
          (assert_stmt
            (axiom_stmt
              (LABEL "tze")
              (typecode
                (constant
                  (MATH_SYMBOL "term")))
              (MATH_SYMBOL "0")))))
      (outermost_scope_stmt
        (stmt
          (assert_stmt
            (axiom_stmt
              (LABEL "tpl")
              (typecode
                (constant
                  (MATH_SYMBOL "term")))
              (MATH_SYMBOL "(")
              (MATH_SYMBOL "t")
              (MATH_SYMBOL "+")
              (MATH_SYMBOL "r")
              (MATH_SYMBOL ")")))))
      (outermost_scope_stmt
        (stmt
          (assert_stmt
            (axiom_stmt
              (LABEL "weq")
              (typecode
                (constant
                  (MATH_SYMBOL "wff")))
              (MATH_SYMBOL "t")
              (MATH_SYMBOL "=")
              (MATH_SYMBOL "r")))))
      (outermost_scope_stmt
        (stmt
          (assert_stmt
            (axiom_stmt
              (LABEL "wim")
              (typecode
                (constant
                  (MATH_SYMBOL "wff")))
              (MATH_SYMBOL "(")
              (MATH_SYMBOL "P")
              (MATH_SYMBOL "->")
              (MATH_SYMBOL "Q")
              (MATH_SYMBOL ")")))))
      (outermost_scope_stmt
        (stmt
          (assert_stmt
            (axiom_stmt
              (LABEL "a1")
              (typecode
                (constant
                  (MATH_SYMBOL "|-")))
              (MATH_SYMBOL "(")
              (MATH_SYMBOL "t")
              (MATH_SYMBOL "=")
              (MATH_SYMBOL "r")
              (MATH_SYMBOL "->")
              (MATH_SYMBOL "(")
              (MATH_SYMBOL "t")
              (MATH_SYMBOL "=")
              (MATH_SYMBOL "s")
              (MATH_SYMBOL "->")
              (MATH_SYMBOL "r")
              (MATH_SYMBOL "=")
              (MATH_SYMBOL "s")
              (MATH_SYMBOL ")")
              (MATH_SYMBOL ")")))))
      (outermost_scope_stmt
        (stmt
          (assert_stmt
            (axiom_stmt
              (LABEL "a2")
              (typecode
                (constant
                  (MATH_SYMBOL "|-")))
              (MATH_SYMBOL "(")
              (MATH_SYMBOL "t")
              (MATH_SYMBOL "+")
              (MATH_SYMBOL "0")
              (MATH_SYMBOL ")")
              (MATH_SYMBOL "=")
              (MATH_SYMBOL "t")))))
      (outermost_scope_stmt
        (stmt
          (block
            (stmt
              (hypothesis_stmt
                (essential_stmt
                  (LABEL "min")
                  (typecode
                    (constant
                      (MATH_SYMBOL "|-")))
                  (MATH_SYMBOL "P"))))
            (stmt
              (hypothesis_stmt
                (essential_stmt
                  (LABEL "maj")
                  (typecode
                    (constant
                      (MATH_SYMBOL "|-")))
                  (MATH_SYMBOL "(")
                  (MATH_SYMBOL "P")
                  (MATH_SYMBOL "->")
                  (MATH_SYMBOL "Q")
                  (MATH_SYMBOL ")"))))
            (stmt
              (assert_stmt
                (axiom_stmt
                  (LABEL "mp")
                  (typecode
                    (constant
                      (MATH_SYMBOL "|-")))
                  (MATH_SYMBOL "Q")))))))
      (outermost_scope_stmt
        (stmt
          (assert_stmt
            (provable_stmt
              (LABEL "th1")
              (typecode
                (constant
                  (MATH_SYMBOL "|-")))
              (MATH_SYMBOL "t")
              (MATH_SYMBOL "=")
              (MATH_SYMBOL "t")
              (proof
                (uncompressed_proof
                  (LABEL "tt")
                  (LABEL "tze")
                  (LABEL "tpl")
                  (LABEL "tt")
                  (LABEL "weq")
                  (LABEL "tt")
                  (LABEL "tt")
                  (LABEL "weq")
                  (LABEL "tt")
                  (LABEL "a2")
                  (LABEL "tt")
                  (LABEL "tze")
                  (LABEL "tpl")
                  (LABEL "tt")
                  (LABEL "weq")
                  (LABEL "tt")
                  (LABEL "tze")
                  (LABEL "tpl")
                  (LABEL "tt")
                  (LABEL "weq")
                  (LABEL "tt")
                  (LABEL "tt")
                  (LABEL "weq")
                  (LABEL "wim")
                  (LABEL "tt")
                  (LABEL "a2")
                  (LABEL "tt")
                  (LABEL "tze")
                  (LABEL "tpl")
                  (LABEL "tt")
                  (LABEL "tt")
                  (LABEL "a1")
                  (LABEL "mp")
                  (LABEL "mp"))))))))

### mmparser

    (database
      (outermost_scope_stmt
        (constant_stmt
          (constant
            (MATH_SYMBOL "0"))
          (constant
            (MATH_SYMBOL "+"))
          (constant
            (MATH_SYMBOL "="))
          (constant
            (MATH_SYMBOL "->"))
          (constant
            (MATH_SYMBOL "("))
          (constant
            (MATH_SYMBOL ")"))
          (constant
            (MATH_SYMBOL "term"))
          (constant
            (MATH_SYMBOL "wff"))
          (constant
            (MATH_SYMBOL "|-"))))
      (outermost_scope_stmt
        (stmt
          (variable_stmt
            (variable
              (MATH_SYMBOL "t"))
            (variable
              (MATH_SYMBOL "r"))
            (variable
              (MATH_SYMBOL "s"))
            (variable
              (MATH_SYMBOL "P"))
            (variable
              (MATH_SYMBOL "Q")))))
      (outermost_scope_stmt
        (stmt
          (hypothesis_stmt
            (floating_stmt
              (LABEL "tt")
              (typecode
                (constant
                  (MATH_SYMBOL "term")))
              (variable
                (MATH_SYMBOL "t"))))))
      (outermost_scope_stmt
        (stmt
          (hypothesis_stmt
            (floating_stmt
              (LABEL "tr")
              (typecode
                (constant
                  (MATH_SYMBOL "term")))
              (variable
                (MATH_SYMBOL "r"))))))
      (outermost_scope_stmt
        (stmt
          (hypothesis_stmt
            (floating_stmt
              (LABEL "ts")
              (typecode
                (constant
                  (MATH_SYMBOL "term")))
              (variable
                (MATH_SYMBOL "s"))))))
      (outermost_scope_stmt
        (stmt
          (hypothesis_stmt
            (floating_stmt
              (LABEL "wp")
              (typecode
                (constant
                  (MATH_SYMBOL "wff")))
              (variable
                (MATH_SYMBOL "P"))))))
      (outermost_scope_stmt
        (stmt
          (hypothesis_stmt
            (floating_stmt
              (LABEL "wq")
              (typecode
                (constant
                  (MATH_SYMBOL "wff")))
              (variable
                (MATH_SYMBOL "Q"))))))
      (outermost_scope_stmt
        (stmt
          (assert_stmt
            (axiom_stmt
              (LABEL "tze")
              (typecode
                (constant
                  (MATH_SYMBOL "term")))
              (MATH_SYMBOL "0")))))
      (outermost_scope_stmt
        (stmt
          (assert_stmt
            (axiom_stmt
              (LABEL "tpl")
              (typecode
                (constant
                  (MATH_SYMBOL "term")))
              (MATH_SYMBOL "(")
              (MATH_SYMBOL "t")
              (MATH_SYMBOL "+")
              (MATH_SYMBOL "r")
              (MATH_SYMBOL ")")))))
      (outermost_scope_stmt
        (stmt
          (assert_stmt
            (axiom_stmt
              (LABEL "weq")
              (typecode
                (constant
                  (MATH_SYMBOL "wff")))
              (MATH_SYMBOL "t")
              (MATH_SYMBOL "=")
              (MATH_SYMBOL "r")))))
      (outermost_scope_stmt
        (stmt
          (assert_stmt
            (axiom_stmt
              (LABEL "wim")
              (typecode
                (constant
                  (MATH_SYMBOL "wff")))
              (MATH_SYMBOL "(")
              (MATH_SYMBOL "P")
              (MATH_SYMBOL "->")
              (MATH_SYMBOL "Q")
              (MATH_SYMBOL ")")))))
      (outermost_scope_stmt
        (stmt
          (assert_stmt
            (axiom_stmt
              (LABEL "a1")
              (typecode
                (constant
                  (MATH_SYMBOL "|-")))
              (MATH_SYMBOL "(")
              (MATH_SYMBOL "t")
              (MATH_SYMBOL "=")
              (MATH_SYMBOL "r")
              (MATH_SYMBOL "->")
              (MATH_SYMBOL "(")
              (MATH_SYMBOL "t")
              (MATH_SYMBOL "=")
              (MATH_SYMBOL "s")
              (MATH_SYMBOL "->")
              (MATH_SYMBOL "r")
              (MATH_SYMBOL "=")
              (MATH_SYMBOL "s")
              (MATH_SYMBOL ")")
              (MATH_SYMBOL ")")))))
      (outermost_scope_stmt
        (stmt
          (assert_stmt
            (axiom_stmt
              (LABEL "a2")
              (typecode
                (constant
                  (MATH_SYMBOL "|-")))
              (MATH_SYMBOL "(")
              (MATH_SYMBOL "t")
              (MATH_SYMBOL "+")
              (MATH_SYMBOL "0")
              (MATH_SYMBOL ")")
              (MATH_SYMBOL "=")
              (MATH_SYMBOL "t")))))
      (outermost_scope_stmt
        (stmt
          (block
            (stmt
              (hypothesis_stmt
                (essential_stmt
                  (LABEL "min")
                  (typecode
                    (constant
                      (MATH_SYMBOL "|-")))
                  (MATH_SYMBOL "P"))))
            (stmt
              (hypothesis_stmt
                (essential_stmt
                  (LABEL "maj")
                  (typecode
                    (constant
                      (MATH_SYMBOL "|-")))
                  (MATH_SYMBOL "(")
                  (MATH_SYMBOL "P")
                  (MATH_SYMBOL "->")
                  (MATH_SYMBOL "Q")
                  (MATH_SYMBOL ")"))))
            (stmt
              (assert_stmt
                (axiom_stmt
                  (LABEL "mp")
                  (typecode
                    (constant
                      (MATH_SYMBOL "|-")))
                  (MATH_SYMBOL "Q")))))))
      (outermost_scope_stmt
        (stmt
          (assert_stmt
            (provable_stmt
              (LABEL "th1")
              (typecode
                (constant
                  (MATH_SYMBOL "|-")))
              (MATH_SYMBOL "t")
              (MATH_SYMBOL "=")
              (MATH_SYMBOL "t")
              (proof
                (uncompressed_proof
                  (LABEL "tt")
                  (LABEL "tze")
                  (LABEL "tpl")
                  (LABEL "tt")
                  (LABEL "weq")
                  (LABEL "tt")
                  (LABEL "tt")
                  (LABEL "weq")
                  (LABEL "tt")
                  (LABEL "a2")
                  (LABEL "tt")
                  (LABEL "tze")
                  (LABEL "tpl")
                  (LABEL "tt")
                  (LABEL "weq")
                  (LABEL "tt")
                  (LABEL "tze")
                  (LABEL "tpl")
                  (LABEL "tt")
                  (LABEL "weq")
                  (LABEL "tt")
                  (LABEL "tt")
                  (LABEL "weq")
                  (LABEL "wim")
                  (LABEL "tt")
                  (LABEL "a2")
                  (LABEL "tt")
                  (LABEL "tze")
                  (LABEL "tpl")
                  (LABEL "tt")
                  (LABEL "tt")
                  (LABEL "a1")
                  (LABEL "mp")
                  (LABEL "mp"))))))))