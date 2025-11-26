

Test of parser: "principia"
===========================


Match-test "M1"
----------------

### Test-code:

    *1⋅01  P(x)≡(Gr(x,y).Gr(y,5)) Df
    *1⋅02   |- (Gr(7, 6) . Gr(6,5)) => P(7)  Pp

### AST

    (principia
      (statement
        (numbering
          (chapter "1")
          (counter "01"))
        (definition
          (formula
            (predication
              (relation "P")
              (variable "x"))
            (operator
              (ifonlyif "≡"))
            (group `(left "(") `(right ")")
              (And
                (predication `(right ".")
                  (relation "Gr")
                  (variable "x")
                  (variable "y"))
                (predication
                  (relation "Gr")
                  (variable "y")
                  (number "5")))))))
      (statement
        (numbering
          (chapter "1")
          (counter "02"))
        (axiom
          (formula
            (group `(left "(") `(right ")")
              (And
                (predication `(right ".")
                  (relation "Gr")
                  (number "7")
                  (number "6"))
                (predication
                  (relation "Gr")
                  (number "6")
                  (number "5"))))
            (operator
              (ifthen "=>"))
            (predication
              (relation "P")
              (number "7"))))))

### LST

    (principia
      (statement
        (numbering
          (chapter "1")
          (counter "01"))
        (definition
          (ifonlyif `(subscript "df")
            (predication
              (relation "P")
              (variable "x"))
            (And `(left "(") `(right ")")
              (predication `(right ".")
                (relation "Gr")
                (variable "x")
                (variable "y"))
              (predication
                (relation "Gr")
                (variable "y")
                (number "5"))))))
      (statement
        (numbering
          (chapter "1")
          (counter "02"))
        (axiom
          (ifthen
            (And
              (predication `(right ".")
                (relation "Gr")
                (number "7")
                (number "6"))
              (predication
                (relation "Gr")
                (number "6")
                (number "5")))
            (predication
              (relation "P")
              (number "7"))))))

### modern

    1.01    Px  ≡df  (Gr(x,y) & Gr(y,5))
    1.02    Gr(7,6) & Gr(6,5) ⊃ P(7)

### modern.tex

    \[ \tag*{1.01}    Px \; ≡_{df} \; (Gr(x,y) \:\&\: Gr(y,5))
    
    \tag*{1.02}    Gr(7,6) \:\&\: Gr(6,5) {\supset}P(7) \]

### pm.tex

    \[ \tag*{∗1⋅01}    \vdash  Px{\equiv}(Gr(x,y)Gr(y,5)) \quad Df
    
    \tag*{∗1⋅02}    \vdash  :  (Gr(7,6)Gr(6,5)){\supset}P(7) \quad Pp \]