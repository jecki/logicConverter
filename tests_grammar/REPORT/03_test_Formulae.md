

Test of parser: "formula"
=========================


Match-test "M1"
----------------

### Test-code:

    q.⊃.p∨q

### AST

    (formula
      (proposition
        "q"
      )
      (operator `(left ".") `(right ".")
        (ifthen
          "⊃"
        )
      )
      (formula
        (proposition
          "p"
        )
        (operator
          (Or
            "∨"
          )
        )
        (proposition
          "q"
        )
      )
    )

### LST

    (ifthen (proposition "q") (Or (proposition "p") (proposition "q")))

### modern

    q ⊃ p ∨ q

### modern.tex

    q {\supset}p  \vee q

### pm.tex

    q.{\supset}.p \vee q


Match-test "M2"
----------------

### Test-code:

    p∨q.⊃.q∨p

### AST

    (formula
      (formula
        (proposition "p")
        (operator
          (Or "∨"))
        (proposition "q"))
      (operator `(left ".") `(right ".")
        (ifthen "⊃"))
      (formula
        (proposition "q")
        (operator
          (Or "∨"))
        (proposition "p")))

### LST

    (ifthen (Or (proposition "p") (proposition "q")) (Or (proposition "q") (proposition "p")))

### modern

    p ∨ q ⊃ q ∨ p

### modern.tex

    p  \vee q {\supset}q  \vee p

### pm.tex

    p \vee q.{\supset}.q \vee p


Match-test "M3"
----------------

### Test-code:

    p∨(q∨r).⊃.q∨(p∨r)

### AST

    (formula
      (formula
        (proposition "p")
        (operator
          (Or "∨"))
        (group `(left "(") `(right ")")
          (formula
            (proposition "q")
            (operator
              (Or "∨"))
            (proposition "r"))))
      (operator `(left ".") `(right ".")
        (ifthen "⊃"))
      (formula
        (proposition "q")
        (operator
          (Or "∨"))
        (group `(left "(") `(right ")")
          (formula
            (proposition "p")
            (operator
              (Or "∨"))
            (proposition "r")))))

### LST

    (ifthen
      (Or
        (proposition "p")
        (Or `(left "(") `(right ")")
          (proposition "q")
          (proposition "r")))
      (Or
        (proposition "q")
        (Or `(left "(") `(right ")")
          (proposition "p")
          (proposition "r"))))

### modern

    p ∨ (q ∨ r) ⊃ q ∨ (p ∨ r)

### modern.tex

    p  \vee (q  \vee r) {\supset}q  \vee (p  \vee r)

### pm.tex

    p \vee (q \vee r).{\supset}.q \vee (p \vee r)


Match-test "M4"
----------------

### Test-code:

    q⊃r.⊃:p∨q.⊃.p∨r

### AST

    (formula
      (formula
        (proposition "q")
        (operator
          (ifthen "⊃"))
        (proposition "r"))
      (operator `(left ".") `(right ":")
        (ifthen "⊃"))
      (formula
        (formula
          (proposition "p")
          (operator
            (Or "∨"))
          (proposition "q"))
        (operator `(left ".") `(right ".")
          (ifthen "⊃"))
        (formula
          (proposition "p")
          (operator
            (Or "∨"))
          (proposition "r"))))

### LST

    (ifthen
      (ifthen
        (proposition "q")
        (proposition "r"))
      (ifthen `(left "(") `(right ")")
        (Or
          (proposition "p")
          (proposition "q"))
        (Or
          (proposition "p")
          (proposition "r"))))

### modern

    q ⊃ r ⊃ (p ∨ q ⊃ p ∨ r)

### modern.tex

    q {\supset}r {\supset}(p  \vee q {\supset}p  \vee r)

### pm.tex

    q{\supset}r.{\supset}:p \vee q.{\supset}.p \vee r


Match-test "M5"
----------------

### Test-code:

    p⊃∼q.⊃.q⊃∼p

