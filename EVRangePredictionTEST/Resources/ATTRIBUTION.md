# Attribution

Starter training data in this accelerator is commercially licensed for model training. Credit the original authors in any product documentation.

## BMW i3 trips — CC BY 4.0

Steinstraeter, Matthias; Buberger, Johannes; Trifonov, Dimitar (Technical University of Munich). *Battery and Heating Data in Real Driving Cycles.* IEEE DataPort. https://ieee-dataport.org/open-access/battery-and-heating-data-real-driving-cycles  
Kaggle mirror: https://www.kaggle.com/datasets/atechnohazard/battery-and-heating-data-in-real-driving-cycles  
License: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)

## Vehicle Energy Dataset (VED) — Apache 2.0

Oh, Geunseob; LeBlanc, David J.; Peng, Huei. *Vehicle Energy Dataset (VED), A Large-scale Dataset for Vehicle Energy Consumption Research.* https://github.com/gsoh/VED  
License: [Apache License 2.0](https://github.com/gsoh/VED/blob/master/LICENSE)

This project uses **PHEV/EV rows only** (2013 Nissan Leaf and plug-in hybrids). Do not add SpritMonitor, d-EVD (CC BY-NC-SA), or EV-Database scrapes.

## On datasets that log range directly

Neither source above records remaining range, and no public EV dataset that does is licensed for commercial use. The closest candidates are both excluded here:

- [TUM electric-vehicle-uds-dataset](https://github.com/tumftm/electric-vehicle-uds-dataset) — VW ID.3 and CUPRA Born, 72,000 km, with SoC and distance. **CC BY-NC 4.0**, non-commercial.
- [d-EVD](https://github.com/Vicomtech/d-EVD_dual-Electric-Vehicle-Dataset) — built specifically for battery range prediction from OBD-II trips. **CC BY-NC-SA 4.0**, non-commercial and share-alike.

This is why the project predicts measured energy per kilometre and leaves the range division to the application.
