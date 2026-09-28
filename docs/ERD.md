# ERD & Data Lineage

## Arsitektur lapisan

```
 SOURCES            STAGING (DuckDB)        MARTS (DuckDB + Parquet)
┌─────────────┐     ┌──────────────────┐    ┌──────────────────────────┐
│ World Bank  │────►│ stg_wb_indicators│───►│ mart_food_price_index    │
│ Open Data   │     │  (long format)   │    │ mart_inflation           │
└─────────────┘     └──────────────────┘    │ mart_food_security       │
┌─────────────┐     ┌──────────────────┐    │ mart_asean_ranking       │
│ Frankfurter │────►│ stg_fx           │    └──────────────────────────┘
│ (kurs)      │     └──────────────────┘              │
└─────────────┘                                       ▼
                                    ┌─────────────────────────────────┐
                                    │ dashboard.py · alerts.py · tests │
                                    └─────────────────────────────────┘
```

## ERD (relasi marts)

```
                    mart_food_security
                    ╔═══════════════════╗
                    ║ country_iso  (PK) ║
                    ║ year         (PK) ║
                    ║ country           ║
                    ║ price_index       ║
                    ║ inflation_pct     ║
                    ║ food_prod_index   ║
                    ║ food_import_pct   ║
                    ║ fertilizer_per_ha ║
                    ║ pop_growth_pct    ║
                    ╚═════════╤═════════╝
                              │ 1:N (country_iso, year)
              ┌───────────────┼───────────────────┐
              ▼               ▼                   ▼
  ╔═══════════════════╗ ╔════════════════╗ ╔══════════════════╗
  ║ mart_food_price   ║ ║ mart_inflation ║ ║ mart_asean_      ║
  ║ _index            ║ ║                ║ ║ ranking          ║
  ║ country_iso (PK)  ║ ║ country_iso PK ║ ║ year (PK)        ║
  ║ year (PK)         ║ ║ year (PK)      ║ ║ country_iso (PK) ║
  ║ price_index       ║ ║ inflation_pct  ║ ║ rank_inflation   ║
  ║ yoy_pct           ║ ║ alert          ║ ║ rank_production  ║
  ║ yoy_flag          ║ ║                ║ ║                  ║
  ╚═══════════════════╝ ╚════════════════╝ ╚══════════════════╝
```

## Lineage kolom kunci

| Kolom marts | Asal | Transformasi |
|---|---|---|
| `price_index` | `FP.CPI.TOTL` | pivot langsung |
| `yoy_pct` | `price_index` | `(now − LAG(now)) / LAG(now) × 100` |
| `yoy_flag` | `yoy_pct` | `>=7 → spike`, `>=3 → elevated`, else normal |
| `inflation_pct` | `FP.CPI.TOTL.ZG` | langsung |
| `alert` | `inflation_pct` | `>= 5.0` |
| `food_prod_index` | `AG.PRD.FOOD.XD` | pivot |
| `food_import_pct` | `TM.VAL.FOOD.ZS.UN` | pivot |
| `rank_inflation` | `inflation_pct` | `RANK() OVER (PARTITION year ORDER BY ASC)` |

## Indikator World Bank yang dipakai

| Kode | Nama | Kategori |
|---|---|---|
| `FP.CPI.TOTL` | Consumer price index (2010=100) | Harga |
| `FP.CPI.TOTL.ZG` | Inflation, consumer prices (annual %) | Harga |
| `AG.PRD.FOOD.XD` | Food production index (2014-2016=100) | Produksi |
| `TM.VAL.FOOD.ZS.UN` | Food imports (% merchandise imports) | Perdagangan |
| `AG.CON.FERT.ZS` | Fertilizer consumption (kg/ha) | Input |
| `SP.POP.GROW` | Population growth (annual %) | Demografi |

## Negara

`IDN` Indonesia · `MYS` Malaysia · `THA` Thailand · `VNM` Vietnam · `PHL` Philippines
