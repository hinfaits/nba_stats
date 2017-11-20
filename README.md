[![Build Status](https://travis-ci.org/hinfaits/nba_stats.svg?branch=develop)](https://travis-ci.org/hinfaits/nba_stats)

# nba_scraper

Gather data from stats.nba.com into analyzable formats

## Dependencies (important)
Use a recent version of [nba_py](https://github.com/seemethere/nba_py). The version as of writing (17-Nov-17) on PyPi is out of date. In other words, `pip install -r requirements.txt` will cause errors. You can install all requirements from `requirements.txt`, then upgrade the found version of nba_py from a current source.

Clone nba_py and install via `pip install --upgrade /path/to/nba_py`. Commit `ffeaf4251d796ff9313367a752a45a0d7b16489e` is verified compatible. Or use:
```
$ pip install --upgrade git+git://github.com/seemethere/nba_py.git@ffeaf4251d796ff9313367a752a45a0d7b16489e
```
