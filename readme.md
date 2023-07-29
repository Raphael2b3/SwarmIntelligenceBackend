de

# Schwarm Intelligenz

---

## Definitionen

Gegeben sei eine Menge aus Projekten **P** = {*p0*,*p1*,*p2*,...}

Ein Projekt *p* ist ein gewichteter gerichteter azyklischer Graph *p*(E, V). 

Die Menge V der Knoten ist die Menge der Statements **S**. 

Ein Statement *s* ist eine verbale Aussage die entweder wahr oder falsch ist. 

Die Menge E der Kanten ist die Menge der Verbindungen *C* = {*c0*, *c1*, *c2*, ...} zwischen den Statements. 

*c* ist eine Verbindung definiert durch ein Tupel (*s0*, *s1*, *t*, *w*) wobei:

- *s0* der Start Punkt und Element von S ist
- *s1* der End Punkt und Element von S ist
- *t* der Typ der Verbindung und Element von {+,-} ist und angibt ob *s1* die Aussage unterstützt oder widerlegt
- *w* die Gewichtung und eine reelle Zahl im Intervall [0, 1] ost

---

### Statement

---

Die Funktion W(s): s in S -> [0,1] gibt den Wahrheitsgehalt der Aussage s wieder.
W(s) = 