
# Wikipedia Scraper

[![forthebadge made-with-python](https://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)

## [🌎](https://emojipedia.org/globe-showing-americas)Description

The Earth is a big planet, there are a lot of different countries and cultures, and thoroughout history, there have been many different leaders for each of these. But maybe it's not that simple to find information on past leaders for countries you don't know the history of. Well, thankfully, someone's got you covered!

This script retrieves data from an API, and organizes data into different countries, and organizing each leader in their countries, as well as adding some small information on them.

![earth](https://img.freepik.com/premium-photo/planet-earth-with-realistic-geography-surface-orbital-3d-cloud-atmosphere_31965-35388.jpg)

## 📦 Repo structure

```
.
├── countries/
│   ├── be.csv
│   ├── fr.csv
│   ├── ma.csv
│   ├── ru.csv
│   └── us.csv
├── src/
│   └── scraper.py
├── .gitignore
├── leaders.json
├── main.py
└── README.md
```

## 🛎️ Usage

1. Clone the repository to your local machine.
2. To run the script, you can execute the `main.py` file from your command line:
   ``python main.py``
3. The script does everything automatically. It will grab data from the API, and creates a few files. To read the raw output, you can open, after execution, leaders.json. If you want the data in a more readable and organized format, check the countries folder, and the files inside.

## ⏱️ Timeline

This project took three days for completion.

## 📌 Personal Situation

This project was done as part of the AI Boocamp at BeCode.org.
