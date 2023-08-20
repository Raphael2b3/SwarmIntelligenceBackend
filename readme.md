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

## Routen

### POST "/connection/create"

Erstelle eine Connection

```

Sende:
{
    "stm_start": "Aussage id die unterstützend Arbeitet"
    "stm_stop": "Aussage id die unterstützt wird"
    "supports": true // falls die Aussage unterstützt, false wenn sie wiederlegt
}
```

---

### POST "/connection/isbad"

```
Sende:
{
    "id": "connection Id"
    "is_bad": true // wenn user connection weg haben will false wenn rückgängig gemacht werden soll
    
}
```

--- 

### POST "/connection/delete"

```
Sende:
{
    "id": "connection Id"    
}
```

---

### POST "/token"

```
Sende:
{
    "username": "username"
    "password": "password123"    // muss halt https sein sonst unsicher
}

Erhalte:
{
    "access_token": "fabcef138fb89cf934f93a9def934892", //irgendwie so
    "token_type": "bearer"
}
```

---

### POST "/statement/star"

remove=True wenn der stern entfernt werden soll, sonst weglassen

```

Sende:
{
    "id": "Id von Object was mit stern markiert werden soll",
    "remove":True
}

```

---

### POST "/project/star"

remove=True wenn der stern entfernt werden soll, sonst weglassen

```

Sende:
{
    "id": "Id von Object was mit stern markiert werden soll",
    "remove": true
}

```

---

### POST "/user/star"

remove=True wenn der stern entfernt werden soll, sonst weglassen

```

Sende:
{
    "id": "Id von Object was mit stern markiert werden soll",
    "remove":false
}

```

---

### POST "/statement/report"

```

Sende:
{
    "id": "Id von Object was reported wird"
    "message": "Begründung was nicht in Ordnung war"
}

```

---

### POST "/project/report"

```

Sende:
{
    "id": "Id von Object was reported wird"
    "message": "Begründung was nicht in Ordnung war"
}
```

---

### POST "/user/report"

```

Sende:
{
    "id": "Id von Object was reported wird"
    "message": "Begründung was nicht in Ordnung war"
}

```

---

### GET "/project?q=A"

"q=A"  ->  "A" ist der Suchstring

```

Erhalte:
[
    {
        "id": "0",
        "name": "Abnehmen"
    },
    {
        "id": "1",
        "name": "Autofahren"
    },
    {
        "id": "2",
        "name": "Alkohol"
    },
]

```

---

### POST "/project/create"

```

Sende:
{
    "name": "Analysis"
}


```

---

### POST "/project/delete"

```

Sende:
{
    "id": "4"
}


```

---

### GET "/statement?q="

"q="  ->  "" ist der Suchstring

```

Erhalte:
[
    {
        "id": "22",
        "text": "1 ist 1"
        "user_vote":-1 # kann 1, 0, -1 sein 
        "user_is_author": false 
    
    },
    {
        "id": "23",
        "text": "2 ist 2"
        "user_vote":-1 # kann 1, 0, -1 sein 
        "user_is_author": false 
    
    },
    {
        "id": "24",
        "text": "3 ist 3"
        "user_vote":-1 # kann 1, 0, -1 sein 
        "user_is_author": true  
    
    },
]

```

---

### POST "/statement/create"

```

Sende:

{
    "value": "Analysis"
}


```

---

### POST "/statement/delete"
Deletes globally for ever
```

Sende:
{
    "id": "4"
}


```

---

### POST "/statement/context"

```

Sende:
{
    "id": "4",
    
    "parentgenerations": 1, //how many layers/generations of parents 
    "n_parents": 4, // number of parents loaded
    "skip_parents": 0, // number of parents skipped before loading
    
    "childgenerations": 1, //how many layers/generations of children 
    "n_childs": 4, // number of children loaded
    "skip_childs": 4, // number of children skipped before loading
    
    
}

Erhalte:

{

    "id" = "88",
    "value": "Delphine sind schwule heie ja",
    "w": 0.6,
    "args": [
                {
                "id": "12"
                "supports": true,
                "statement": {
                    "id" = "88",
                    "value": "Delphine machen fischen angst wie Haie",
                    "w": 0.9,
                    "args": [],
                    "parents": [],
                    "tags": ["lgbtq+","fyfyfy","fische"],
                    "user_vote": 1, // 1: upvote, 0: Neutral, -1: down
                    "user_is_author": false 
                    },
                "user_disapprove": false,
                "user_is_author": true
                },
                {
                "id": "13"
                "supports": false,
                "statement": {
                    "id" = "69",
                    "value": "Delphine sind Hetero weil sie überleben",
                    "w": 0.98,
                    "args": [],
                    "parents": [],
                    "tags": ["lgbtq+","fyfyfy","fische"],
                    "user_vote": -1,
                    "user_is_author": true 
                    },
                "user_disapprove": true,
                "user_is_author": false
                }
            ],
    "parents": [{
                "id": "59"
                "supports": true,
                "statement": {
                    "id" = "25",
                    "value": "Delphine gehören zu LGTBQ+ Community ja vallah",
                    "w": 0.5,
                    "args": [],
                    "parents": [],
                    "tags": ["lgbtq+","fyfyfy","fische"],
                    "user_vote": -1,
                    "user_is_author": true 
                    },
                "user_disapprove": true,
                "user_is_author": false
                }],
    "tags": ["lgbtq+","fyfyfy","fische"],
    "user_vote": 1 , 
    "user_is_author": false

}

```

---
### POST "/statement/tag"
```

Sende:
{
    "id": "4",
    "projectname": "Auto"
    
}


```

---

### POST "/user/create"
```

Sende:
{
    "username":"susibaka203",
    "password":"132kdsad2314_;;sdlj"
    
}


```

---
### POST "/user/delete"
```

Sende:
{
    "username":"susibaka203",
}


```

