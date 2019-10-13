import math


def rankings_change(home_rank, away_rank, home_score, away_score, is_neutral_venue=False, is_rwc=False):
    home_adjusted_rank = home_rank if is_neutral_venue else home_rank + 3
    exchange = points_exchange(home_adjusted_rank - away_rank, home_score - away_score, is_rwc)
    return round(home_rank + exchange, 2), round(away_rank - exchange, 2)


def points_exchange(rank_differences, score_difference, is_rwc=False):
    multiplier = is_rwc + 1
    if score_difference == 0:
        return min(rank_differences * multiplier * 0.1, multiplier)
    if abs(score_difference) < 16:
        return min((10 - rank_differences) * multiplier * 0.1, multiplier * 2)
    else:
        return min((10 - rank_differences) * multiplier * 0.15, multiplier * 3)


def running_rankings(match_results, current_rankings):
    for m in match_results:
        t1, t2 = m["teams"]
        s1, s2 = m["score"]
        r1, r2 = current_rankings[t1], current_rankings[t2]

        r1, r2 = rankings_change(r1, r2, s1, s2, m["nha"], m["rwc"])

        current_rankings[t1] = r1
        current_rankings[t2] = t2
    return current_rankings


def conversion_distance_2d(d, p=5.6):
    """

    :param d:The from the horizontal distance from the try and the nearest post.
    :param p: width of the posts
    :return:
    """
    return (d * (d - p / 2)) ** 0.5

import matplotlib.pyplot as plt
import numpy as np


x = np.arange(0, 50, 0.1)
y = conversion_distance_2d(x)

plt.plot(x, y)
plt.show()

