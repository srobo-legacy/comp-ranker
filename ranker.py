
def calc_positions(zpoints, dsq_list):
    """
    A function to work out the placings of zones in a game, given the game points.
    @param zpoints: a dict of zone number to game points.
    @param dsq_list: a list of zones that should be considered below last.
    @returns: a dict of position to array of zone numbers.
    """

    pos_map = {}
    points_map = {}

    for z, p in zpoints.items():
        if z in dsq_list:
            p = -1
        if p not in points_map:
            points_map[p] = set()
        points_map[p].add(z)

    i = 1
    for p in sorted(list(points_map.keys()), reverse = True):
        pos_map[i] = points_map[p]
        i += len(points_map[p])

    return pos_map

def calc_ranked_points(pos_map, dsq_list):
    """
    A function to work out the ranked points for each zone, given the rankings within that game.
    @param pos_map: a dict of position to array of zone numbers.
    @param dsq_list: a list of zones that shouldn't be awarded ranked points.
    @returns: a dict of zone number to rank points.
    """

    rpoints = {}

    for pos, zones in pos_map.items():
        # remove any that are dsqaulified
        # note that we do this before working out the ties, so that any
        # dsq tie members are removed from contention
        zones = [z for z in zones if z not in dsq_list]
        if len(zones) == 0:
            continue

        # max points is 8, decreases by two for subsequent positions. pos is
        # 1-indexed, hence the subtraction
        points = 8 - 2*(pos - 1)
        # Now that we have the value for this position if it were not a tie,
        # we need to allow for ties. In case of a tie, the available points
        # for all the places used are shared by all those thus placed.
        # Eg: three first places get 6pts each (8+6+4)/3.
        # Rather than generate a list and average it, it's quicker to just
        # do some maths using the max value and the length of the list
        points = points - (len(zones) - 1)
        for z in zones:
            rpoints[z] = points

    # those that were dsq get 0
    for z in dsq_list:
        rpoints[z] = 0

    return rpoints

def get_ranked_points(zpoints, dsq):
    """
    A function to work out the rank points for each zone, given the game points.
    This is a thin convenience wrapper around `calc_positions` and `calc_rank_points`.
    @param zpoints: a dict of zone number to game points.
    @param dsq: a list of zones that shouldn't be awarded ranked points.
    @returns: a dict of zone number to rank points.
    """
    pos_map = calc_positions(zpoints, dsq)
    rpoints = calc_ranked_points(pos_map, dsq)
    return rpoints

if __name__ == '__main__':
    """Demo"""
    scores = { 'ABC' : 12,
               'DEF' : 3,
               'ABC2' : 4,
               'JLK' : 10 }

    dsq = []

    print('Original scores:', scores)
    ranked_scores = get_ranked_points(scores, dsq)
    print('Ranked scores:', ranked_scores)

    dsq = ['ABC']

    print("And now disqulifying 'ABC'.")
    ranked_scores = get_ranked_points(scores, dsq)
    print('Ranked scores:', ranked_scores)
