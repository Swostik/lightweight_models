# ROC & PR Report

Generated: 2025-12-21T23:16:36

## Overview
- ROC AUC: **0.9176**
- PR AUC: **0.9326**
- Test accuracy (model.evaluate): **0.7660**, Test loss: **0.9475**

## Threshold analysis
- Evaluated threshold: **0.835**
- Confusion matrix (tn, fp, fn, tp): (137, 97, 12, 378)
- Accuracy at threshold: **0.8253**
- Precision (Pneumonia) at threshold: **0.7958**
- Recall / Sensitivity (Pneumonia) at threshold: **0.9692**
- Specificity (Normal) at threshold: **0.5855**
- F1 (Pneumonia) at threshold: **0.8740**

## Interpretation / Key points
- ROC AUC of ~0.92 indicates strong overall separability between classes.
- PR AUC confirms good precision–recall tradeoff given class imbalance.
- At threshold 0.835, model favors high sensitivity for Pneumonia (recall = 0.969)
- This comes at the cost of lower specificity (many false positives among Normal cases).

## Recommendations
- If clinical goal prioritizes catching all Pneumonia cases (high sensitivity), keep a high threshold that preserves recall; else raise threshold to reduce false positives.
- Consider reporting both sensitivity and specificity (or plotting operating point on ROC) when choosing production threshold.
- Combine threshold tuning with calibration, class-weighted training, or sampling if false positive burden is high.

## Diagnostics to run next (if desired)
- Inspect prob. histograms for both classes (to confirm separability and overlap).
- Evaluate metrics at multiple thresholds (precision/recall/f1) and choose based on operational cost.
- Calibrate probabilities (Platt scaling / isotonic) if probability values are used directly for decisions.

## Raw numbers / arrays (short)
- Number of test samples: 624
- ROC AUC (raw): 0.917636
- PR AUC (raw): 0.932638

## Files / saved artifacts
- (This script does not save plots. To save annotated ROC/PR plots, run plotting code and save figures.)

## Full classification report

```
              precision    recall  f1-score   support

      NORMAL       0.92      0.59      0.72       234
   PNEUMONIA       0.80      0.97      0.87       390

    accuracy                           0.83       624
   macro avg       0.86      0.78      0.79       624
weighted avg       0.84      0.83      0.81       624

```