from __future__ import annotations

import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)


def evaluate(
    model,
    test_generator,
    name: str = "model",
    threshold: float = 0.5,
    flip=None,
    class_weights: str = "None",
):
    test_generator.reset()
    probs = model.predict(test_generator, verbose=0).ravel()
    y_true = test_generator.classes

    auroc = roc_auc_score(y_true, probs)
    auprc = average_precision_score(y_true, probs)

    preds = (probs >= threshold).astype(int)
    cm = confusion_matrix(y_true, preds)

    acc = accuracy_score(y_true, preds)
    macro_f1 = f1_score(y_true, preds, average="macro")
    weighted_f1 = f1_score(y_true, preds, average="weighted")

    specificity = recall_score(y_true, preds, pos_label=0)  # Normal recall
    sensitivity = recall_score(y_true, preds, pos_label=1)  # Pneumonia recall
    precision_pos = precision_score(y_true, preds, pos_label=1, zero_division=0)

    print(f"\n=== {name} @ threshold {threshold:.3f} ===")
    print(cm)
    print(
        classification_report(
            y_true,
            preds,
            target_names=["NORMAL", "PNEUMONIA"],
            zero_division=0,
        )
    )
    print(f"AUROC: {auroc:.4f} | AUPRC: {auprc:.4f}")
    print(f"Macro F1: {macro_f1:.4f} | Weighted F1: {weighted_f1:.4f}")
    print(
        f"Sensitivity: {sensitivity:.4f} | Specificity: {specificity:.4f} | Precision: {precision_pos:.4f}"
    )

    return {
        "Model": name,
        "Flip": flip,
        "Class Weights": class_weights,
        "Threshold": threshold,
        "AUROC": auroc,
        "AUPRC": auprc,
        "Accuracy": acc,
        "Macro F1": macro_f1,
        "Weighted F1": weighted_f1,
        "Sensitivity": sensitivity,
        "Specificity": specificity,
        "Precision": precision_pos,
        "TN": cm[0, 0],
        "FP": cm[0, 1],
        "FN": cm[1, 0],
        "TP": cm[1, 1],
    }


def eval_thresholds(model, generator, thresholds):
    generator.reset()
    probs = model.predict(generator, verbose=0).ravel()
    y_true = generator.classes

    rows = []

    for t in thresholds:
        preds = (probs >= t).astype(int)
        cm = confusion_matrix(y_true, preds)

        rows.append(
            {
                "Threshold": t,
                "Accuracy": (cm[0, 0] + cm[1, 1]) / cm.sum(),
                "Macro F1": f1_score(y_true, preds, average="macro"),
                "Weighted F1": f1_score(y_true, preds, average="weighted"),
                "Specificity": recall_score(y_true, preds, pos_label=0),
                "Sensitivity": recall_score(y_true, preds, pos_label=1),
                "FN": cm[1, 0],
                "FP": cm[0, 1],
            }
        )

    return pd.DataFrame(rows).round(3)

