import pandas as pd
from flask import Flask,render_template
import json
import spotifyAnalysis

app_config_file = "config/config.json"
app_config = {}
app_port = None

Spotify_Data = spotifyAnalysis.SpotifyData()

with open(app_config_file,"r") as configobj:
    app_config = json.load(configobj)
    app_port = app_config.get("app_port")


app = Flask(__name__)
@app.route('/')
def welcome():
    """
    #Welcome page shows the main default Dashboard hosting the following in a sliding slick carousel format:
    #Top 20 songs from 2000-2023 alongside 2 graphs: bar graph showing count of songs in the top 20 per genre,
    #doughnut chart showing characteristics distribution of those top 20 songs
    :return:
    - index.html
    """
    #dt = Spotify_Data.getArtistdata(artist_id='4524518717075603732')
    genredata = Spotify_Data.GenrebyCountry
    genres = Spotify_Data.Genres
    TopGenres = Spotify_Data.TopGenres
    UniqueGenres = Spotify_Data.UniqueGenres
    CountriesbyGenre = Spotify_Data.CountriesbyGenre

    headers =['Country','Most Popular Genre','latitude','longitude']
    top20Songs = Spotify_Data.YearlySpotifyData

    top20Songs_df = pd.DataFrame(top20Songs)


    spotify_top20_by_year = top20Songs_df[top20Songs_df["YearlyPopularityRank"] <= 20]
    Year_bin = spotify_top20_by_year[["Year", "Title", "Artist","Genre", "Popularity","GenreIcon","Bpm","Energy","Danceability",
                                      "Db","Liveness","Valence","Duration","Acousticness","Speechiness","Artist_ID"]]
    # second bar chart in carousel - which song characteristics that contributed to the popularity in that year
    Year_song_char = pd.DataFrame(Year_bin.groupby("Year").sum())
    #comment
    Year_song_char.drop(columns=["Title","Artist","Genre","GenreIcon","Popularity","Duration","Artist_ID"],inplace=True)


    Year_song_char = Year_song_char.to_json(orient="index")
    Year_song_char = json.loads(Year_song_char)

    Year_bin["Song"] = Year_bin.apply(lambda x: dict(Title=x.get("Title"),
                                                     Artist=x.get("Artist"),
                                                     Artist_ID = x.get("Artist_ID"),
                                                     Genre=x.get("Genre"),
                                                     GenreIcon = x.get("GenreIcon"),
                                                     Popularity=x.get("Popularity"),
                                                     Bpm=x.get("Bpm"),
                                                     Energy=x.get("Energy"),
                                                     Danceability=x.get("Danceability"),
                                                     Db=x.get("Db"),
                                                     Liveness=x.get("Liveness"),
                                                     Valence=x.get("Valence"),
                                                     Duration=x.get("Duration"),
                                                     Acousticness=x.get("Acousticness"),
                                                     Speechiness=x.get("Speechiness")),axis=1)

    # with year as index - for javascript - popular songs bar chart
    Year_bin_genres = pd.DataFrame(Year_bin.groupby(["Year","Genre"])["Title"].count()).reset_index()
    Year_bin_labels= pd.DataFrame(Year_bin_genres.groupby("Year")["Genre"].apply(list))
    Year_bin_values = pd.DataFrame(Year_bin_genres.groupby("Year")["Title"].apply(list))
    Year_metrics = pd.merge(Year_bin_values,Year_bin_labels,how="inner",left_index=True,right_index=True)
    Year_metrics.rename(columns={"Title":"Songcounts"},inplace=True)
    Year_metrics = Year_metrics.to_json(orient="index")
    Year_metrics = json.loads(Year_metrics)

    # with year as column - for carousel list in html
    Year_bin_lookup = Year_bin.groupby("Year")["Song"].apply(list)
    Year_bin = pd.DataFrame(Year_bin_lookup).reset_index()
    Year_bin = Year_bin.to_json(orient="records")
    Year_bin = json.loads(Year_bin)

    return render_template("index.html",headers=headers,tableData=genredata, Year_bin=Year_bin,Year_metrics=Year_metrics,
                           Year_song_char=Year_song_char,genres=genres,TopGenres=TopGenres,
                           UniqueGenres = UniqueGenres, CountriesbyGenre=CountriesbyGenre)


@app.route('/Timeline')
def showTimeline():
    """
    #Timeline route gets triggered on View Timeline button click
    #Show interactive timeline bar chart of average popularity over the years
    #On click of Back to Dashboard button takes to the main page
    :return:
    - timeline.html
    """
    return render_template("timeline.html")


@app.route('/timelineseries')
def showTimelineSeries():
    """
    # '/timelineseries' is called from timeline.html
    #returns static htmls created from plotly_express in jupyter
    :return:
    - timelineseries.html
    """
    return render_template("timelineseries.html")


