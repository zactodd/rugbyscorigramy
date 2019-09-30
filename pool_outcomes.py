from itertools import product
from match_data import remaining_matches, matches_teams

SCORE_OUTCOMES = {
    # Bonus point win with bonus loss variations
    (5, 2), (5, 1), (5, 0), (2, 5), (1, 5), (0, 5),

    # Win with bonus loss variations
    (4, 2), (4, 1), (4, 0), (2, 4), (1, 4), (0, 4),

    # Draws with bonus variations
    (3, 2), (2, 3), (2, 2)
}

POOL_A = {"JAPAN": 9, "IRELAND": 6, "SAMOA": 5, "RUSSIA": 0, "SCOTLAND": 0}
pool_a_matches = matches_teams(remaining_matches(), "A")


def pool_score_outcomes(current_pool, matches, match_outcomes=SCORE_OUTCOMES):
    pools_outcomes = {t: {s} for t, s in current_pool.items()}
    for t1, t2 in matches:
        t1, t2 = t1.upper(), t2.upper()
        pools_outcomes[t1] = {s + o[0] for s, o in product(pools_outcomes[t1], match_outcomes)}
        pools_outcomes[t2] = {s + o[1] for s, o in product(pools_outcomes[t2], match_outcomes)}
    return pools_outcomes

