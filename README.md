# ODPC
Open Data Portal Crawler Master Projekt


Das erstellte ETL-Tool zur Untersuchung in der Masterarbeit 
_"Datenqualität deutscher Open Data Angebote - Implementierung eines ETL-Tools und Analyse vergleichbarerPortallösungen"_

Eine Untersuchung wird von *OGDPortalAnalyzer.py* aus gestartet.

Diese lädt die eruierten Portale in *portale_gesamt_sortiert.csv* und über gibt sie sequentiell an den Crawler.
Dieser extrahiert, transformiert und lädt die Datensätze aller qualifizierenden Portale in die *testdb.db*.\
Anschließend wird die *rawDataValidation.py"* ausgeführt, welche alle ermittelten Rohdaten auf den Dateityp testet
und falls dieser validierbar ist, die Datei herunterlädt, die Validierung vornimmt, die Datei wieder löscht und das
Ergebnis in die testdb.db lädt.\
Abschließend wird die *qualityAnalyer.py* ausgeführt, welche die Funktionen zur Analyse der Datenqualität nach dem 
in der Arbeit erarbeiteten Framework ausführt. Die Analyseergebnisse werden in der framework.db gespeichert.\
\
Alle Teile sind auch einzeln voneinander nutzbar.\
\
Die in der der Arbeit präsentierten Ergebnisse sind durch diesen Status des Codes entstanden.\
\
Zu beachten:
* Der Code wurde stellenweise aus bereits vorhandenen _eigenen_ Projekten übernommen und wechselt dadurch
häufiger zwischen Englisch und Deutsch. Vor allem in den Beschreibungen.
* Dadurch kommt es zu unterschiedlichen Stilen in der Umsetzung und in der Projektstruktur. Für frisch entstandene Teile wurde zumeist
aus Zeitgründen die erste funktionierende Version genommen und wenig optimiert.
* Es gibt eine Menge Todos :)
* Die testdb.db ist zu groß zum Uploaden. Kann auf Wunsch gerne bei mir angefragt werden.