### AST

    (formula
      (formula
        (proposition "p")
        (operator
          (ifthen "⊃"))
        (Not
          (proposition "q")))
      (operator `(left ".") `(right ".")
        (ifthen "⊃"))
      (formula
        (proposition "q")
        (operator
          (ifthen "⊃"))
        (Not
          (proposition "p"))))

### LST

    (ifthen
      (ifthen
        (proposition
          "p"
        )
        (Not
          (proposition
            "q"
          )
        )
      )
      (ifthen `(left "(") `(right ")")
        (proposition
          "q"
        )
        (Not
          (proposition
            "p"
          )
        )
      )
    )

### modern

    p ⊃ ∼q ⊃ (q ⊃ ∼p)

### modern.tex

    p {\supset}{\sim}q {\supset}(q {\supset}{\sim}p)

### pm.tex

    p{\supset}{\sim}q.{\supset}.q{\supset}{\sim}p


Match-test "M6"
----------------

### Test-code:

    p.q.⊃.r:⊃:p.⊃.q⊃r

### AST

    (formula
      (formula
        (And
          (proposition `(right ".") "p")
          (proposition "q"))
        (operator `(left ".") `(right ".")
          (ifthen "⊃"))
        (proposition "r"))
      (operator `(left ":") `(right ":")
        (ifthen "⊃"))
      (formula
        (proposition "p")
        (operator `(left ".") `(right ".")
          (ifthen "⊃"))
        (formula
          (proposition "q")
          (operator
            (ifthen "⊃"))
          (proposition "r"))))

### LST

    (ifthen
      (ifthen
        (And
          (proposition "p")
          (proposition "q"))
        (proposition "r"))
      (ifthen `(left "(") `(right ")")
        (proposition "p")
        (ifthen `(left "(") `(right ")")
          (proposition "q")
          (proposition "r"))))

### modern

    p & q ⊃ r ⊃ (p ⊃ (q ⊃ r))

### modern.tex

    p \:\&\: q {\supset}r {\supset}(p {\supset}(q {\supset}r))

### pm.tex

    p.q.{\supset}.r:{\supset}:p.{\supset}.q{\supset}r


Match-test "M7"
----------------

### Test-code:

    p.q.⊃.∼r:≡:q.r.⊃.∼p

### AST

    (formula
      (formula
        (And
          (proposition `(right ".") "p")
          (proposition "q"))
        (operator `(left ".") `(right ".")
          (ifthen "⊃"))
        (Not
          (proposition "r")))
      (operator `(left ":") `(right ":")
        (ifonlyif "≡"))
      (formula
        (And
          (proposition `(right ".") "q")
          (proposition "r"))
        (operator `(left ".") `(right ".")
          (ifthen "⊃"))
        (Not
          (proposition "p"))))

### LST

    (ifonlyif
      (ifthen
        (And
          (proposition "p")
          (proposition "q"))
        (Not
          (proposition "r")))
      (ifthen
        (And
          (proposition "q")
          (proposition "r"))
        (Not
          (proposition "p"))))

### modern

    p & q ⊃ ∼r ≡ q & r ⊃ ∼p

### modern.tex

    p \:\&\: q {\supset}{\sim}r ≡_{} q \:\&\: r {\supset}{\sim}p

### pm.tex

    p.q.{\supset}.{\sim}r:{\equiv}:q.r.{\supset}.{\sim}p


Match-test "M8"
----------------

### Test-code:

    q⊃∼r.⊃:p∨q.r.≡.p.r

### AST

    (formula
      (formula
        (proposition "q")
        (operator
          (ifthen "⊃"))
        (Not
          (proposition "r")))
      (operator `(left ".") `(right ":")
        (ifthen "⊃"))
      (formula
        (And
          (formula `(right ".")
            (proposition "p")
            (operator
              (Or "∨"))
            (proposition "q"))
          (proposition "r"))
        (operator `(left ".") `(right ".")
          (ifonlyif "≡"))
        (And
          (proposition `(right ".") "p")
          (proposition "r"))))

### LST

    (ifthen
      (ifthen
        (proposition "q")
        (Not
          (proposition "r")))
      (ifonlyif `(left "(") `(right ")")
        (And
          (Or `(right ".")
            (proposition "p")
            (proposition "q"))
          (proposition "r"))
        (And
          (proposition "p")
          (proposition "r"))))

