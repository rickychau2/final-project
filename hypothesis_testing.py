import pandas as pd
from stats_tests import chisquared_independence_test, two_sample_ttest
from stats_functions import not_on_spotify, with_and_without_spotify, split_by_percentile

SPOTIFY_ATTRIBUTES = ["danceability", "energy", "key", "loudness", "mode", "speechiness",\
    "acousticness", "instrumentalness", "liveness", "valence", "tempo", "type", "id", "uri",\
        "track_href", "analysis_url", "duration_ms", "time_signature"]

all_songs_dfs = {}
for decade in range(1970, 2030, 10):
    filename = "dataset/%ss_dataset"%str(decade)
    all_songs_dfs[decade] = pd.read_csv(filename)
    
print(all_songs_dfs[1970].dtypes)

with_spotify_dfs = {}
without_spotify_dfs = {}
for decade in range(1970, 2030, 10):
    with_spotify_dfs[decade], without_spotify_dfs[decade] = with_and_without_spotify(all_songs_dfs[decade])


### Hypothesis 1: chi-square testing fo all numerical attributes on list songs with spotify data (but targetting dancebility)
def h1():
    for decade in range(1970, 2030, 10):
        print("********************\nThis is %s decade:\n********************"%str(decade))
        for attribute in SPOTIFY_ATTRIBUTES:
            print("This is for " + attribute + ":")
            chisquared_independence_test(with_spotify_dfs[decade], "weeks_on_chart", attribute)
    

### Hypothesis 2: two sample t test to see if average valence is different for songs that are on charts longest
def h2():
    for decade in range(1970, 2030, 10):
        top_percentile, bottom_percentile = split_by_percentile(with_spotify_dfs[decade], 10)
        two_sample_ttest(top_percentile["valence"], bottom_percentile["valence"])


### Hypothesis 3: two sample t test to see if average energy score is different from 1970s to 2010s
def h3():
    two_sample_ttest(with_spotify_dfs[1970]["energy"], with_spotify_dfs[2010]["energy"])

# h1()
# h2()
# h3()

chisquared_independence_test(with_spotify_dfs[decade], "energy", "tempo")