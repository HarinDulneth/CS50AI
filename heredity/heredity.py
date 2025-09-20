import csv
import itertools
import sys

PROBS = {
    # Unconditional probabilities for having gene
    "gene": {2: 0.01, 1: 0.03, 0: 0.96},
    "trait": {
        # Probability of trait given two copies of gene
        2: {True: 0.65, False: 0.35},
        # Probability of trait given one copy of gene
        1: {True: 0.56, False: 0.44},
        # Probability of trait given no gene
        0: {True: 0.01, False: 0.99},
    },
    # Mutation probability
    "mutation": 0.01,
}


def main():
    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {"gene": {2: 0, 1: 0, 0: 0}, "trait": {True: 0, False: 0}}
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):
        # Check if current set of people violates known information
        fails_evidence = any(
            (
                people[person]["trait"] is not None
                and people[person]["trait"] != (person in have_trait)
            )
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):
                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (
                    True
                    if row["trait"] == "1"
                    else False
                    if row["trait"] == "0"
                    else None
                ),
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s)
        for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def pass_prob(gene_count):
    """
    Probability a parent with `gene_count` copies passes the gene.
    """
    MUTATION = PROBS["mutation"]
    if gene_count == 0:
        return MUTATION
    elif gene_count == 1:
        return 0.5
    else:  # gene_count == 2
        return 1 - MUTATION


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    joint_probes = {
        person: {"gene": None, "trait": None, "p": None} for person in people
    }
    joint_prob = 1.0

    for key in joint_probes:
        if key in one_gene:
            joint_probes[key]["gene"] = 1
        elif key in two_genes:
            joint_probes[key]["gene"] = 2
        else:
            joint_probes[key]["gene"] = 0

        joint_probes[key]["trait"] = key in have_trait

    for key in joint_probes:
        gene = joint_probes[key]["gene"]
        trait = joint_probes[key]["trait"]
        mother = people[key]["mother"]
        father = people[key]["father"]

        if mother is None and father is None:
            p_gene = PROBS["gene"][gene]
        else:
            mom_pass = pass_prob(joint_probes[mother]["gene"])
            dad_pass = pass_prob(joint_probes[father]["gene"])
            if gene == 0:
                p_gene = (1 - mom_pass) * (1 - dad_pass)
            elif gene == 1:
                p_gene = mom_pass * (1 - dad_pass) + (1 - mom_pass) * dad_pass
            else:
                p_gene = mom_pass * dad_pass

        joint_probes[key]["p"] = p_gene * PROBS["trait"][gene][trait]
        joint_prob *= joint_probes[key]["p"]

    return joint_prob


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    for key in probabilities:
        if key in one_gene:
            probabilities[key]["gene"][1] += p
        elif key in two_genes:
            probabilities[key]["gene"][2] += p
        else:
            probabilities[key]["gene"][0] += p

        if key in have_trait:
            probabilities[key]["trait"][True] += p
        else:
            probabilities[key]["trait"][False] += p


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    for key in probabilities:
        gene_count = sum(probabilities[key]["gene"].values())
        trait_count = sum(probabilities[key]["trait"].values())
        for gene in probabilities[key]["gene"]:
            probabilities[key]["gene"][gene] /= gene_count
        for trait in probabilities[key]["trait"]:
            probabilities[key]["trait"][trait] /= trait_count


if __name__ == "__main__":
    main()
