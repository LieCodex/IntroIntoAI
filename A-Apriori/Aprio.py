from itertools import combinations
import argparse
from pathlib import Path

def load_transactions(filename):
    transactions = []
    with open(filename, "r") as f:
        for line in f:
            items = line.strip().split()
            transactions.append(set(items))
    return transactions


def get_support(transactions, itemset):
    count = 0
    for t in transactions:
        if itemset.issubset(t):
            count += 1
    return count / len(transactions)


def generate_candidates(prev_frequent, k):
    candidates = set()
    prev_list = list(prev_frequent)

    for i in range(len(prev_list)):
        for j in range(i + 1, len(prev_list)):
            union = prev_list[i] | prev_list[j]
            if len(union) == k:
                candidates.add(frozenset(union))

    return candidates


def apriori(transactions, min_support=0.2):

    items = set()
    for t in transactions:
        items |= t

    frequent = {}
    current = set()

    # L1
    for item in items:
        itemset = frozenset([item])
        support = get_support(transactions, itemset)

        if support >= min_support:
            current.add(itemset)
            frequent[itemset] = support

    k = 2

    while current:

        candidates = generate_candidates(current, k)
        next_level = set()

        for c in candidates:
            support = get_support(transactions, c)

            if support >= min_support:
                next_level.add(c)
                frequent[c] = support

        current = next_level
        k += 1

    return frequent


def generate_rules(frequent_itemsets, min_confidence=0.6):

    rules = []

    for itemset in frequent_itemsets:

        if len(itemset) < 2:
            continue

        for i in range(1, len(itemset)):

            for antecedent in combinations(itemset, i):

                antecedent = frozenset(antecedent)
                consequent = itemset - antecedent

                confidence = frequent_itemsets[itemset] / frequent_itemsets[antecedent]

                if confidence >= min_confidence:

                    rules.append((antecedent, consequent, confidence))

    return rules


def _format_itemset(itemset):
    return "{" + ", ".join(sorted(itemset)) + "}"


def main():
    parser = argparse.ArgumentParser(description="Run Apriori and print frequent itemsets/rules.")
    parser.add_argument(
        "dataset",
        nargs="?",
        default="gaming_transactions.txt",
        help="Path to transaction dataset (default: gaming_transactions.txt)",
    )
    parser.add_argument(
        "--min-support",
        type=float,
        default=0.2,
        help="Minimum support threshold in [0, 1] (default: 0.2)",
    )
    parser.add_argument(
        "--min-confidence",
        type=float,
        default=0.6,
        help="Minimum confidence threshold in [0, 1] (default: 0.6)",
    )
    args = parser.parse_args()

    dataset_path = Path(args.dataset)
    if not dataset_path.is_absolute():
        dataset_path = Path(__file__).resolve().parent / dataset_path

    if not dataset_path.exists():
        raise FileNotFoundError(f"Dataset not found: {dataset_path}")

    transactions = load_transactions(dataset_path)
    frequent_itemsets = apriori(transactions, min_support=args.min_support)
    rules = generate_rules(frequent_itemsets, min_confidence=args.min_confidence)

    print(f"Dataset: {dataset_path.name}")
    print(f"Transactions: {len(transactions)}")
    print(f"Min support: {args.min_support}")
    print(f"Min confidence: {args.min_confidence}")
    print()

    print("Frequent itemsets:")
    for itemset, support in sorted(
        frequent_itemsets.items(), key=lambda x: (len(x[0]), sorted(x[0]), -x[1])
    ):
        print(f"  {_format_itemset(itemset)} -> support={support:.3f}")

    print()
    print("Association rules:")
    if not rules:
        print("  (none above confidence threshold)")
    else:
        for antecedent, consequent, confidence in sorted(
            rules, key=lambda x: (len(x[0]), sorted(x[0]), sorted(x[1]), -x[2])
        ):
            print(
                f"  {_format_itemset(antecedent)} => {_format_itemset(consequent)} "
                f"(confidence={confidence:.3f})"
            )


if __name__ == "__main__":
    main()