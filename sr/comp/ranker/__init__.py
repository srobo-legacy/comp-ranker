"""Conversions of game points into league points."""

from __future__ import print_function

from collections import defaultdict

DEFAULT_NUM_ZONES = 4


def calc_positions(zpoints, dsq_list=()):
    """
    Calculate positions from a map of zones to in-game points.

    Parameters
    ----------
    zpoints : dict
        A mapping from some key (typically a zone or corner name) to game
        points (usually a numeric type, but can be any type that is comparable
        and usable as a key for dictionaries).
    dsq_list : list
        If provided, is a :py:class:`list` of keys of teams or zones that have
        been disqualified and are therefore considered below last place.

    Returns
    -------
    dict
        A mapping from positions to an iterable of teams in that position.

    Note
    ----
       In case of a tie, both teams are awarded the same position, as is usual
       in sport. That is, if team A has 3 points, team B has 3 points and team
       C has 1 point, then teams A and B are both awarded 1\ :sup:`st`, and C
       is awarded 3\ :sup:`rd`.

    Examples
    --------
    Some examples of usage are shown below:

    >>> calc_positions({'A': 3, 'B': 3, 'C': 1})
    {1: {'A', 'B'}, 3: {'C'}}

    >>> calc_positions({'A': 3, 'B': 3, 'C': 0, 'D': 0}, ['A', 'C'])
    {1: {'B'}, 2: {'D'}, 3: {'A', 'C'}}
    """

    pos_map = {}
    points_map = defaultdict(set)

    for zone, points in zpoints.items():
        # Wrap the points in a type which also encodes their disqualification
        quaifies_for_points = zone not in dsq_list
        points = (
            quaifies_for_points,
            points if quaifies_for_points else None,
        )
        points_map[points].add(zone)

    position = 1
    for points in sorted(list(points_map.keys()), reverse=True):
        pos_map[position] = points_map[points]
        position += len(points_map[points])

    return pos_map


def _points_for_position(position, winner_points, num_tied):
    """
    Calculate the number of league points for a given position, allowing for
    ties.

    The number of points awarded decreases by two for each position below the
    winner, ties are resolved by sharing the points equally. For example, if a
    tied posiion would normally earn earn 8 points and there is a three-way tie
    for first place, each gets 6pts since (8+6+4)/3.

    While we could loop over the tied positions to share the points out, it's
    faster to just use maths to do it for us.

    Given that the general formula for the points at a given position is:

        (tied_pos_points + (tied_pos_points - 2) + (tied_pos_points - 4) ...)
        ---------------------------------------------------------------------
                                num_tied

    we start by pulling out the tied_pos_points:

        num_tied * tied_pos_points + ((-2) + (-4) ...)
        ----------------------------------------------
                          num_tied

    multiplying the right hand part through by -1 and knowing that the sum from
    1..(n-1) is (n(n-1))/2, we can rewrite that as:

        num_tied * tied_pos_points - num_tied * (num_tied - 1)
        -------------------------------------------------------
                               num_tied

    which obviously simplifies to:

        tied_pos_points - (num_tied - 1)

    which is what we use to calculate the points for given position.
    """

    # pos is 1-indexed, hence the subtraction
    points = winner_points - 2 * (position - 1)

    return points - (num_tied - 1)

def calc_ranked_points(pos_map, dsq_list=(), num_zones=DEFAULT_NUM_ZONES):
    """
    Calculate league points from a mapping of positions to teams.

    The league points algorithm is documented in :ref:`league-points-algorithm`.

    Parameters
    ----------
    pos_map : dict
        A mapping from positions (integers indicating ending position, such as
        1 for 1\ :sup:`st`, 3 for 3\ :sup:`rd` etc) to some iterable of teams
        or zones in that position.
    dsq_list : list
        If provided, is a :py:class:`list` of teams or zones that are
        considered to be disqualified.
    num_zones : int
        The overall number of zones. This is usually the same as the total
        number of zones/team provided in ``pos_map`` (and cannot be less than
        that), though may be more if there were empty zones during some given
        match.

    Returns
    -------
    dict
        A mapping from zones/teams to league points.

    Examples
    --------
    Uniquely placed teams in a four-zone arena would earn 8, 6, 4 and 2 points
    for first through fourth place respectively.

    Three teams tied for first place in a four-zone arena will each earn 6
    points (since this is ``(8+6+4)/3``).

    Some examples of usage are shownn below.

    >>> calc_ranked_points({1: ['A'], 2: ['B'], 3: ['C'], 4: ['D']})
    {'A': 8, 'B': 6, 'C': 4, 'D': 2}

    >>> calc_ranked_points({1: ['A', 'B'], 2: ['C', 'D']})
    Traceback (most recent call last):
        ...
    ValueError: Cannot have position 2 when position 1 is shared by 2 zones

    >>> calc_ranked_points({1: ['A', 'B'], 3: ['C', 'D']})
    {'A': 7, 'B': 7, 'C': 3, 'D': 3}

    >>> calc_ranked_points({1: ['A', 'B']}, num_zones=3)
    {'A': 5, 'B': 5}

    >>> calc_ranked_points({1: ['B'], 2: ['D'], 3: ['A', 'C']}, ['A', 'C'])
    {'A': 0, 'B': 8, 'C': 0, 'D': 6}
    """

    num_teams = sum(len(v) for v in pos_map.values())
    if num_teams > num_zones:
        raise ValueError(
            "More teams given positions ({0}) than zones available ({1})".format(
                num_teams,
                num_zones,
            ),
        )

    rpoints = {}

    winner_points = 2 * num_zones

    for pos, zones in pos_map.items():
        # remove any that are dsqaulified
        # note that we do this before working out the ties, so that any
        # dsq tie members are removed from contention
        zones = [z for z in zones if z not in dsq_list]
        if len(zones) == 0:
            continue

        points = _points_for_position(pos, winner_points, num_tied=len(zones))

        for zone in zones:
            rpoints[zone] = points

        for offset in range(1, len(zones)):
            invalid_pos = pos + offset
            if invalid_pos in pos_map:
                raise ValueError(
                    "Cannot have position {0} when position {1} is shared by "
                    "{2} zones".format(invalid_pos, pos, len(zones)),
                )

    # those that were dsq get 0
    for disqualified_zone in dsq_list:
        rpoints[disqualified_zone] = 0

    return rpoints


def get_ranked_points(zpoints, dsq=(), num_zones=DEFAULT_NUM_ZONES):
    """
    Compute, from a mapping of teams to game points, the teams' league points.

    This is a convenience wrapper around `calc_positions` and
    `calc_rank_points`.

    Examples
    --------
    An example of usage is shown below.

    >>> get_ranked_points({'A': 1, 'B': 3, 'C': 3, 'D': 4}, ['A'])
    {'A': 0, 'B': 5, 'C': 5, 'D': 8}
    """

    pos_map = calc_positions(zpoints, dsq)
    rpoints = calc_ranked_points(pos_map, dsq, num_zones)
    return rpoints


def _demo():
    """Run a quick demo of this module."""

    scores = {'ABC': 12,
              'DEF':  3,
              'ABC2': 4,
              'JLK': 10}

    dsq = []

    print('Original scores:', scores)
    ranked_scores = get_ranked_points(scores, dsq)
    print('Ranked scores:', ranked_scores)

    dsq = ['ABC']

    print("And now disqulifying 'ABC'.")
    ranked_scores = get_ranked_points(scores, dsq)
    print('Ranked scores:', ranked_scores)


if __name__ == '__main__':
    _demo()
