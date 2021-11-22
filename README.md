# Masterarbeit
Programme zur Masterarbeit: Untersuchung der Periodizität von Parabeln unter Anwendung des GridPeelings

Erklärung der Programme:

**calc.py**: 
Enthält verschiedene Hilfsprogramme.

**calcVerticalDis.py**: 
Enthält verschiedene Hilfsprogramme zur Berechnung der Distanz zwischen Parabelapproximationen und einer Parabel.

**csvStuff.py**: 
Enthält Hilfsprogramme zum Lesen und Erstellen von CSV Dateien.

**GridPeeling_ofP.py**: 
Erzeugt bei Ausführung einen Plot, der die convex-layer decomposition einer zufälligen Menge von 25 Punkten darstellt.

**display_parabola.py**: 
Ist ein Programm zur Darstellung von Gitterschälungen von Parabelapproximationen. Es erzeugt einen Plot der Ausführung die Gitterschälung der Parabel x^2/2 im Z2. Zur Änderung der Ausgangsparabel und des Gitter können die globalen Variablen *a_one,a_two,b_one,b_two,g_one,g_two* (fast) nach Belieben geändert werden. Dabei gilt:

      Gitterlänge = *g_one/g_two*   
      f(x) = *(a_one/a_two)* * x^2 + *(b_one/b_two)* * x
         
Das Programm wurde nur für positive a_one,a_two,b_one,b_two ausgelegt.

**display_vector_parabolas.py** : 
Es ist ein Programm zur Darstellung von Gitterschälungen von den in der Arbeit genannten Vektorparabeln. Es erzeugt bei Ausführung einen Plot der Schälung der in der Arbeit genannten Vektorparabel für t=6 und druckt die zeitliche Periode auf der Konsole aus. Andere Werte können durch Änderung der globalen Variablen *a* und *t* erzeugt werden. Dabei gilt *a=c_t* und *t* muss gerade sein. Es ist eine Tabelle als Kommentar eingefügt, aus der einige Werte für *a* und *t* entnommen werden können.

**investigate_specific_parabolas.py** : 
Ist ein Programm zur Erzeugung von Datensätzen zur Auswertung von Gitterschälungen von Parabelapproximationen. Es erzeugt bei Ausführung einen Order namens *All Data* und erzeugt den Datensatz aus der Masterarbeit, der für lineare Glieder ungleich 0 erzeugt wurd. Dafür wird eine CSV Datei erstellt, die die Ergebnisse beinhaltet. ACHTUNG: Dieser Prozess kann mehrere Stunden dauern. (sollte allerdings kürzer als 4 Stunden dauern). Die Größe des Datensatzes kann durch Anpassung der Schleifen, in der die main Methode ausgeführt wird angepasst werden. Der Ordnername des Ordners, in den die Dateien geschrieben werden sollen, kann durch Veränderung der Variable *path* erfolgen. Wenn man die globale Variable *writeLogs* auf *True* setzt werden für jede untersuchte Parabel verschiedene Logs, die jedes Peeling speichern, erzeugt. Das ist notwendig, wenn man untersuchen will, wieviele Elemente maximal durch die Korrektur verändert werden. Achtung, das können sehr schnell, sehr viele Dateien werden, die auch sehr groß werden können. Nur wenn wirklich notwendig aif *True* setzen.

**readinvestigateLogs.py** : 
Es ist ein Programm zur Darstellung der durch  **investigate_specific_parabolas.py** erzeugten Logs. Es erzeugt bei Ausführung einen Plot der vertikalen Perioden des Datensatzes aus der Masterarbeit von den Parabeln mit linearem Glied ungleich 0. Durch Änderung der Variable displaycase können unterschiedliche Plots erzeugt werden:

displaycase = 1 : Vertikale Periode in Abhängigkeit von a.

displaycase = 2 : Durchschnittliche vertikale Translation der Schälungen in einer zeitlichen Periode in Abhängigkeit von a.

displaycase = 3 : Maximale Schlauchdicke der konvexen Hüllen der Schälungen in einer zeitlichen Periode in Abhängigkeit von a.

displaycase = 4 : Durchschnittliche vertikale Translation der Schälungen in einer zeitlichen Periode in Abhängigkeit von b bei den Grenzfällen a= 1/2;1/8;1/22;1/44.

displaycase = 5 : Zeitliche Periode in Abhängigkeit von b bei den Grenzfällen a= 1/2;1/8;1/22;1/44.

displaycase = 6 : Durchschnittliche Schlauchdicke der konvexen Hüllen der Schälungen in einer zeitlichen Periode in Abhängigkeit von b bei den Grenzfällen a= 1/2;1/8;1/22;1/44.

Die für die Plots zugrunde liegenden Dateien befinden sich in dem Ordner *Logs*.  


**read_Logs_correction_change.py**: 
Dieses Programm dient der Analyse der Korrektur der konvexen Hüllen. Es enthält die beiden Funktionen: *createMaxDifferencesLog(Foldername)* und *displayMaxDifferences(Foldername)*. Die Funktion *createMaxDifferencesLog* analysiert einen Datensatz, der durch **investigate_specific_parabolas.py** erstellt wurde. Wichtig: die Variable *writeLogs* musste auf True gesetzt sein, damit es funktioniert. *Foldername* ist der Name des Ordners, in dem sich die Logs befinden. Dadurch wird eine csv Datei mit dem Namen *change.csv* erstellt, in der die Änderungen durch die Korrektur dargestellt sind. Nachdem *createMaxDifferencesLog* ausgeführt wurde kann *displayMaxDifferences* ausgeführt werden, dass die Anzahl korrigierter Punkte in Abhängkeit von *a* darstellt.


