# YHK Print Tool

Eine einfache Windows-Anwendung zum Drucken von **Texten** und **QR-Codes** auf günstigen Bluetooth-Thermodruckern der YHK-/TEDi-Serie.

Das Projekt entstand, weil viele dieser Drucker ausschließlich über Smartphone-Apps genutzt werden können. Dieses Tool ermöglicht den direkten Druck unter Windows – ohne Emulator und ohne proprietäre Hersteller-App.

---

## Funktionen

- ✅ Text direkt eingeben und drucken
- ✅ QR-Codes erzeugen und drucken
- ✅ Verbindung über Bluetooth (SPP / COM-Port)
- ✅ Keine Cloud
- ✅ Keine Internetverbindung erforderlich
- ✅ Open Source
- ✅ Extrem leichtgewichtig

---

## Unterstützte Drucker

Getestet mit:

- TEDi Mini Thermodrucker
- Bluetooth-Name: `YHK-XXXX`

Weitere YHK-kompatible Drucker dürften ebenfalls funktionieren.

---

## Voraussetzungen

- Windows 10 oder Windows 11
- Python 3.10 oder neuer
- Bluetooth
- Drucker bereits mit Windows gekoppelt

---

## Installation

Python installieren:

https://www.python.org/downloads/

Benötigte Pakete installieren:

```bash
pip install pyserial pillow qrcode
```

---

## Drucker koppeln

1. Bluetooth einschalten
2. Drucker einschalten
3. In Windows koppeln
4. COM-Port ermitteln

```
Win + R
```

```
control bthprops.cpl
```

oder

Gerätemanager

```
Anschlüsse (COM & LPT)
```

Beispiel:

```
COM11
```

Im Python-Code anschließend anpassen:

```python
COM_PORT = "COM11"
```

---

## Starten

```bash
python yhk_print_tool.py
```

---

## Bedienung

Text eingeben

```
Hallo Welt!
```

Button

```
Text drucken
```

oder

```
QR-Code drucken
```

---

## Beispiel

```
Marcus Dziersan
https://marcus-dziersan.de

kontakt@marcus-dziersan.de
```

oder

```
WLAN:T:WPA;
S:MeinWLAN;
P:Passwort123;;
```

als QR-Code.

---

## Bekannte Einschränkungen

- unterstützt aktuell ausschließlich Text
- unterstützt QR-Codes
- kein PDF-Druck
- keine Bilder
- keine Barcodes
- Druckbreite 384 Pixel

---

## Projektstruktur

```
.
│
├── yhk_print_tool.py
├── README.md
└── requirements.txt
```

---

## requirements.txt

```
pyserial
pillow
qrcode
```

---

## Roadmap

Geplant sind unter anderem:

- Bilder drucken
- Logo einfügen
- Mehrere QR-Codes
- Etikettenvorlagen
- Automatische Schriftgrößenanpassung
- Drag & Drop
- EXE-Version ohne Python
- Einstellbarer COM-Port
- Live-Druckvorschau
- Mehrsprachigkeit

---

## Lizenz

MIT License

Dieses Projekt steht frei zur Verfügung und darf verändert, erweitert und weitergegeben werden.

---

## Haftung

Dieses Projekt wird ohne Gewähr bereitgestellt.

Die Nutzung erfolgt auf eigene Verantwortung.

---

## Danksagung

Ein Dank geht an die Open-Source-Community für die Analyse des YHK-Druckprotokolls sowie an alle Entwickler der verwendeten Python-Bibliotheken.

---

## Autor

**Marcus Dziersan**

GitHub:
https://github.com/

Website:
https://marcus-dziersan.de
