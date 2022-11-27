This "proof-of-concepts" demonstrates the automatic translation of formulae 
in the notation of the Russell's and Whitehead's Principia Mathematica (PM) 
into:

a) the AST (the abstract syntax tree) which resembles the PM formula in its 
   concrete textual form ("Textgestalt"). This corresponds to the 
   presentation form in MathML
b) the LST (logical syntax tree) which resembles the abstract logical 
   structure of the formula or the "mathematical object" described 
   by the formula. This corresponds to the notation of "mathematical
   object" in MathXML. 
c) modern: A unicode based serialization of b) in modern notation (with
   some restrictions, since subscripts und superscripts a printed inline)
d) pm.tex: A translation of the principia notation into TeX's math-mode.
   In fact, this is a serialization of the AST as TeX-source.

This should suffice to demonstrate the feasibility and at least some of the
capabilities of the approach of automatic conversion. Further targets 
could most probably be implemented without much effort 
(but haven't been done, yet):

e) modern.tex: A serialization of the LST in modern notation in TeX

f) PM MathML: The presentation form of the PM-notation in MathML
   (if MathML is to be supported, say, for archiving purposes.)

e) MathML mathematical object: A conversion of the LST to MathML.

g) modern MathML: The presentation form of the modern notation of 
   the same form in math ML (if Math ML should be supported)

h) coq or any other computer algebra system that offers sufficient 
   support for formal logic to digest Carnap's formulae. (SageMath
   unfortunately does not.)

i) metamath.org: might be very much in the spirit of Carnap...


Test of parser: "principia"
===========================


Match-test "M1*"
-----------------

### Test-code:

    ∗1⋅2  ⊢:p∨p.⊃.p  Pp

### CST

    (principia
      (statement
        (numbering
          (chapter "1")
          (number "2"))
        (axiom
          (_d2 ":")
          (formula
            (formula1
              (and1
                (formula0
                  (proposition "p")
                  (operator
                    (Or "∨"))
                  (proposition "p")))
              (_d1 ".")
              (operator
                (ifthen "⊃"))
              (_d1 ".")
              (and1
                (formula0
                  (proposition "p"))))))))

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

    1.2    p ∨ p ⊃ p

### pm.tex

    \[
    \tag*{∗2⋅1}    \vdash  \colon   p\vee p\ldot {\supset}\ldot p \quad Pp
    \]


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
          (equals `(subscript "df")
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

### pm.tex

    \[
    \tag*{∗01⋅3}    \vdash  p\ldot q\ldot {=}\ldot \osim (\osim p\vee \osim q) \quad Df
    \]


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
          (equals `(subscript "df")
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

### pm.tex

    \[
    \tag*{∗01⋅9}    \vdash  \osim \{(x)\ldot ϕx\}\ldot {=}\ldot (\exists x)\ldot \osim ϕx \quad Df
    \]


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
            (And `(left "(") `(right ")")
              (proposition "p")
              (proposition "q"))))))

### modern

    3.12    ∼p ∨ ∼q ∨ (p & q)

### pm.tex

    \[
    \tag*{∗12⋅3}    {\vdash} \colon   \osim p\ldot \vee \ldot \osim q\ldot \vee \ldot p\ldot q
    \]


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
          (equals `(subscript "df")
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

### pm.tex

    \[
    \tag*{∗33⋅2}    \vdash  p\vee q\vee r\ldot {=}\ldot (p\vee q)\vee r \quad Df
    \]


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
          (equals `(subscript "df")
            (for_all
              (variable "x")
              (ifthen `(left "(") `(right ")")
                (function
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
                  (variable "x"))))))))

### modern

    10.02    ∀x (ϕx ⊃ ψx)  =df  ∀x (ϕx ⊃ ψx)

### pm.tex

    \[
    \tag*{∗02⋅10}    \vdash  ϕx{\supset}_{x }ψx\ldot {=}\ldot (x)\ldot ϕx{\supset}ψx \quad Df
    \]


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
          (equals `(subscript "df")
            (for_all
              (variable "x")
              (ifonlyif `(left "(") `(right ")")
                (function
                  (function_name "ϕ")
                  (variable "x"))
                (function
                  (function_name "ψ")
                  (variable "x"))))
            (for_all
              (variable "x")
              (ifonlyif `(left "(") `(right ")")
                (function
                  (function_name "ϕ")
                  (variable "x"))
                (function
                  (function_name "ψ")
                  (variable "x"))))))))

### modern

    10.03    ∀x (ϕx ≡ ψx)  =df  ∀x (ϕx ≡ ψx)

### pm.tex

    \[
    \tag*{∗03⋅10}    \vdash  ϕx{\equiv}_{x }ψx\ldot {=}\ldot (x)\ldot ϕx{\equiv}ψx \quad Df
    \]