### modern

    q ⊃ ∼r ⊃ (p ∨ q. & r ≡ p & r)

### modern.tex

    q {\supset}{\sim}r {\supset}(p  \vee q. \:\&\: r ≡_{} p \:\&\: r)

### pm.tex

    q{\supset}{\sim}r.{\supset}:p \vee qr.{\equiv}.p.r


Match-test "M9"
----------------

### Test-code:

    p.∨.(x).ϕx:=.(x).ϕx∨p

### AST

    (formula
      (formula
        (proposition "p")
        (operator `(left ".") `(right ".")
          (Or "∨"))
        (for_all
          (variable `(right ".") "x")
          (function
            (function_name "ϕ")
            (variable "x"))))
      (operator `(left ":") `(right ".")
        (equals "="))
      (for_all
        (variable `(right ".") "x")
        (formula
          (function
            (function_name "ϕ")
            (variable "x"))
          (operator
            (Or "∨"))
          (proposition "p"))))

### LST

    (equals
      (Or
        (proposition "p")
        (for_all
          (variable "x")
          (function
            (function_name "ϕ")
            (variable "x"))))
      (for_all
        (variable "x")
        (Or `(left "(") `(right ")")
          (function
            (function_name "ϕ")
            (variable "x"))
          (proposition "p"))))

### modern

    p ∨ ∀x ϕx = ∀x (ϕx ∨ p)

### modern.tex

    p  \vee \forall x\;ϕx =_{} \forall x\;(ϕx  \vee p)

### pm.tex

    p. \vee .(x).ϕx:{=}.(x).ϕx \vee p


Match-test "M10"
-----------------

### Test-code:

    (∃x).ϕx.⊃.q:⊃:.(∃x).ϕx.∨.r:⊃.q∨r

### AST

    (formula
      (formula
        (exists
          (variable `(right ".") "x")
          (function
            (function_name "ϕ")
            (variable "x")))
        (operator `(left ".") `(right ".")
          (ifthen "⊃"))
        (proposition "q"))
      (operator `(left ":") `(right ":.")
        (ifthen "⊃"))
      (formula
        (formula
          (exists
            (variable `(right ".") "x")
            (function
              (function_name "ϕ")
              (variable "x")))
          (operator `(left ".") `(right ".")
            (Or "∨"))
          (proposition "r"))
        (operator `(left ":") `(right ".")
          (ifthen "⊃"))
        (formula
          (proposition "q")
          (operator
            (Or "∨"))
          (proposition "r"))))

### LST

    (ifthen
      (ifthen
        (exists
          (variable "x")
          (function
            (function_name "ϕ")
            (variable "x")))
        (proposition "q"))
      (ifthen `(left "(") `(right ")")
        (Or
          (exists
            (variable "x")
            (function
              (function_name "ϕ")
              (variable "x")))
          (proposition "r"))
        (Or
          (proposition "q")
          (proposition "r"))))

### modern

    ∃x ϕx ⊃ q ⊃ (∃x ϕx ∨ r ⊃ q ∨ r)

### modern.tex

    \exists x\;ϕx {\supset}q {\supset}(\exists x\;ϕx  \vee r {\supset}q  \vee r)

### pm.tex

    (\exists x).ϕx.{\supset}.q:{\supset}:.(\exists x).ϕx. \vee .r:{\supset}.q \vee r


Match-test "M11"
-----------------

### Test-code:

    (∃x).ϕx.ψx:ϕx⊃x ψx:≡:(∃x).ϕx:ϕx⊃x ψx

