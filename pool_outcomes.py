from itertools import product

SCORE_OUTCOMES = {
    # Bonus point win with bonus loss variations
    (5, 2), (5, 1), (5, 0), (2, 5), (1, 5), (0, 5),

    # Win with bonus loss variations
    (4, 2), (4, 1), (4, 0), (2, 4), (1, 4), (0, 4),

    # Draws with bonus variations
    (3, 2), (2, 3), (2, 2)
}


def pool_score_outcomes(current_pool, matches, match_outcomes=SCORE_OUTCOMES):
    pools_outcomes = {t: {s} for t, s in current_pool.items()}
    for t1, t2 in matches:
        pools_outcomes[t1] = {s + o for s, o in product(pools_outcomes[t1], match_outcomes)}
        pools_outcomes[t2] = {s + o for s, o in product(pools_outcomes[t2], match_outcomes)}
    return pools_outcomes
