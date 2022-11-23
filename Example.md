

Test of parser: "principia"
===========================


Match-test "M1"
----------------

### Test-code:

    ∗1⋅2  ⊢:p∨p.⊃.p  Pp

### AST

    (principia
      (statement
        (numbering
          (chapter "1")
          (number "2"))
        (axiom `(left "⊢:")
          (formula
            (formula
              (proposition "p")
              (operator
                (Or "∨"))
              (proposition "p"))
            (operator `(left ".") `(right ".")
              (ifthen "⊃"))
            (proposition "p")))))

### LST

    (principia
      (statement
        (numbering
          (chapter "1")
          (number "2"))
        (axiom
          (ifthen
            (Or
              (proposition "p")
              (proposition "p"))
            (proposition "p")))))

### modern

    1.2    ⊢  p ∨ p ⊃ p


Match-test "M2"
----------------

### Test-code:

    ∗3⋅01  p.q.=.∼(∼p∨∼q)  Df

### AST

    (principia
      (statement
        (numbering
          (chapter "3")
          (number "01"))
        (definition
          (formula
            (And
              (proposition `(right ".") "p")
              (proposition "q"))
            (operator `(left ".") `(right ".")
              (equals "="))
            (Not
              (group `(left "(") `(right ")")
                (formula
                  (Not
                    (proposition "p"))
                  (operator
                    (Or "∨"))
                  (Not
                    (proposition "q")))))))))

### LST

    (principia
      (statement
        (numbering
          (chapter "3")
          (number "01"))
        (definition
          (equals
            (And
              (proposition "p")
              (proposition "q"))
            (Not
              (Or `(left "(") `(right ")")
                (Not
                  (proposition "p"))
                (Not
                  (proposition "q"))))))))

### modern

    3.01    p & q  =df  ∼(∼p ∨ ∼q)


Match-test "M3"
----------------

### Test-code:

    ∗9⋅01  ∼{(x).ϕx}.=.(∃x).∼ϕx  Df

### AST

    (principia
      (statement
        (numbering
          (chapter "9")
          (number "01"))
        (definition
          (formula
            (Not
              (group `(left "{") `(right "}")
                (for_all
                  (variable `(right ".") "x")
                  (function
                    (function_name "ϕ")
                    (variable "x")))))
            (operator `(left ".") `(right ".")
              (equals "="))
            (exists
              (variable `(right ".") "x")
              (Not
                (function
                  (function_name "ϕ")
                  (variable "x"))))))))

### LST

    (principia
      (statement
        (numbering
          (chapter "9")
          (number "01"))
        (definition
          (equals
            (Not
              (for_all `(left "{") `(right "}")
                (variable "x")
                (function
                  (function_name "ϕ")
                  (variable "x"))))
            (exists
              (variable "x")
              (Not
                (function
                  (function_name "ϕ")
                  (variable "x"))))))))

### modern

    9.01    ∼∀x ϕx  =df  ∃x ∼ϕx


Match-test "M4"
----------------

### Test-code:

    ∗3⋅12  ⊢:∼p.∨.∼q.∨.p.q

### AST

    (principia
      (statement
        (numbering
          (chapter "3")
          (number "12"))
        (theorem `(left "⊢:")
          (formula
            (Not
              (proposition "p"))
            (operator `(left ".") `(right ".")
              (Or "∨"))
            (Not
              (proposition "q"))
            (operator `(left ".") `(right ".")
              (Or "∨"))
            (And
              (proposition `(right ".") "p")
              (proposition "q"))))))

### LST

    (principia
      (statement
        (numbering
          (chapter "3")
          (number "12"))
        (theorem
          (Or
            (Or
              (Not
                (proposition "p"))
              (Not
                (proposition "q")))
            (And
              (proposition "p")
              (proposition "q"))))))

### modern

    3.12    ⊢  ∼p ∨ ∼q ∨ (p & q)


Match-test "M5"
----------------

### Test-code:

    ∗2⋅33  p∨q∨r.=.(p∨q)∨r  Df

