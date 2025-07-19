# Häufige Fragen und Bekannte Probleme

## Probleme mit dem Toctree

Wenn in deinen `.md`-Dateien Fehler auftreten, kann es passieren, dass folgende Zeile unerwartet erscheint:

`<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">`

Direkt nach dem letzten Link im `toctree`. Dieses Problem entsteht in der Regel durch einen nicht korrekt geschlossenen `toctree`-Block.

Achte darauf, den `toctree`-Block mit drei Backticks zu schließen:  "```".  
Wenn der Block mit einem `.md`-Dateinamen endet und nicht korrekt abgeschlossen ist, bleibt das Problem bestehen.

## Fehler bei der Build-Funktion

Tritt während der Build-Phase der Fehler auf:

`[WinError 32] Der Prozess kann nicht auf die Datei zugreifen, da sie von einem anderen Prozess verwendet wird`

stelle sicher, dass die Windows-Eingabeaufforderung, die den Python-Server hostet, geschlossen ist.

Schließe einfach das CMD-Fenster und führe den Build-Befehl erneut aus.  
Das Tool benötigt exklusiven Zugriff auf bestimmte Verzeichnisse.