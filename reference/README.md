# Reference implementations

`rugby-rwc-2027/` is a git submodule of https://github.com/JustusVermaakSkystrm/rugby-rwc-2027
(Elo + Monte Carlo RWC 2027 simulator), pinned at `d6592db`. Use it to cross-check our bracket,
tiebreak and third-place logic (see `rugby/simulator.py`: `rank_pool`, `rank_thirds`, `allocate_thirds`,
and `rugby/data/bracket.json`), or as a starting point for a dynamic pool-prediction simulator.

Fetch it with `git submodule update --init`. Known differences from our rules: it ranks best thirds with
try difference (World Rugby's published order does not), and allocates thirds by constraints only
(ambiguous when pools E and F both qualify) rather than the official 15-row table we use.
