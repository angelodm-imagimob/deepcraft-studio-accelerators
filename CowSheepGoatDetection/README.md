# Cow Sheep Goat Detection

This project is designed to work exclusively with DEEPCRAFT™ Studio. Download it from [here](https://softwaretools.infineon.com/assets/com.ifx.tb.tool.deepcraftstudio)

## Overview - Use-Case

The **Cow Sheep Goat Detection** project builds an end-to-end system that identifies **cows**, **sheep**, and **goats** from camera or live video input.

The object detection model is YOLO-based and it can be used in applications for

- **Livestock monitoring:** Detect cows, sheep, and goats in barn, pasture, or farm cameras
- **Precision agriculture:** Count and track animals for herd management and automated farm systems
- **Farm security:** Flag livestock in a camera view for alerting or access control around barns and paddocks

Users can further expand this project by training their own models, importing new data, and evaluating performance using the provided tools.

- **Machine learning method:** YOLO-based object detection trained in DEEPCRAFT™ Studio
- **Sensor and data type:** RGB camera or live video input (image data)
- **Why it matters:** Enables livestock monitoring and farm automation from live camera feeds, provided the model is trained on images that match the deployment camera.

## Features

1. **Real-Time Detection**: The project uses a YOLO-based model to detect and classify cows, sheep, and goats accurately and in real-time.
2. **Custom Data Integration**: Users can add new data through the data import or using `Object Detection Data Collection Graph UX` template and label their own data for model training.
3. **Model Evaluation**: Evaluate trained models by double-clicking the `.tflite` file; it will generate a Graph UX project to run.

## Contents

- **`Data`**: Contains starter data from Roboflow with images of cows, sheep, and goats: [Cow sheep goat datasets](https://universe.roboflow.com/search?q=cow%20sheep%20goat%20object%20detection). Data consists of 8,317 annotated sessions (7,450 cow, 5,556 sheep, 4,585 goat bounding boxes), grouped into class folders (`cow_dataset*`, `sheep_dataset*`, `goat_dataset*`). Sources mix dedicated cattle, sheep, and goat sets with a multi-class livestock set that is split by the class in each image, including close-up farm views so animals occupy a usable fraction of the 320 px training image. Labels that were too small at that training size were removed.

- **`Models`** - Stores the trained YOLO-based model and its quantized versions as well as their predictions.

- **`Resources`** - Folder containing supporting project files, including `rename_mapping.csv` and `rename_mapping.json` which map the current session image names back to their original Roboflow source filenames.

## Steps to get started: Model Training and Evaluation

1. Train the YOLO-based model using the provided dataset or custom data.
2. Download the trained model `.tflite` file from the trained job.
3. Double-click the `.tflite` file and it will create a Graph UX project.
4. Run the Graph UX project to evaluate model performance in real time using the selected camera.
5. Put in front of the camera pictures with cows, sheep, and goats and observe detection from live camera.

## Sensor(s) & Data

Image data is stored as DEEPCRAFT™ Studio object-detection sessions under `Data/`. Each session contains a JPG image and `LabelXml` annotations with normalized center bounding boxes (`X`, `Y`, `Width`, `Height`). The project currently contains 8,317 sessions targeting cows, sheep, and goats.

**Small-box cleaning:** Sessions were filtered so tiny labels do not remain in the training set. At the 320 px training size, boxes whose shorter side is under 24 px are dropped, and images that would be left with unlabeled animals after that cut are skipped entirely. Distant specks that a 320 px detector cannot localize reliably are therefore not used as positives.

**Training augmentation:** DEEPCRAFT™ Studio Augmentation Settings in this project's `.improj` are chosen for upright farm animals at 320 px rather than for extreme viewpoint change. Rotation is mild (`degrees` 5) and translation is modest (`translate` 0.1); scale (`scale` 0.2) and mosaic (`mosaic` 0.5) are kept below the YOLO defaults so distant animals are not shrunk further. Flip left/right is on (`fliplr` 0.5); flip up/down, shear, and perspective are off so animals stay the right way up. HSV saturation (`hsv_s` 0.35) and brightness (`hsv_v` 0.4) cover outdoor lighting, with a small hue shift (`hsv_h` 0.015). Parameter names follow [YOLO data augmentation](https://docs.ultralytics.com/guides/yolo-data-augmentation).

Data sources and commercial-use conditions:

- `cow_dataset1` (1290 images, MIT): https://universe.roboflow.com/jaaz/cattle-xbqql
  - Dedicated cattle dataset. The `Cattle` class is mapped to `cow`.
- `cow_dataset2` (1573 images, CC BY 4.0): https://universe.roboflow.com/deep-learning-in-livestock/goat-sheet-and-cow-detection
  - Cow sessions from the multi-class livestock set (version 2, no generated augmentations). Boxes whose shorter side is under 24 px at the 320 px training image size are dropped before sessions are written.
- `sheep_dataset1` (630 images, CC BY 4.0): https://universe.roboflow.com/sheeprecognition-7a7fq/sheep-v2-db0s6
  - Dedicated sheep dataset. Images that still contained a box under 24 px at the 320 px training size were left out, so remaining sessions stay fully annotated.
- `sheep_dataset2` (1343 images, CC BY 4.0): https://universe.roboflow.com/deep-learning-in-livestock/goat-sheet-and-cow-detection
  - Sheep sessions from the same multi-class livestock set as `cow_dataset2` and `goat_dataset2`.
- `sheep_dataset3` (820 images, CC BY 4.0): https://universe.roboflow.com/benedict-project/sheep-svfcb
  - Natural farm and pasture sheep photographed at close and medium range. Version 5 carries no generated augmentations. Images containing any sheep whose shorter side is under 24 px at the 320 px training image size are skipped entirely.
- `goat_dataset1` (500 images, CC BY 4.0): https://universe.roboflow.com/z-firewood-house/goat-5eecg
  - Domestic goats photographed on farms and pastures, with varied breeds, poses, and backgrounds.
- `goat_dataset2` (1204 images, CC BY 4.0): https://universe.roboflow.com/deep-learning-in-livestock/goat-sheet-and-cow-detection
  - Goat sessions from the same multi-class livestock set as `cow_dataset2` and `sheep_dataset2`.
- `goat_dataset3` (957 images, CC BY 4.0): https://universe.roboflow.com/karthik-a3uja/goat-olvnd
  - Close-up goats on farms, village roads, and pastures. The export bakes in three augmented copies per photo, so only one copy per original image is imported. Images containing any goat whose shorter side is under 24 px at the 320 px training image size are skipped entirely.

## Adding More Data

You can add more data to the project following the steps below to improve detection or to include new classes.

1. Use `Object Detection Data Collection Graph UX` template to collect and label new data.
2. Import data to your project and retrain to get an updated model.

You can also import data from any other source (for example, your own images or another dataset) as long as it follows the DEEPCRAFT™ Studio object-detection format: images with matching `LabelXml` annotations using normalized center coordinates (`X`, `Y`, `Width`, `Height`). See [Bring your own data for object detection projects](https://developer.imagimob.com/deepcraft-studio/data-preparation/bring-your-data/bring-your-own-data-object-detection).

## Steps to Production

The recommended path to production for this project includes the following steps:

- **Add more data if detection rate is low.** The starter dataset has 8,317 sessions across pasture, barn, and mixed lighting conditions, but performance can drop on your target camera (for example, a fixed barn view, drone, or low-resolution feed). Collect and label images from the actual deployment scene—same angle, distance, and lighting—and retrain until cows, sheep, and goats are detected reliably in that environment.
- **Add more classes if needed.** The project currently detects `cow`, `sheep`, and `goat` only. If your product must distinguish breeds, calves vs adults, or other farm animals, add new classes and label accordingly before retraining.
- **Add negative data, including other animals.** Include empty scenes and look-alikes so the model does not treat every four-legged shape as a cow, sheep, or goat. For a more robust model, add images of **other animals**—horses, donkeys, deer, dogs, pigs, llamas, and similar livestock or wildlife that can appear on a farm—as unlabeled negatives, then retrain.
- **Watch sheep vs goat confusion.** The two species overlap in pose and coat; extra close-up examples from your farm reduce mix-ups that distant pasture shots cannot fix alone.
- **Match augmentation to outdoor variability.** Keep flip up/down off for upright animals; increase flip left/right for varied approach angles; adjust HSV for sun, shade, and indoor barns. Keep scale and mosaic moderate if many animals occupy only a small part of the frame.
- **Tune confidence for your sensitivity target.** Missing an animal may under-count a herd; a false detection may trigger a wasted alert—set thresholds for the cost you care about.

Some points to highlight:

- **Increase data variability:** Collect data from different environments, cameras, lighting conditions, distances, and backgrounds. Use DEEPCRAFT™ Studio augmentation settings (flip, scale, brightness, exposure) to increase image variability for vision models.
- **Keep test data independent:** Make sure the test set is not used in train or validation and reflects scenarios where the model must generalize.
- **Add negative data:** Include images without cows, sheep, or goats, and images of **other animals**, so the model stays robust against false positives.

## Attribution & Citation

@misc{
cattle-xbqql_dataset,
title = { Cattle Dataset },
type = { Open Source Dataset },
author = { jaaz },
howpublished = { \url{ https://universe.roboflow.com/jaaz/cattle-xbqql } },
url = { https://universe.roboflow.com/jaaz/cattle-xbqql },
journal = { Roboflow Universe },
publisher = { Roboflow },
year = { 2025 },
month = { feb },
note = { visited on 2026-09-08 },
}


@misc{
sheep-v2-db0s6_dataset,
title = { Sheep v2 Dataset },
type = { Open Source Dataset },
author = { sheeprecognition-7a7fq },
howpublished = { \url{ https://universe.roboflow.com/sheeprecognition-7a7fq/sheep-v2-db0s6 } },
url = { https://universe.roboflow.com/sheeprecognition-7a7fq/sheep-v2-db0s6 },
journal = { Roboflow Universe },
publisher = { Roboflow },
year = { 2025 },
month = { nov },
note = { visited on 2026-09-08 },
}


@misc{
goat-5eecg_dataset,
title = { Goat Dataset },
type = { Open Source Dataset },
author = { z Firewood House },
howpublished = { \url{ https://universe.roboflow.com/z-firewood-house/goat-5eecg } },
url = { https://universe.roboflow.com/z-firewood-house/goat-5eecg },
journal = { Roboflow Universe },
publisher = { Roboflow },
year = { 2022 },
month = { aug },
note = { visited on 2026-09-08 },
}


@misc{
goat-sheet-and-cow-detection_dataset,
title = { Goat, Sheet and cow detection Dataset },
type = { Open Source Dataset },
author = { Deep learning in livestock },
howpublished = { \url{ https://universe.roboflow.com/deep-learning-in-livestock/goat-sheet-and-cow-detection } },
url = { https://universe.roboflow.com/deep-learning-in-livestock/goat-sheet-and-cow-detection },
journal = { Roboflow Universe },
publisher = { Roboflow },
year = { 2024 },
month = { feb },
note = { visited on 2026-09-08 },
}


@misc{
goat-olvnd_dataset,
title = { Goat Dataset },
type = { Open Source Dataset },
author = { karthik },
howpublished = { \url{ https://universe.roboflow.com/karthik-a3uja/goat-olvnd } },
url = { https://universe.roboflow.com/karthik-a3uja/goat-olvnd },
journal = { Roboflow Universe },
publisher = { Roboflow },
year = { 2023 },
month = { jul },
note = { visited on 2026-09-08 },
}


@misc{
sheep-svfcb_dataset,
title = { Sheep Dataset },
type = { Open Source Dataset },
author = { Benedict Project },
howpublished = { \url{ https://universe.roboflow.com/benedict-project/sheep-svfcb } },
url = { https://universe.roboflow.com/benedict-project/sheep-svfcb },
journal = { Roboflow Universe },
publisher = { Roboflow },
year = { 2025 },
month = { feb },
note = { visited on 2026-09-08 },
}


## Getting Started

Please visit [developer.imagimob.com](https://developer.imagimob.com), where you can read about DEEPCRAFT™ Studio and go through step-by-step tutorials to get you quickly started.

For object-detection data formats, see [Bring your own data for object detection projects](https://developer.imagimob.com/deepcraft-studio/data-preparation/bring-your-data/bring-your-own-data-object-detection).


## Help & Support

If you need support or if you want to know how to deploy the model onto the device, please submit a ticket on the Infineon [community forum](https://community.infineon.com/t5/Imagimob/bd-p/Imagimob/page/1) DEEPCRAFT™ Studio page.
