# VJCMS (Viola Jones Cam-Shift)

## Modus

### detect

Im ``` detect``` Modus werden Objekte nur erkannt und die entsprechende Bounding-Box nur für einem Frame in der Preview angezeigt. Des eigentliche sind hinter diesem Modus ist die kontinuierliche Bereitschtellung von Positionsdaten der im Stream detektierten Objekte.

### detect_and_track

Der ``` detect_and_track``` Modus dient eher einem Debugging als einer tatsächlichen Anwendung. Objekte im Stream werden nicht nur erkannt, sondern auch für eine gewisse Zeit mittels Cam-Shift getrackt.

## Exceptions (utils/VJ_Exceptions)

Es gibt zwei custom Exception Klassen:
- CameraNotConnected
- InvalidMode

Eine Exception aus einer dieser beiden Klassen führt automatisch zur Beendigung des Programs.
## Output
Die Ausgabe über Monitor und Stream wird in späteren Versionen evnetuell zusammengelegt und über das Modul `VideoStream` abgehndelt.
## Monitor (VideoStream)

Die Ausgabe auf dem Monitor geschieht zur Zeit noch direkt über `cv2.imshow()`.


### Stream

`TODO ` Stream der Frames entweder via UDP oder TCP Stream. Alternativ könnte auch ein Umweg über VLC möglich sein. In einem ersten Versuch war keine der Möglichkeiten vernünftig umsetzbar.

### Output-Generator (utils/vj_output)

`TODO ` Je nach Spezifikation soll über dieses Modul eine für das Projekt nutzbare Ausgabe erstellt werden...

### Logging (utils/VJ_Logging)

Für das Logging gibt es genau drei Modus, INFO, WARNING und ERROR. Diese werden durch folgende IDs repräsentiert.

| ID | Klasse|
|---|---|
| 0 | INFO|
| 1 | WARNING |
| 2 | ERROR |

Im Standard wird nur ERROR (2) angezeigt. Über `--verbose` kann das level entsprechend gesetzt werden.
Neben dem Logging auf der Konsole wird eine Log-file im Verzeichnis erstellt. Diese enthält die Ereigenisse des Logging-Levels, inklusive der Auflistung der erkannten Objekte.

```
[Sat Feb 17 10:46:14 2018][INFO]      [main] starting program
[Sat Feb 17 10:46:14 2018][INFO]      [main] streaming to monitor
[Sat Feb 17 10:46:14 2018][INFO]      [main] DEBUG 1
[Sat Feb 17 10:46:14 2018][INFO]      [main] MODE 0
[Sat Feb 17 10:46:14 2018][INFO]      [main] VERBOSE 0
[Sat Feb 17 10:46:14 2018][INFO]      [detect_and_track] Begin detect_and_track
[Sat Feb 17 10:46:14 2018][INFO]      [detect_and_track] starting Thread for Viola
[Sat Feb 17 10:46:14 2018][INFO]      [detect_and_track] opening input stream
[Sat Feb 17 10:46:14 2018][OBJECT]    [Cone](351,102) (552,240)
[Sat Feb 17 10:46:14 2018][OBJECT]    [Cone](183,141) (252,180
```
