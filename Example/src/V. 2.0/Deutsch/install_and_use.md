# Anleitung zur Installation und Nutzung des Tools

## Installation

Das Tool ist auf [PyPI](https://pypi.org/project/Easy-versioning/) verfügbar und kann einfach mit folgendem Befehl installiert werden:

`pip install easy-versioning`

Während der Installation werden automatisch auch die im `requirements.txt` aufgelisteten Pakete installiert, da sie für den ordnungsgemäßen Betrieb des Tools erforderlich sind.

## Verwendung

Zuerst sollte die Projektstruktur für die Dokumentation wie folgt aufgebaut sein:

📦 Easy_versioning_Sphinx/  
├── 📂 data/  
│   └── 📄 Footer.md  
├── 📂 src/  
│   ├── 📁 V. X.XX/  
│   │   ├── 🌐 Sprache 1/  
│   │   │   └── 📘 Sprache 1 Sphinx-Projekt/  
│   │   └── 🌐 Sprache 2/  
│   │       └── 📘 Sprache 2 Sphinx-Projekt/  
│   ├── 📁 V. Y.YY/  
│   ├── 📁 V. Z.ZZ/

Anschließend eine Konsole öffnen, in das Hauptverzeichnis des Projekts wechseln (in unserem Beispiel `Easy_versioning_Sphinx/`) und folgenden Befehl ausführen: `Easy_versioning_build`

Der Befehl `Easy_versioning_build` akzeptiert bis zu zwei optionale Parameter:

1. **Hauptsprache** (Zeichenkette): Diese dient zur sicheren Weiterleitung, falls eine Sprachversion in bestimmten Versionen der Dokumentation fehlt. Die hier angegebene Sprache muss in allen Versionen vorhanden sein.

2. **Behandlung der Quell-Dateien** (Ganzzahl): Wenn dieser Wert auf `0` gesetzt wird, bleiben die `.md`-Quelldateien im finalen Projekt erhalten. Andernfalls werden sie automatisch gelöscht, um das Projekt kompakter und leichter zu hosten.

Werden keine Parameter übergeben, wird standardmäßig **Englisch** als Hauptsprache gesetzt und die Quelldateien aus der finalen Build entfernt.

Die Dateien im `src/`-Verzeichnis werden **niemals verändert oder gelöscht**. Die Parameter betreffen ausschließlich das finale Build-Ergebnis.

## Formular zum Wechseln von Version/Sprache

Wird zusätzlich zur `src/`-Struktur ein `data/`-Verzeichnis mit einer Datei `footer.md` angelegt, kann der Footer der Dokumentation angepasst werden, einschließlich eines Formulars zum Wechseln von Version und Sprache.

Ein funktionierendes Beispiel von `footer.md` ist hier zu finden: [GitHub](https://github.com/Quadra-Ryo/Easy-versioning-sphinx/blob/main/Easy_versioning/footer.md).  
Falls kein `data/footer.md` vorhanden ist, wird das Standard-Template aus dem Link verwendet.