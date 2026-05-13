# Debugging Challenge: Mini Student Project

## Ziel
Bringe das Projekt wieder zum Laufen, indem du schrittweise die Fehler behebst.
Das Projekt ist absichtlich so gebaut, dass nach jedem Fix meist der naechste Fehler sichtbar wird.

## Start
1. Oeffne den Ordner debug_student_repo.
2. Fuehre aus: python main.py
3. Lies den Fehler und behebe ihn.
4. Wiederhole, bis das Programm komplett laeuft.

## Enthaltene Fehlerarten
- Falscher Importpfad
- Zirkulaerer Import
- Unsauberes try/except
- ValueError
- Logikfehler bei Bool-Umwandlung
- Fehlerhafte Vergleichslogik (`<` vs `<=`)
- Fehlender main-guard

## Hinweise fuer die Bearbeitung
- Arbeite in kleinen Schritten und teste nach jedem Fix.
- Nutze Tracebacks aktiv: erste sinnvolle Fehlerstelle suchen.
- Vermeide broad except ohne Logging.

## Definition of Done
Du bist fertig, wenn:
1. `python main.py` ohne Exception durchlaeuft.
2. Es genau 5 gueltige Studierende im Report gibt.
3. Der Durchschnitt korrekt ist.
4. Der finale Output inhaltlich dem folgenden Soll-Output entspricht.

## Soll-Output (Final)
```text
Row skipped (invalid points): ben -> N/A
Row skipped (invalid points): tom -> Five
=== Course Report ===
Anna: 10 points, passed=True
Carl: 8 points, passed=True
Max: 2 points, passed=False
Hannah: 3 points, passed=False
Jakob: 7 points, passed=True
Average points: 6.00
```

## Bonus (optional)
- Fuege einen `if __name__ == "__main__":`-Guard in `main.py` hinzu.
- Ersetze pauschale Fehlerbehandlung durch gezielte `except ValueError`-Zweige mit aussagekraeftigem Logging.
