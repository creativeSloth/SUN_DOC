# Example data

Dummy source documents and an empty target directory used to demo the
**Article Fetcher** module without needing real customer files.

```
example_data/
├── source/                          # source directory for the fetcher
│   ├── inverters_and_modules/
│   │   ├── 000004_Solar_Panel_400W.pdf
│   │   ├── 000005_Wechselrichter_5kW.docx
│   │   ├── 000006_Batteriespeicher_10kWh.pdf
│   │   ├── 000016_PV_Modul_450W.pdf
│   │   └── 000017_Stringwechselrichter_10kW.docx
│   └── cables_and_misc/
│       ├── 000001_Messgeraet_Typ_A.pdf
│       ├── 000002_Sensor_Typ_B.docx
│       ├── 000003_Kabel_5m.pdf
│       ├── 000007_DC_Kabel_6mm_10m.pdf
│       └── 000008_AC_Kabel_3x2_5mm_5m.docx
└── target/                          # empty, receives copies on demo run
    └── .gitkeep
```

The filenames start with the article number (`000001`, `000004`, …) so
they match the `articles.article_no` values seeded by the Docker
Postgres stack. The fetcher matches files where the article number
appears anywhere in the filename, so the trailing description text is
cosmetic.

All files are minimal but valid PDFs / DOCX (a few hundred bytes each)
— open them in a viewer to confirm the demo pipeline produced the
expected output.

## How to use

1. Start the Postgres stack: `cd docker && docker compose up -d`
2. From a fresh clone, copy the example config so the app starts pre-configured:
   ```bash
   cp src/logs/config.example.ini src/logs/config.ini
   ```
3. Run the app from the `src/` directory: `cd src && python main.py`
4. Click the "load from DB" icon button — 50 articles appear.
5. Tick a few checkboxes, click the "copy" button.
6. Files land under `example_data/target/<project>/<timestamp>/...`.

See the main `README.md` for the full step-by-step walkthrough.
