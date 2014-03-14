Ranker
======

[![Build Status](https://travis-ci.org/PeterJCLaw/ranker.png)](https://travis-ci.org/PeterJCLaw/ranker)

Given a collection of entrants and their scores,
 it will sort them and return their ranked points

The mechanism used to alocate the ranked points is (quote taken from the
[Student Robotics](https://www.studentrobotics.org)
[rulebook](https://www.studentrobotics.org/docs/rules)).

> The team with the **most** game points will be awarded 4 points towards the competition league.
> The team with the second most will be awarded 3.
> The team with the third most will be awarded 2 points, and the team with the fewest game points will be awarded 1 point.
> Teams whose robot was not entered into the round, or who were disqualified from the round, will be awarded no points.
>
> Tied robots will be awarded the average of the points that their combined positions would be awarded.
> Thus, three robots tied for first place would receive 3 points each (since this is `(4+3+2)/3`).

As a result, the ranked points for an entrant (team) might not be an integer.
However, for 4 entrants the value will always be a multiple of 0.5.
