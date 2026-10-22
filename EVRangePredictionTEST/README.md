# EV Range Prediction

This project is designed to work exclusively with DEEPCRAFT™ Studio. Download it from [here](https://softwaretools.infineon.com/assets/com.ifx.tb.tool.deepcraftstudio)

## Overview

The **EV Range Prediction** accelerator is a **time-series regression** project. It predicts **energy consumption (kWh/km) over the next 3 minutes** from 1 Hz vehicle telemetry: pack voltage and current, speed, HVAC load, ambient temperature, elevation, and state of charge (SoC).

It targets onboard range estimation, fleet energy monitoring, and PSOC Edge **current/voltage** demos (not camera-based, not IMU classification).

### What the model predicts

| Track | Role | Unit |
|---|---|---|
| `Vehicle Data` | Inputs | speed km/h, pack V, pack A, HVAC kW, ambient °C, elevation m, SoC % |
| `consumption_kwh_per_km` | Regression target | pack energy per km over the next 180 s |

**The target is measured, not modelled.** It is the logged pack voltage and current integrated over the next 180 seconds, divided by the distance the logged speed covers in that same window. No battery capacity is assumed, no state-of-charge curve is inverted, and no value is clipped. About 2–6% of windows are negative, which is real: on a descent, regeneration returns more energy than the pack delivers.

### Getting range from it

Neither source dataset logs remaining range — no public EV dataset under a commercial licence does. Range is therefore left to the application, as one division using the pack you actually ship:

```
remaining_km = usable_pack_kWh × SoC_fraction / predicted_kWh_per_km
```

Reference figures for the vehicles here: BMW i3 60 Ah ≈ **18.8 kWh** usable, 2013 Nissan Leaf ≈ **21.3 kWh**. Clamp the divisor to a sane floor so that a downhill stretch does not report infinite range.

The consumption rate spans roughly fourfold across conditions, driven by ambient temperature, HVAC load, terrain, and speed. Learning it from those conditions is the model's job; converting it into kilometres is arithmetic.

### Why the horizon is 180 s

Measured on the BMW trips, how well recent history predicts the target peaks near this horizon and collapses beyond it:

| Horizon | Negative windows | Correlation with recent past | Spread to explain (MAE vs mean) |
|---|---|---|---|
| 60 s | 3.9% | 0.456 | 0.0714 |
| **180 s** | **1.9%** | **0.469** | **0.0515** |
| 300 s | 1.6% | 0.392 | 0.0439 |
| 600 s | 1.3% | 0.045 | 0.0406 |

At ten minutes the target converges to each trip's own average and is no longer forecastable. Change `target_horizon_sec` in `scripts/configs/ev_range_prediction.json` and re-import to move it.

### How to perform / capture

There is no gesture to act out. Log the same seven channels from a vehicle CAN/OBD logger or a PSOC analog front-end at **1 Hz**, matching the column units in `vehicle.data`.

## Contents

- **`Data`** — Nested DEEPCRAFT sessions (one folder per trip)
  - `bmw_i3` — BMW i3 (60 Ah) real trips, CC BY 4.0
  - `ved_electric` — VED Nissan Leaf / PHEV trips, Apache 2.0
- **`Models`** — Trained models, predictions, and generated Edge code (after you train in Studio)
- **`Resources/ATTRIBUTION.md`** — Dataset licenses and citations
- **`Tools`** — Pointer to the import script

## Dataset

All included sessions are **resampled to 1 Hz**. This import currently includes **70 BMW i3 trips** and **120 VED Leaf/PHEV trips**. Re-run `python import_ev_range.py --fresh` to rebuild. Each session folder contains:

- `vehicle.data` — sensor track (time + 7 channels)
- `consumption_kwh_per_km.data` — regression label track (time + kWh/km over the next 180 s)
- `<session>.imsession` — Studio session file with `consumption_kwh_per_km` as the **active label track** (this is what makes the project **Regression**, not Classification)

Trips shorter than ~90 s or with almost no motion are dropped, as are trips whose pack delivers less than 0.05 kWh/km — those are plug-in hybrids running on their engine, where the battery is not doing the driving. Each session is also trimmed at the point where the forward horizon no longer covers enough distance, which removes the parked tail at the end of a trip.

### Label quality differs sharply between the two sources

The BMW logs sample pack current continuously; VED's OBD-II logger polls it on a slow round-robin and holds the last value between polls. Measured on the imported sessions:

| | Repeated current samples | Negative windows | Recent past predicts target |
|---|---|---|---|
| BMW i3 | 2.1% | 6.2% | correlation 0.29 |
| VED | 57.7% | 18.5% | correlation 0.03 |

Integrating a held current across acceleration and regeneration transients loses real energy, so **VED labels are substantially noisier and its trips are close to unpredictable on this target**. They are included for vehicle and climate variety, but use the `Dataset` custom column in Studio to evaluate the two sources separately before trusting a combined metric. If VED drags validation loss, re-import with only the BMW entry in `scripts/configs/ev_range_prediction.json`.

**Sensor scales (as stored in this project):**

| Channel | Unit | Notes |
|---|---|---|
| Speed_kmh | km/h | Vehicle speed |
| PackVoltage_V | V | HV pack voltage |
| PackCurrent_A | A | HV pack current, oriented per session so positive means discharge |
| Hvac_kW | kW | Cabin heat + A/C power |
| Ambient_C | °C | Outside / ambient temperature |
| Elevation_m | m | 0 when the source has no altitude |
| SoC_pct | % | Pack state of charge |
| Consumption_kWh_per_km | kWh/km | Label: measured pack energy per km over the next 180 s |

Loggers disagree on which current direction is positive, so each session's sign is set from its own energy integral: a driving trip must take net energy out of the pack. Regeneration then keeps its negative sign and correctly reduces consumption instead of adding to it.

### BMW i3 trips

[Battery and Heating Data in Real Driving Cycles](https://ieee-dataport.org/open-access/battery-and-heating-data-real-driving-cycles) — 72 real drives of a BMW i3 (60 Ah), summer (A) and winter (B), with pack, HVAC, speed, elevation, and ambient temperature.

License: **CC BY 4.0** (commercial use with attribution).

### VED Leaf / PHEV

[Vehicle Energy Dataset](https://github.com/gsoh/VED) — Ann Arbor OBD-II fleet. This project keeps **electric / PHEV rows only** (including the three 2013 Nissan Leaf BEVs). ICE/HEV files are not imported.

License: **Apache 2.0**.

Do **not** mix in SpritMonitor (scraping forbidden) or d-EVD (**CC BY-NC-SA**).

## Adding more data

Collect additional trips at **1 Hz** with the same seven channels and units. For regression, each recording folder needs two `.data` files with identical timestamps: sensors in `vehicle.data` and the target in `consumption_kwh_per_km.data`. In Studio, put the sensor file on the **Data** track and `consumption_kwh_per_km.data` on the **Label** track.

Log pack current as fast as the bus allows. A slow-polled, sample-and-held current channel cannot support an energy label, which is the single biggest quality difference between the two included sources.

Then:

```bash
cd ACCELERATORS/scripts
python import_ev_range.py --fresh
```

Or use **Add Data** in the Studio Data tab (nested folders). All sessions must use a `.data` file as the active label track.

Because the target is energy per kilometre rather than range, vehicles with different pack sizes can be mixed freely — a 75 kWh car and an 18 kWh car both consume in the same units. Pack size only enters the downstream range division.

## Steps to production

The included trips are a starting point. They come from a 2014-era i3 and 2013 Leaf / PHEVs in Ann Arbor. For a product, log the **target vehicle** CAN signals, the same HVAC definition, and real weather.

In Studio:

1. Open `EVRangePrediction.improj`
2. Confirm **Project type: Regression** and the preprocessor: **60 s window at 1 Hz** (`[60,7]`), prediction every 1 s
3. Train (default Conv1D, MSE)
4. Evaluate MSE / R² / residual plots on the held-out test split
5. Generate Edge code and validate on-device with live current/voltage (and SoC if available)

**Baselines to beat.** Predicting the dataset mean for every window gives an MAE of **0.069 kWh/km** on the BMW sessions and **0.177** on VED. Carrying the last 60 seconds of consumption forward does *worse* than that on both, so a model only earns its place by reading conditions — speed regime, HVAC draw, ambient temperature, elevation trend — rather than extrapolating recent draw.

A longer window (e.g. 120 s) captures hills and HVAC better but adds latency. Shorten it if you only care about instantaneous consumption.

## Attribution & citation

See `Resources/ATTRIBUTION.md`.

```
@dataset{steinstraeter2020i3,
  author    = {Steinstraeter, Matthias and Buberger, Johannes and Trifonov, Dimitar},
  title     = {Battery and Heating Data in Real Driving Cycles},
  year      = {2020},
  publisher = {IEEE DataPort},
  doi       = {10.21227/6jr9-5235}
}

@article{oh2022ved,
  author  = {Oh, Geunseob and LeBlanc, David J. and Peng, Huei},
  title   = {Vehicle Energy Dataset (VED), A Large-Scale Dataset for Vehicle Energy Consumption Research},
  journal = {IEEE Transactions on Intelligent Transportation Systems},
  year    = {2022}
}
```

## Getting Started

Visit [developer.imagimob.com](https://developer.imagimob.com) for DEEPCRAFT Studio tutorials, including [regression vs classification](https://developer.imagimob.com/deepcraft-studio/getting-started/machine-learning-algorithms) and [bring your own data](https://developer.imagimob.com/deepcraft-studio/data-preparation/bring-your-data/bring-your-own-data).

## Help & Support

Submit a ticket on the Infineon [community forum](https://community.infineon.com/t5/Imagimob/bd-p/Imagimob/page/1) Imagimob Studio page.
