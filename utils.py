from typing import Tuple, Dict, List, Any


def rankings_change(home_rank: float, away_rank: float, home_score: int, away_score: int,
                    is_neutral_venue: bool = False, is_rwc: bool = False) -> Tuple[float, float]:
    """
    THe change in rankings for both teams for a given match result.
    :param home_rank: THe home teams rank points.
    :param away_rank:  THe away teams ranking points.
    :param home_score: THe home teams score.
    :param away_score: THe away teams score.
    :param is_neutral_venue: If the match occurred at a neural venue.
    :param is_rwc: If the match was played at the rugby world cup.
    :return: The updated point for the home team then the away team.
    """
    home_adjusted_rank = home_rank if is_neutral_venue else home_rank + 3
    exchange = points_exchange(home_adjusted_rank - away_rank, home_score - away_score, is_rwc)
    return round(home_rank + exchange, 2), round(away_rank - exchange, 2)


def points_exchange(rank_differences: float, score_difference: int, is_rwc: bool = False) -> float:
    """
    Calculates the point exchanged based on the result of the match.
    :param rank_differences: THe ranking difference of the teams pre match.
    :param score_difference: The difference in match score.
    :param is_rwc: Is a rugby world cup match.
    :return: THe score to be exchanged.
    """
    multiplier = is_rwc + 1
    if score_difference == 0:
        return min(rank_differences * multiplier * 0.1, multiplier)
    if abs(score_difference) < 16:
        return min((10 - rank_differences) * multiplier * 0.1, multiplier * 2)
    else:
        return min((10 - rank_differences) * multiplier * 0.15, multiplier * 3)


def running_rankings(match_results: List[Dict[str, Any]], current_rankings: Dict[str]) -> Dict[str]:
    for m in match_results:
        t1, t2 = m["teams"]
        s1, s2 = m["score"]
        r1, r2 = current_rankings[t1], current_rankings[t2]
        current_rankings[t1], current_rankings[t2] = rankings_change(r1, r2, s1, s2, m["nha"], m["rwc"])
    return current_rankings


def conversion_distance_2d(d: float, p: float = 5.6) -> float:
    """
    Determine the distance at which a conversion is taken.
    :param d: The from the horizontal distance from the try and the nearest post.
    :param p: Width of the posts.
    :return: The vertical distance at which the conversion is taken.
    """
    return (d * (d - p / 2)) ** 0.5

