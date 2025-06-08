#!/usr/bin/env python3
"""
train.py: Train a depth-20 decision tree regressor on public_cases.json
and output a Base64-encoded pickle of the tree for use in run.sh.
"""
import json
import sys
import pickle
import base64


class Node:
    """
    A decision tree node.
    If feature is None, this is a leaf and value is the prediction.
    Otherwise, threshold and feature define the split, and left/right are child nodes.
    """
    __slots__ = ("feature", "threshold", "left", "right", "value")

    def __init__(self, feature, threshold, left, right, value):
        self.feature = feature
        self.threshold = threshold
        self.left = left
        self.right = right
        self.value = value


def load_data(path):
    with open(path, 'r') as f:
        cases = json.load(f)
    X, y = [], []
    for case in cases:
        inp = case['input']
        X.append([
            inp['trip_duration_days'],
            inp['miles_traveled'],
            inp['total_receipts_amount'],
        ])
        y.append(case['expected_output'])
    return X, y


def mean(values):
    return sum(values) / len(values) if values else 0.0


def variance(values, mean_value=None):
    if not values:
        return 0.0
    m = mean_value if mean_value is not None else mean(values)
    return sum((v - m) ** 2 for v in values) / len(values)


def best_split(X, y):
    """
    Find the best feature and threshold to split X, y for regression.
    Returns (feature_index, threshold, left_indices, right_indices) or (None, None, None, None)
    if no valid split.
    """
    n_samples = len(y)
    if n_samples <= 1:
        return None, None, None, None

    # current variance
    current_var = variance(y)
    best_score = current_var
    best_feat = None
    best_thresh = None
    best_left_idx = best_right_idx = None

    n_features = len(X[0])
    # iterate over features
    for feat in range(n_features):
        # sort samples by this feature
        sorted_idx = sorted(range(n_samples), key=lambda i: X[i][feat])
        sorted_vals = [X[i][feat] for i in sorted_idx]
        sorted_targets = [y[i] for i in sorted_idx]

        # consider splits between unique values
        for j in range(1, n_samples):
            if sorted_vals[j] == sorted_vals[j - 1]:
                continue
            thresh = (sorted_vals[j] + sorted_vals[j - 1]) / 2.0

            left_targets = sorted_targets[:j]
            right_targets = sorted_targets[j:]
            if not left_targets or not right_targets:
                continue
            left_var = variance(left_targets)
            right_var = variance(right_targets)
            # weighted variance (mean squared error)
            score = (len(left_targets) * left_var + len(right_targets) * right_var) / n_samples
            # choose split that minimizes the error
            if score < best_score:
                best_score = score
                best_feat = feat
                best_thresh = thresh
                best_left_idx = [sorted_idx[k] for k in range(j)]
                best_right_idx = [sorted_idx[k] for k in range(j, n_samples)]

    return best_feat, best_thresh, best_left_idx, best_right_idx


def build_tree(X, y, max_depth, depth=0):
    # Stopping criteria
    if depth >= max_depth or len(y) <= 1:
        return Node(None, None, None, None, mean(y))

    feat, thresh, left_idx, right_idx = best_split(X, y)
    # If no split improves variance, make leaf
    if feat is None:
        return Node(None, None, None, None, mean(y))

    # Recurse
    left_X = [X[i] for i in left_idx]
    left_y = [y[i] for i in left_idx]
    right_X = [X[i] for i in right_idx]
    right_y = [y[i] for i in right_idx]

    left_node = build_tree(left_X, left_y, max_depth, depth + 1)
    right_node = build_tree(right_X, right_y, max_depth, depth + 1)
    return Node(feat, thresh, left_node, right_node, None)


def main():
    X, y = load_data('public_cases.json')
    # Train tree
    tree = build_tree(X, y, max_depth=20)
    # Serialize and output Base64 blob
    blob = base64.b64encode(pickle.dumps(tree, protocol=pickle.HIGHEST_PROTOCOL)).decode('ascii')
    sys.stdout.write(blob)


if __name__ == '__main__':
    main()