### AST

    (principia
      (statement
        (numbering
          (chapter "2")
          (number "33"))
        (definition
          (formula
            (formula
              (proposition "p")
              (operator
                (Or "∨"))
              (proposition "q")
              (operator
                (Or "∨"))
              (proposition "r"))
            (operator `(left ".") `(right ".")
              (equals "="))
            (formula
              (group `(left "(") `(right ")")
                (formula
                  (proposition "p")
                  (operator
                    (Or "∨"))
                  (proposition "q")))
              (operator
                (Or "∨"))
              (proposition "r"))))))

### LST

    (principia
      (statement
        (numbering
          (chapter "2")
          (number "33"))
        (definition
          (equals
            (Or
              (Or
                (proposition "p")
                (proposition "q"))
              (proposition "r"))
            (Or
              (Or `(left "(") `(right ")")
                (proposition "p")
                (proposition "q"))
              (proposition "r"))))))

### modern

    2.33    p ∨ q ∨ r  =df  (p ∨ q) ∨ r


Match-test "M6"
----------------

### Test-code:

    ∗10⋅02  ϕx⊃x ψx.=.(x).ϕx⊃ψx  Df

### AST

    (principia
      (statement
        (numbering
          (chapter "10")
          (number "02"))
        (definition
          (formula
            (for_all `(subscripted "x")
              (variable "x")
              (formula
                (function
                  (function_name "ϕ")
                  (variable "x"))
                (operator `(subscript "x")
                  (ifthen "⊃"))
                (function
                  (function_name "ψ")
                  (variable "x"))))
            (operator `(left ".") `(right ".")
              (equals "="))
            (for_all
              (variable `(right ".") "x")
              (formula
                (function
                  (function_name "ϕ")
                  (variable "x"))
                (operator
                  (ifthen "⊃"))
                (function
                  (function_name "ψ")
                  (variable "x"))))))))

### LST

    (principia
      (statement
        (numbering
          (chapter "10")
          (number "02"))
        (definition
          (equals
            (for_all
              (variable "x")
              (ifthen
                (function
                  (function_name "ϕ")
                  (variable "x"))
                (function
                  (function_name "ψ")
                  (variable "x"))))
            (for_all
              (variable "x")
              (ifthen
                (function
                  (function_name "ϕ")
                  (variable "x"))
                (function
                  (function_name "ψ")
                  (variable "x"))))))))

### modern

    10.02    ∀x (ϕx ⊃ ψx)  =df  ∀x (ϕx ⊃ ψx)


Match-test "M7"
----------------

### Test-code:

    ∗10⋅03  ϕx≡x ψx.=.(x).ϕx≡ψx  Df

### AST

    (principia
      (statement
        (numbering
          (chapter "10")
          (number "03"))
        (definition
          (formula
            (for_all `(subscripted "x")
              (variable "x")
              (formula
                (function
                  (function_name "ϕ")
                  (variable "x"))
                (operator `(subscript "x")
                  (ifonlyif "≡"))
                (function
                  (function_name "ψ")
                  (variable "x"))))
            (operator `(left ".") `(right ".")
              (equals "="))
            (for_all
              (variable `(right ".") "x")
              (formula
                (function
                  (function_name "ϕ")
                  (variable "x"))
                (operator
                  (ifonlyif "≡"))
                (function
                  (function_name "ψ")
                  (variable "x"))))))))

### LST

    (principia
      (statement
        (numbering
          (chapter "10")
          (number "03"))
        (definition
          (equals
            (for_all
              (variable "x")
              (ifonlyif
                (function
                  (function_name "ϕ")
                  (variable "x"))
                (function
                  (function_name "ψ")
                  (variable "x"))))
            (for_all
              (variable "x")
              (ifonlyif
                (function
                  (function_name "ϕ")
                  (variable "x"))
                (function
                  (function_name "ψ")
                  (variable "x"))))))))

### modern

    10.03    ∀x (ϕx ≡ ψx)  =df  ∀x (ϕx ≡ ψx)