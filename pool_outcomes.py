from itertools import product, chain
from match_data import remaining_matches, matches_in_pool
import math

SCORE_OUTCOMES = {
    # Bonus point win with bonus loss variations
    (5, 2), (5, 1), (5, 0), (2, 5), (1, 5), (0, 5),

    # Win with bonus loss variations
    (4, 2), (4, 1), (4, 0), (2, 4), (1, 4), (0, 4),

    # Draws with bonus variations
    (3, 2), (2, 3), (2, 2)
}

POOL_A = {"JAPAN": 14, "IRELAND": 11, "SAMOA": 5, "RUSSIA": 0, "SCOTLAND": 10}
POOL_B = {"NEW ZEALAND": 12, "SOUTH AFRICA": 15, "ITALY": 10, "CANADA": 0, "NAMIBIA": 0}
POOL_C = {"ENGLAND": 17, "FRANCE": 14, "ARGENTINA": 11, "TONGA": 1, "UNITED STATES": 0}
POOL_D = {"WALES": 14, "AUSTRALIA": 11, "FIJI": 7, "URUGUAY": 4, "GEORGIA": 5}

pool_a_matches = matches_in_pool(remaining_matches(), "A")
pool_b_matches = matches_in_pool(remaining_matches(), "B")
pool_c_matches = matches_in_pool(remaining_matches(), "C")
pool_d_matches = matches_in_pool(remaining_matches(), "D")


def pool_score_outcomes(current_pool, matches, match_outcomes=SCORE_OUTCOMES):
    outcomes = [current_pool]
    for t1, t2 in matches:
        t1, t2 = t1.upper(), t2.upper()
        new_outcomes = {}
        for o, (p1, p2) in product(outcomes, match_outcomes):
            o = o.copy()
            o[t1] += p1
            o[t2] += p2
            new_outcomes[hash(tuple(o.items()))] = o
        outcomes = list(new_outcomes.values())
    return outcomes


def agg_pool_outcomes(outcomes, transform_totals=None, position_till=-1):
    ranks_dicts = {t: 0 for t in outcomes[0]}
    for o in outcomes:
        for t, s in sorted(o.items(), key=lambda x: x[1], reverse=True)[0:position_till]:
            ranks_dicts[t] += s

    if transform_totals is not None:
        ranks_dicts = {t: transform_totals(s) for t, s in ranks_dicts.items()}
    results = sorted(ranks_dicts.items(), key=lambda x: x[1], reverse=True)
    return results


def max_min_pool_outcomes(outcomes):
    ranks_dicts = {t: [float("inf"), 0] for t in outcomes[0]}
    for o in outcomes:
        for t, s in sorted(o.items(), key=lambda x: x[1], reverse=True):
            if s < ranks_dicts[t][0]:
                ranks_dicts[t][0] = s
            if s > ranks_dicts[t][1]:
                ranks_dicts[t][1] = s
    results = sorted(ranks_dicts.items(), key=lambda x: x[1][::-1], reverse=True)
    return results


def pprint_pool_outcomes(outcomes):
    row_format = " | ".join("{:15} {:>8}" for _ in range(5))
    rank_row = row_format.format(*["1st", "", "2nd", "", "3rd", "", "4th", "", "5th", ""])
    table_format = "\n".join(["Outcome: {}", rank_row, row_format, "\n"])
    for i, o in enumerate(outcomes):
        results = sorted(o.items(), key=lambda x: x[1], reverse=True)
        print(table_format.format(i, *list(chain.from_iterable(results))))


def pprint_results_across(pools_results):
    row_format = " | ".join("{:15} {:>8}" for _ in range(5))
    rank_row = row_format.format(*["1st", "", "2nd", "", "3rd", "", "4th", "", "5th", ""])
    table_format = "\n".join(["{}", rank_row, "-" * len(rank_row), row_format, "\n"])
    for p, result in pools_results.items():
        print(table_format.format(p, *list(str(i) for i in chain.from_iterable(result))))


def pprint_results_down(pools_results):
    row_format = "{:5}| " + " | ".join("{:15} {:>8}" for _ in range(4))
    headers_rows = row_format.format("", *[j for i in zip(pools_results.keys(), [""] * 4) for j in i])
    print(headers_rows)
    print("-" * len(headers_rows))
    for i, r in enumerate(["1st", "2nd", "3rd", "4th", "5th"]):
        print(row_format.format(r, *[str(j) for v in pools_results.values() for j in v[i]]))


func_str = "agg_pool_outcomes(pool_score_outcomes(POOL_{}, pool_{}_matches))"
# eval(func_str.format(i, i.lower()))
pools_results = {"Pool {}".format(i): sorted(eval("POOL_{}".format(i)).items(), key=lambda x: x[1], reverse=True) for i in "ABCD"}
pprint_results_down(pools_results)



