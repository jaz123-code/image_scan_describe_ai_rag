def learn_auto_approval_threshold(records, target_accuracy=0.90):
    """
    records: list of tuples (confidence, is_correct)
    """
    records = sorted(records, key=lambda X: X[0], reverse=True)
    correct = 0
    total = 0
    for con, is_c in records:
        total += 1
        if is_c:
            correct += 1
        accuracy = correct / total
        if accuracy>=target_accuracy:
            return con
    return 1.0