def not_on_spotify(complete_df):
    '''
    Description: finds how many songs are not on Spotify in given df
    Inputs: a Dataframe of songs with and without Spotify attributes
    Returns: a tuple of (number songs not on Spotify, total songs, percentage not on Spotify)
    '''
    # checks if danceability attribute is null or not
    missing_spotify_df = complete_df[complete_df.danceability.isnull()]
    return missing_spotify_df.shape[0], complete_df.shape[0], (missing_spotify_df.shape[0] / complete_df.shape[0])

def with_and_without_spotify(complete_df):
    '''
    Description: makes two dataset - one containing the songs with Spotify attributes, one without
    Inputs: a Dataframe of songs with and without Spotify attributes
    Returns: a tuple of (Dataframe of songs with Spotify attributes, Dataframe without)
    '''
    # checks if danceability attribute is null or not
    missing_spotify_df = complete_df[complete_df.danceability.isnull()]
    with_spotify_df = complete_df[complete_df.danceability.notnull()]
    return with_spotify_df, missing_spotify_df

def __obtain_weeks_on_chart_values(song_df):
    '''
    Description: creates distinct list of weeks_on_chart values
    Inputs: a Dataframe containing song and billboard data
    Returns: a distinct Dataframe of weeks_on_chart values for the given Dataframe
    '''
    weeks_on_chart_col = song_df[["weeks_on_chart"]]
    # may have to check if values in column are not null
    weeks_on_chart_values = weeks_on_chart_col.drop_duplicates()
    weeks_on_chart_values = weeks_on_chart_values.sort_values(by=["weeks_on_chart"], ascending=False)
    return weeks_on_chart_values

def weeks_on_chart_count(song_df):
    '''
    Description: prints table that counts how many songs have been on for each number of weeks
    Inputs: a Dataframe containing song and billboard data
    Returns: a Datagrame containing the counts how many songs appear on the billboard for each number of weeks
    '''
    weeks_on_chart_values = __obtain_weeks_on_chart_values(song_df)
    weeks_on_chart_count = [0] * weeks_on_chart_values.shape[0]
    weeks_on_chart_counter = 0
    for index, row in weeks_on_chart_values.iterrows():
        weeks_on_chart_value = row["weeks_on_chart"]
        value_count = song_df[song_df.weeks_on_chart == weeks_on_chart_value].shape[0]
        weeks_on_chart_count[weeks_on_chart_counter] += int(value_count)
        weeks_on_chart_counter += 1
    weeks_on_chart_values["count"] = weeks_on_chart_count
    return weeks_on_chart_values
    
    
def __get_percentile(weeks_on_chart_values, percentile):
    '''
    Description: gets the weeks_on_chart cutoff for a given percentile
    Inputs: a Dataframe containing weeks_on_chart values and song counts, a Double representing the percentile cutoff
    Returns: an Integer representing the weeks_on_chart cutoff
    '''
    num_of_songs = weeks_on_chart_values["count"].sum()
    exact_cutoff = num_of_songs * (percentile / 100)
    approx_cutoff = 0
    for index, row in weeks_on_chart_values.iterrows():
        exact_cutoff -= row["count"]
        if exact_cutoff < 0:
            break
        approx_cutoff = row["weeks_on_chart"]
    return approx_cutoff

def split_by_percentile(song_df, percentile):
    '''
    Description: splits the given song_df into two Dataframes - one for the top percentile, one for the bottom
    Inputs: a Dataframe of songs, an Integer representing the percentile cutoff
    Returns: a Dataframe representing the top percentile of songs, a Dataframe representing the bottom percentile of songs
    '''
    weeks_on_chart_count_table = weeks_on_chart_count(song_df)
    count_cutoff = __get_percentile(weeks_on_chart_count_table, percentile)
    top_percentile = song_df[song_df.weeks_on_chart > count_cutoff]
    bottom_percentile = song_df[song_df.weeks_on_chart <= count_cutoff]
    return top_percentile, bottom_percentile

