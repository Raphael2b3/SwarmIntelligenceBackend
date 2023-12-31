de

# Schwarm Intelligenz App (Backend)

---

## Konzept

Die App setzt voraus, dass eine Vielzahl von Stimmen bei einer Abstimmung zu einem idealen Ergebnis führt.

Die Applikation ermöglicht es Nutzern Aussagen zu erstellen und diese von anderen Nutzern nach Wahrheit bewerten zu
lassen. Dabei wird ermöglicht Unteraussagen zu treffen. Diese Verkettung von Aussagen ist mit einer Argumentationskette
gleichzusetzen.

Es wird ein Wahrheitswert zu jeder Aussage berechnet, der die Wahrheitswerte der unter Aussagen berücksichtigt.

Um schnell Einschätzungen von Menschen zu neuen oder wenig betrachteten Aussagen zu erhalten, wird die App Vorschläge
für jeden Nutzer erstellen. Durch die Vorschläge sollen unterbewertete Aussagen zu ausreichend bewerteten Aussagen
gemacht werden.

## Modi

--- 

### Informationsbeschaffung

Es gibt einen Modus der Informationsbeschaffung, in welchen man nach Aussagen sucht. Dort werden auch
Argumentationsketten und Verknüpfungen von Aussagen dargestellt.

Aussagen können Kategorien zugeordnet werden, um schneller Aussagen zu finden, die für einen relevant sind.

---

### Evaluation

Im Modus der Evaluation wird nach einem Algorithmus dem Nutzer einfache Fragen gestellt.

Der Nutzer hat die Aufgabe:

- Aussagen auf Richtigkeit bewerten. (upvote, downvote)
- Verknüpfungen von Aussagen bewerten. Hat Aussage A wirklich einfluss auf die Richtigkeit von Aussage B
- Aussagen auf Identität prüfen. Sind zwei Aussagen Identisch (ja, nein)
- Reporten von Aussagen die keinen Informationswert haben bzw. unsachlich sind.

Bei der Bewertung von Aussagen wird dem Nutzer nicht angezeigt wie sich andere Entschieden haben, um einem
Mitlaufverhalten entgegenzuwirken.

---

## Mathematik

Alle Daten (Aussagen, Verknüpfungen, Votes, User) werden in Form eines Gewichteten gerichteten Graphen (Informatik)
modelliert.

Die Knoten sind die Aussagen. Die Kanten sind

---
### Wahrheitswert Berechnung

Die Funktion v(i) ist der Wahrheitswert der durch die Votes ermittelt wird. Ein Upvote ist +1, ein downvote ist -1:

v(i)=(upvotes-downvotes)/n_votes

Die Funktion g_k(i) ist die Gewichtung einer Verbindung zwischen Aussagen i und k und ist eine Zahl zwischen 0 und 1

g_k(i) -> [0,1] : g_k(anzahl warnungen als x) = e^(-x)

C_k ist die Menge aller Children Knoten von K. Also Knoten i, die die Aussage K unterstützen oder wiederlegen.

C_k = {i1,i2,i3,...}

W_c(i) ist der mittlere Wahrheitswert der Children gewichtet nach den Gewichten g(i) für i in C_k.

R ist das Verhältnis von den Anteilen von v(i) und W_c(i) in dem zu definierenden Wahrheitswert W(i)

R ist abhängig von der Menger der Children. R(|C_k| als x) {1 wenn x=0, f(x) sonst} ; f(x) -> [c,1[ ; 0 <=c <1

W_k(i) ist der Wahrheitswert, der den tatsächlichen Wahrheitsgehalt von Aussage k in Prozent angeben soll.

W_k(i) = R*v(k) + (1-R)*summe[ i in C_k: w_c(i) * g_k(i) ]/ summe[ i in C_k, g_k(i)]


---

## Models

Get Statement:
{
  - id
  - text
  - tags
  - [userdecision]
  - [user_is_creator]
}

Get Connection:
{
  - id
  - argument
  - thesis
  - [userdecision]
  - [user_is_creator]
}

Get Statement Context:
{
  - statements: list[Get Statement]
  - connections: list[Get Connection]
}


## Routen