### AST

    (formula
      (And
        (exists `(right ":")
          (variable `(right ".") "x")
          (And
            (function `(right ".")
              (function_name "ϕ")
              (variable "x"))
            (function
              (function_name "ψ")
              (variable "x"))))
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
              (variable "x")))))
      (operator `(left ":") `(right ":")
        (ifonlyif "≡"))
      (And
        (exists `(right ":")
          (variable `(right ".") "x")
          (function
            (function_name "ϕ")
            (variable "x")))
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
              (variable "x"))))))

### LST

    (ifonlyif
      (And
        (exists
          (variable "x")
          (And `(left "(") `(right ")")
            (function `(right ".")
              (function_name "ϕ")
              (variable "x"))
            (function
              (function_name "ψ")
              (variable "x"))))
        (for_all
          (variable "x")
          (ifthen `(left "(") `(right ")")
            (function
              (function_name "ϕ")
              (variable "x"))
            (function
              (function_name "ψ")
              (variable "x")))))
      (And
        (exists
          (variable "x")
          (function
            (function_name "ϕ")
            (variable "x")))
        (for_all
          (variable "x")
          (ifthen `(left "(") `(right ")")
            (function
              (function_name "ϕ")
              (variable "x"))
            (function
              (function_name "ψ")
              (variable "x"))))))

### modern

    ∃x (ϕx & ψx) & ∀x (ϕx ⊃ ψx) ≡ ∃x ϕx & ∀x (ϕx ⊃ ψx)

### modern.tex

    \exists x\;(ϕx \:\&\: ψx) \:\&\: \forall x\;(ϕx {\supset}ψx) ≡_{} \exists x\;ϕx \:\&\: \forall x\;(ϕx {\supset}ψx)

### pm.tex

    (\exists x).ϕxψxϕx{\supset}_{x }ψx:{\equiv}:(\exists x).ϕxϕx{\supset}_{x }ψx


Test of parser: "formula1"
==========================


Match-test "M1"
----------------

### Test-code:

    ϕx.ψx

### AST

    (And (function `(right ".") (function_name "ϕ") (variable "x")) (function (function_name "ψ") (variable "x")))

### LST

    (And (function `(right ".") (function_name "ϕ") (variable "x")) (function (function_name "ψ") (variable "x")))

### modern

    ϕx & ψx

### modern.tex

    ϕx \:\&\: ψx

### pm.tex

    ϕxψx


Test of parser: "and2"
======================


Match-test "M1"
----------------

### Test-code:

    ϕx.ψx:ϕx⊃x ψx

### AST

    (And
      (And `(right ":")
        (function `(right ".")
          (function_name "ϕ")
          (variable "x"))
        (function
          (function_name "ψ")
          (variable "x")))
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
            (variable "x")))))

### LST

    (And
      (And `(right ":")
        (function `(right ".")
          (function_name "ϕ")
          (variable "x"))
        (function
          (function_name "ψ")
          (variable "x")))
      (for_all
        (variable "x")
        (ifthen `(left "(") `(right ")")
          (function
            (function_name "ϕ")
            (variable "x"))
          (function
            (function_name "ψ")
            (variable "x")))))

### modern

    ϕx & ψx: & ∀x (ϕx ⊃ ψx)

### modern.tex

    ϕx \:\&\: ψx: \:\&\: \forall x\;(ϕx {\supset}ψx)

### pm.tex

    ϕxψxϕx{\supset}_{x }ψx


Test of parser: "and1"
======================


Match-test "M1"
----------------

### Test-code:

    ϕx.ψx

### AST

    (And (function `(right ".") (function_name "ϕ") (variable "x")) (function (function_name "ψ") (variable "x")))

### LST

    (And (function `(right ".") (function_name "ϕ") (variable "x")) (function (function_name "ψ") (variable "x")))

### modern

    ϕx & ψx

### modern.tex

    ϕx \:\&\: ψx

### pm.tex

    ϕxψx


Test of parser: "predication"
=============================


Match-test "M1"
----------------

### Test-code:

    P(x)

### AST

    (predication (relation "P") (variable "x"))

### LST

    (predication (relation "P") (variable "x"))

### modern

    Px

### modern.tex

    Px

### pm.tex

    Px


Match-test "M2"
----------------

### Test-code:

    Gr(x,y)

### AST

    (predication (relation "Gr") (variable "x") (variable "y"))

### LST

    (predication (relation "Gr") (variable "x") (variable "y"))

### modern

    Gr(x,y)

### modern.tex

    Gr(x,y)

### pm.tex

    Gr(x,y)