[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/akbare12/news-23-b23-front-page-dense/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/akbare12/news-23-b23-front-page-dense/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

# The World Today — Monday 23 November 2026

One image summing up the world's news of Monday 23 November 2026: a dense
front page with 31 stories across 6 regions.

- **Hero trio:** the AI rout hits Asia (Kospi −3.3%), Guterres calls for global
  AI safety rules before it's too late, and the US lead over China falls to a
  record low (Asia Power Index gap 5.3).
- **10 illustrated cards** plus an 18-story "ALSO ON MONDAY" list, a world map
  with 31 numbered pins, and a DATE CHECK box that keeps 22/21/19 November
  stories out of the day's news.
- Scenes are drawn illustrations, not photographs.

## Run

```sh
python3 main.py            # writes entry.png to $MAKEFUN_OUTPUT_DIR (or ./out)
```

`main.py` copies `entry.png` (drawn by `draw.py`, Pillow) to
`$MAKEFUN_OUTPUT_DIR/entry.png` and verifies its dimensions and sha256.
