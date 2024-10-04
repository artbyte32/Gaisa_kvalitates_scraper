# Gaisa_kvalitates_scraper
Python skripts, kas lejupielādē datus par gaisa kvalitāti Rīgā no http://gmsd24.riga.lv/main.php. Dati NETIEK ņemti no pirmavota, un tiek pieņemts, ka mājaslapas `main.php` fails tiks regulāri atjaunināts ar aktuālo informāciju. Gaisa kvalitātes dati tiek saglabāti `.json` failā. Papildus pieejams shell skripts, kas uzstādīs crontab uzdevumu periodiskai datu skreipošanai katru dienu.

### Prasības
- Python 3.x
- Instalētas nepieciešamās Python bibliotēkas:

  ```bash
  git clone https://github.com/ArtisRu/Gaisa_kvalitates_scraper.git
  cd Gaisa_kvalitates_scraper/
  pip install -r requirements.txt
  ```

### Automātiska datu ieguve
Bash skripts `auto_monitor.sh` pievienos crontab ikdienas uzdevumu python skripta izpildei, kas saglabās datus repozitorija mapē.
  ```bash
  sudo chmod +x auto_monitor.sh
  ./auto_monitor.sh 
    Do you want to set up a cron job? (yes/no): yes
    At what time do you want to run the script daily? (HH:MM format): 10:00
    Cron job set to run daily at 10:00
  ```

### Manuāla datu ieguve
Vienkārši startējam python skriptu.
```bash
python3 air_quality.py
```

### Dati
Dati tiek saglabāti JSON formātā ērtākai programmiskai interpretēšanai. Pašlaik ir pieejami dati no 3 gaisa kvalitātes mērīšanas stacijām: Mīlgrāvja, Pārdaugavas un Centra. 
`span_information` - galvenā piesārņojošā viela (piemērā O₃ µg/m³), laiks, kad iegūti dati no pirmavota un stacijas nosaukums.

`Measurements` sadaļā redzami visi mērījumi konkrētajai stacijai, piemērā stacijai "Mīlgrāvis" redzami mērījumi `measurement` "NO₂ µg/m³ 1 h vidējā", "SO₂ µg/m³ 1 h vidējā", "O₃ µg/m³ 1 h vidējā", `labels` pulksteņa laiks, kura indekss sakrīt ar `data` sensoru mērījumiem, ik pa 1h.

Piemērs:
```
{
  "span_information": [
    "O₃ µg/m³",
    "2024.06.28 17:00",
    "„Mīlgrāvis”"
  ],
  "measurements": [
    {
      "measurement": "NO₂ µg/m³ 1 h vidējā",
      "labels": ["18:00", "19:00", ...],
      "data": [1, 7, ...]
    },
    {
      "measurement": "SO₂ µg/m³ 1 h vidējā",
      "labels": ["18:00", "19:00", ...],
      "data": [1, 1, ...]
    },
    {
      "measurement": "O₃ µg/m³ 1 h vidējā",
      "labels": ["Nav datu", "19:00", ...],
      "data": [0, 41, ...]
    }
  ]
}
```
