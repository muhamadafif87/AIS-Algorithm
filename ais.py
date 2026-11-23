import math
from collections import Counter

import pandas as pd

DATASET_PATH = "Groceries_dataset.csv"
DATE_FORMAT = "%d-%m-%Y"
SUPPORT_VALUES = [0.005, 0.01, 0.02, 0.03]
CONFIDENCE_VALUES = [0.05, 0.10, 0.15, 0.20]
TOP_N_RULES = 10


def load_transactions(path):
    """Membaca dataset dan membentuk transaksi (Member_number + Date) berupa set item."""
    df = pd.read_csv(path)
    df["Date"] = pd.to_datetime(df["Date"], format=DATE_FORMAT)
    df = df.drop_duplicates(subset=["Member_number", "Date", "itemDescription"])

    return (
        df.groupby(["Member_number", "Date"])["itemDescription"]
        .apply(set)
        .tolist()
    )


def ais_algorithm(transactions, min_support):
    """Mencari frequent itemset dengan algoritma AIS."""
    min_count = math.ceil(min_support * len(transactions))

    item_counts = Counter(item for t in transactions for item in t)
    current = {
        frozenset([item]): count
        for item, count in item_counts.items()
        if count >= min_count
    }

    all_frequent = dict(current)
    levels = {1: len(current)}
    candidates_per_level = {}
    k = 1

    while current:
        # Perluas frequent itemset dengan item lain pada transaksi yang sama
        candidates = {
            itemset | {item}
            for t in transactions
            for itemset in current
            if itemset <= t
            for item in t - itemset
        }
        if not candidates:
            break

        candidates_per_level[k + 1] = len(candidates)

        counts = Counter(c for t in transactions for c in candidates if c <= t)
        current = {c: n for c, n in counts.items() if n >= min_count}
        if not current:
            break

        all_frequent.update(current)
        levels[k + 1] = len(current)
        k += 1

    return {
        "min_count": min_count,
        "frequent_itemsets": all_frequent,
        "levels": levels,
        "candidates": candidates_per_level,
    }


def generate_rules(frequent_itemsets, total_transactions):
    """Membentuk rule dengan konsekuen satu item beserta support, confidence, dan lift."""
    rules = []

    for itemset, count in frequent_itemsets.items():
        if len(itemset) < 2:
            continue

        for consequent in itemset:
            antecedent = itemset - {consequent}
            antecedent_count = frequent_itemsets.get(antecedent)
            if not antecedent_count:
                continue

            confidence = count / antecedent_count
            consequent_support = (
                frequent_itemsets[frozenset([consequent])] / total_transactions
            )

            rules.append({
                "antecedent": ", ".join(sorted(antecedent)),
                "consequent": consequent,
                "support": count / total_transactions,
                "confidence": confidence,
                "lift": confidence / consequent_support,
            })

    return pd.DataFrame(
        rules,
        columns=["antecedent", "consequent", "support", "confidence", "lift"],
    )


def run_experiment(transactions, min_support):
    result = ais_algorithm(transactions, min_support)
    rules = generate_rules(result["frequent_itemsets"], len(transactions))

    print(f"\nMinimum Support: {min_support}")
    print(f"Minimum Count: {result['min_count']}")
    print(f"Frequent Itemsets: {result['levels']}")
    print(f"Candidates: {result['candidates']}")

    for threshold in CONFIDENCE_VALUES:
        total = (rules["confidence"] >= threshold).sum()
        print(f"Confidence: {threshold} | Jumlah Rules: {total}")

    if not rules.empty:
        print("\nTop Association Rules:")
        top_rules = rules.sort_values(by="confidence", ascending=False)
        print(top_rules.head(TOP_N_RULES).to_string(index=False))


def main():
    transactions = load_transactions(DATASET_PATH)
    for min_support in SUPPORT_VALUES:
        run_experiment(transactions, min_support)


if __name__ == "__main__":
    main()