@app.route('/Songs')
def showSongs():
    """
    #Songs route gets triggered on click of Songs 2000-2023 button
    #Shows the following in jstree format:
    #List of songs appearing in top charts over multiple years
    #Artists having their songs appearing in top charts over multiple years
    #Artists appearing more than once in a Year and the list of those songs
    #On click of Back to Dashboard button takes to the main page
    :return:
    - songs.html
    """
    Songs_by_year = Spotify_Data.Songs_by_year
    Spotify_top_songs = Spotify_Data.Spotify_top_songs
    Songs = Spotify_Data.Songs
    Year_by_artists = Spotify_Data.Year_by_artists

    df = pd.DataFrame(Songs_by_year)
    titles = list(df["Song_Title"])
    nYears = list(df["Number of Years"])
    df_songs = pd.DataFrame(Spotify_top_songs)
    df_songs["Metrics"] = df_songs.apply(lambda x:dict(Year=x.get("Year"),Popularity=x.get("Popularity")),axis=1)
    df_songs["Artist_metrics"] = df_songs.apply(lambda x:dict(Song=x.get("Title"),Genre=x.get("Genre"),Year=x.get("Year"),
                                                              Genreicon=x.get("GenreIcon"),Popularity=x.get("Popularity")),axis=1)
    df_artists = pd.DataFrame(df_songs.groupby("Artist")["Artist_metrics"].apply(list)).reset_index()
    df_artists = df_artists.to_json(orient="records")
    Spotify_top_artists = json.loads(df_artists)


    df_songs = pd.DataFrame(df_songs.groupby(["Song_Title","Artist","Genre","GenreIcon"])["Metrics"].apply(list)).reset_index()
    df_songs = df_songs.to_json(orient="records")
    Spotify_top_songs = json.loads(df_songs)



    return render_template("songs.html",Songs_by_year=Songs_by_year,titles=titles,nYears=nYears,
                           Spotify_top_songs=Spotify_top_songs,Spotify_top_artists=Spotify_top_artists,Year_by_artists=Year_by_artists)


@app.route('/Year/<year>')
def getYearlycharacteristics(year):
    """
    #Year route lists all the individual year data for all characteristics vs popularity scatter plots and regression analysis.
    #Each button links to indvidual years.
    #On click of Back to Dashboard button takes to the main page
    :param year:
    :return:
    - characteristics.html
    """
    yearly_data = Spotify_Data.getSongCharacteristics(year=year)

    yearly_data = yearly_data[0]

    popularity = yearly_data.get("Popularity")
    bpm = yearly_data.get("Bpm")
    energy = yearly_data.get("Energy")
    danceability = yearly_data.get("Danceability")
    liveness = yearly_data.get("Liveness")
    valence = yearly_data.get("Valence")
    duration = yearly_data.get("Duration")
    acousticness = yearly_data.get("Acousticness")
    speechiness = yearly_data.get("Speechiness")

    bpm_popularity = [[bpm[popularity.index(x)], x] for x in popularity]
    energy_popularity = [[energy[popularity.index(x)], x] for x in popularity]
    dance_popularity = [[danceability[popularity.index(x)], x] for x in popularity]
    live_popularity = [[liveness[popularity.index(x)], x] for x in popularity]
    valence_popularity = [[valence[popularity.index(x)], x] for x in popularity]
    duration_popularity = [[duration[popularity.index(x)], x] for x in popularity]
    acoust_popularity = [[acousticness[popularity.index(x)], x] for x in popularity]
    speech_popularity = [[speechiness[popularity.index(x)], x] for x in popularity]

    yearly_characteristics_data = {"bpm":bpm_popularity,
                                 "energy": energy_popularity,
                                 "danceability": dance_popularity,
                                 "liveness": live_popularity,
                                 "valence": valence_popularity,
                                 "duration": duration_popularity,
                                 "acousticness": acoust_popularity,
                                 "speechiness": speech_popularity,
                                 "year": year
                                 }


    return render_template("characteristics.html",yearly_characteristics_data=yearly_characteristics_data,year=year)


@app.route('/Artist/<artist_id>')
def getArtiststats(artist_id):
    """
    #On click of any artist on the top 20 songs list on slick caraousel - Artist route gets triggered which based on Artist ID
    #  opens up a page showing Artist specific details: Popular songs, the years they appeared in the charts, popularity and
    #characteristics of all those songs in a radar chart represenation
    #On click of Back to Dashboard button takes to the main page
    :param artist_id:
    :return:
    - artist.html
    """

    artist_stats = Spotify_Data.getArtistdata(artist_id=artist_id)

    return render_template("artist.html",artist_stats=artist_stats)


@app.route('/songcharvstime')
def showSongCharvsTimeWrapper():
    """
    #On click of the Song Characteristics over Time button triggers the wrapper html characteristicsvstime.html
    #which shows two graphs: 1) Songs Characteristics vs Year and 2) Song Characteristics Timeline
    #On click of Back to Dashboard button takes to the main page
    :return:
    - characteristicsvstime
    """
    return render_template("characteristicsvstime.html")


@app.route('/songcharvstime1')
def showSongCharvsTime():
    """
    #/songcharvstime returns static htmls created from plotly_express in jupyter
    :return:
    - spotify_characteristics_over_time.html
    """
    return render_template("spotify_characteristics_over_time.html")

@app.route('/chartimelineseries')
def showSongCharTimeline():
    """
    #/songcharvstime returns static htmls created from plotly_express in jupyter
    :return:
    - trends_over_time.html
    """
    return render_template("trends_over_time.html")




if __name__ == '__main__':
   app.run(port=app_port)