from itertools import product, chain
from match_data import remaining_matches, matches_teams
import math

SCORE_OUTCOMES = {
    # Bonus point win with bonus loss variations
    (5, 2), (5, 1), (5, 0), (2, 5), (1, 5), (0, 5),

    # Win with bonus loss variations
    (4, 2), (4, 1), (4, 0), (2, 4), (1, 4), (0, 4),

    # Draws with bonus variations
    (3, 2), (2, 3), (2, 2)
}

POOL_A = {"JAPAN": 9, "IRELAND": 6, "SAMOA": 5, "RUSSIA": 0, "SCOTLAND": 5}
POOL_B = {"NEW ZEALAND": 4, "SOUTH AFRICA": 5, "ITALY": 10, "CANADA": 0, "NAMIBIA": 0}
POOL_C = {"ENGLAND": 10, "FRANCE": 4, "ARGENTINA": 6, "TONGA": 0, "UNITED STATES": 0}
POOL_D = {"WALES": 9, "AUSTRALIA": 6, "FIJI": 2, "URUGUAY": 4, "GEORGIA": 5}

pool_a_matches = matches_teams(remaining_matches(), "A")
pool_b_matches = matches_teams(remaining_matches(), "B")
pool_c_matches = matches_teams(remaining_matches(), "C")
pool_d_matches = matches_teams(remaining_matches(), "D")


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


def pprint_pool_outcomes(outcomes):
    row_format = " | ".join("{:15} {:3}" for _ in range(5))
    rank_row = row_format.format(*["1st", "", "2nd", "", "3rd", "", "4th", "", "5th", ""])
    table_format = "\n".join(["Outcome: {}", rank_row, row_format, "\n"])
    for i, o in enumerate(outcomes):
        results = sorted(o.items(), key=lambda x: x[1], reverse=True)
        print(table_format.format(i, *list(chain.from_iterable(results))))


def agg_pool_outcomes(outcomes, transform_totals=None):
    row_format = " | ".join("{:15} {:8}" for _ in range(5))
    rank_row = row_format.format(*["1st", "", "2nd", "", "3rd", "", "4th", "", "5th", ""])
    table_format = "\n".join([rank_row, row_format, "\n"])
    ranks_dicts = {t: 0 for t in outcomes[0]}
    for o in outcomes:
        for t, s in sorted(o.items(), key=lambda x: x[1], reverse=True):
            ranks_dicts[t] += s

    if transform_totals is not None:
        ranks_dicts = {t: transform_totals(s) for t, s in ranks_dicts.items()}
    results = sorted(ranks_dicts.items(), key=lambda x: x[1], reverse=True)
    print(table_format.format(*list(chain.from_iterable(results))))


for i in "ABCD":
    print("POOL: ", i)
    trans = "lambda x: round(math.log(x), 4)"
    exec("agg_pool_outcomes(pool_score_outcomes(POOL_{}, pool_{}_matches), {})".format(i, i.lower(), trans))
