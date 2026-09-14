# Evaluation Results: yolo26n-size320-batch16-epoch200

- **Project type:** ObjectDetection
- **Classes:** 4

## Train

| Metric | Value |
| --- | --- |
| Accuracy | 0.9918 |
| F1 Score | 0.9918 |
| mAP@0.5 | 0.9947 |
| mAP@0.5:0.95 | 0.8834 |

### Per-class mAP

| Class | mAP@0.5 | mAP@0.5:0.95 |
| --- | --- | --- |
| black_measles | 0.9940 | 0.8851 |
| black_rot | 0.9949 | 0.8884 |
| leaf_blight | 0.9950 | 0.9015 |
| healthy | 0.9950 | 0.8585 |

### Confusion Matrix

| True \ Pred | (none) | black_measles | black_rot | leaf_blight | healthy |
| --- | --- | --- | --- | --- | --- |
| (none) | 0 | 109 | 23 | 53 | 4 |
| black_measles | 7 | 1032 | 0 | 0 | 0 |
| black_rot | 2 | 0 | 832 | 0 | 0 |
| leaf_blight | 0 | 0 | 0 | 779 | 0 |
| healthy | 0 | 0 | 0 | 0 | 407 |

## Validation

| Metric | Value |
| --- | --- |
| Accuracy | 0.9798 |
| F1 Score | 0.9797 |
| mAP@0.5 | 0.9697 |
| mAP@0.5:0.95 | 0.8590 |

### Per-class mAP

| Class | mAP@0.5 | mAP@0.5:0.95 |
| --- | --- | --- |
| black_measles | 0.9198 | 0.8279 |
| black_rot | 0.9688 | 0.8696 |
| leaf_blight | 0.9950 | 0.8952 |
| healthy | 0.9950 | 0.8432 |

### Confusion Matrix

| True \ Pred | (none) | black_measles | black_rot | leaf_blight | healthy |
| --- | --- | --- | --- | --- | --- |
| (none) | 0 | 20 | 11 | 28 | 1 |
| black_measles | 26 | 319 | 0 | 0 | 0 |
| black_rot | 6 | 0 | 269 | 0 | 0 |
| leaf_blight | 0 | 0 | 0 | 259 | 0 |
| healthy | 1 | 0 | 0 | 0 | 134 |

## Test

| Metric | Value |
| --- | --- |
| Accuracy | 0.9744 |
| F1 Score | 0.9743 |
| mAP@0.5 | 0.9649 |
| mAP@0.5:0.95 | 0.8573 |

### Per-class mAP

| Class | mAP@0.5 | mAP@0.5:0.95 |
| --- | --- | --- |
| black_measles | 0.9012 | 0.8098 |
| black_rot | 0.9687 | 0.8663 |
| leaf_blight | 0.9950 | 0.8992 |
| healthy | 0.9947 | 0.8539 |

### Confusion Matrix

| True \ Pred | (none) | black_measles | black_rot | leaf_blight | healthy |
| --- | --- | --- | --- | --- | --- |
| (none) | 0 | 39 | 11 | 19 | 2 |
| black_measles | 33 | 321 | 0 | 0 | 0 |
| black_rot | 7 | 0 | 270 | 0 | 1 |
| leaf_blight | 0 | 0 | 0 | 262 | 1 |
| healthy | 1 | 0 | 0 | 0 | 140 |
