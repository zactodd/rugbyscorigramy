
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
