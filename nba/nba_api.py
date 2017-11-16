"""Wrappers for `nba_py` constructors

Functions in this module wraps constructors of interest from `nba_py` with a
rate limiter to throttle requests from the NBA API. The goal is to be nice to
the NBA and prevent suspicion.

We wrap the constructors because all API requests made by `nba_py` classes are
done in the constructor. Class methods only decode the fetched data.

CAVEAT: `nba_py` sometimes caches calls via `requests-cache`, so not all
constructors need throttling. This simple solution throttles everything
regardless if it actually calls stats.nba.com over HTTP.

This module is kind of ugly, but it works. There must be a better way, but I
haven't found it yet.

"""

from retrying import retry
from ratelimiting import RateLimiting

from nba_py import Scoreboard
# from nba_py import league
from nba_py import game
# from nba_py import player


RETRY_ATTEMPTS = 5
RETRY_DELAY = 500
MAX_CALLS_PER_INTERVAL = 5
INTERVAL_IN_SECONDS = 2.0

@retry(stop_max_attempt_number=RETRY_ATTEMPTS, wait_fixed=RETRY_DELAY)
@RateLimiting(max_calls=MAX_CALLS_PER_INTERVAL, period=INTERVAL_IN_SECONDS)
def scoreboard(year, month, day):
    return Scoreboard(year=year, month=month, day=day)


@retry(stop_max_attempt_number=RETRY_ATTEMPTS, wait_fixed=RETRY_DELAY)
@RateLimiting(max_calls=MAX_CALLS_PER_INTERVAL, period=INTERVAL_IN_SECONDS)
def boxscore_summary(game_id, start_period, end_period, start_range,
                     end_range, range_type):
    return game.BoxscoreSummary(game_id, start_period=start_period,
                                end_period=end_period, start_range=start_range,
                                end_range=end_range, range_type=range_type)


@retry(stop_max_attempt_number=RETRY_ATTEMPTS, wait_fixed=RETRY_DELAY)
@RateLimiting(max_calls=MAX_CALLS_PER_INTERVAL, period=INTERVAL_IN_SECONDS)
def boxscore_traditional(game_id, start_period, end_period, start_range,
                         end_range, range_type):
    return game.Boxscore(game_id, start_period=start_period,
                         end_period=end_period, start_range=start_range,
                         end_range=end_range, range_type=range_type)


@retry(stop_max_attempt_number=RETRY_ATTEMPTS, wait_fixed=RETRY_DELAY)
@RateLimiting(max_calls=MAX_CALLS_PER_INTERVAL, period=INTERVAL_IN_SECONDS)
def boxscore_scoring(game_id, start_period, end_period, start_range,
                     end_range, range_type):
    return game.BoxscoreScoring(game_id, start_period=start_period,
                                end_period=end_period, start_range=start_range,
                                end_range=end_range, range_type=range_type)


@retry(stop_max_attempt_number=RETRY_ATTEMPTS, wait_fixed=RETRY_DELAY)
@RateLimiting(max_calls=MAX_CALLS_PER_INTERVAL, period=INTERVAL_IN_SECONDS)
def boxscore_misc(game_id, start_period, end_period, start_range,
                  end_range, range_type):
    return game.BoxscoreMisc(game_id, start_period=start_period,
                             end_period=end_period, start_range=start_range,
                             end_range=end_range, range_type=range_type)


@retry(stop_max_attempt_number=RETRY_ATTEMPTS, wait_fixed=RETRY_DELAY)
@RateLimiting(max_calls=MAX_CALLS_PER_INTERVAL, period=INTERVAL_IN_SECONDS)
def boxscore_advanced(game_id, start_period, end_period, start_range,
                      end_range, range_type):
    return game.BoxscoreAdvanced(game_id, start_period=start_period,
                                 end_period=end_period, start_range=start_range,
                                 end_range=end_range, range_type=range_type)


@retry(stop_max_attempt_number=RETRY_ATTEMPTS, wait_fixed=RETRY_DELAY)
@RateLimiting(max_calls=MAX_CALLS_PER_INTERVAL, period=INTERVAL_IN_SECONDS)
def boxscore_four_factors(game_id, start_period, end_period, start_range,
                          end_range, range_type):
    return game.BoxscoreFourFactors(game_id, start_period=start_period,
                                    end_period=end_period, start_range=start_range,
                                    end_range=end_range, range_type=range_type)


@retry(stop_max_attempt_number=RETRY_ATTEMPTS, wait_fixed=RETRY_DELAY)
@RateLimiting(max_calls=MAX_CALLS_PER_INTERVAL, period=INTERVAL_IN_SECONDS)
def boxscore_usage(game_id, start_period, end_period, start_range,
                   end_range, range_type):
    return game.BoxscoreUsage(game_id, start_period=start_period,
                              end_period=end_period, start_range=start_range,
                              end_range=end_range, range_type=range_type)


@retry(stop_max_attempt_number=RETRY_ATTEMPTS, wait_fixed=RETRY_DELAY)
@RateLimiting(max_calls=MAX_CALLS_PER_INTERVAL, period=INTERVAL_IN_SECONDS)
def boxscore_player_tracking(game_id):
    return game.PlayerTracking(game_id)


@retry(stop_max_attempt_number=RETRY_ATTEMPTS, wait_fixed=RETRY_DELAY)
@RateLimiting(max_calls=MAX_CALLS_PER_INTERVAL, period=INTERVAL_IN_SECONDS)
def boxscore_hustle(game_id):
    return game.HustleStats(game_id)
