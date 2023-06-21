import pandas as pd
from flask import Flask,render_template, jsonify
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
    genredata = Spotify_Data.GenrebyCountry
    genres = Spotify_Data.Genres
    Top3Genres = Spotify_Data.Top3Genres

    headers =['Country','Most Popular Genre','latitude','longitude']
    top20Songs = Spotify_Data.YearlySpotifyData
    top20Songs_df = pd.DataFrame(top20Songs)
    top20Songs_df = top20Songs_df[top20Songs_df["Year"] >= 2000]

    spotify_top20_by_year = top20Songs_df[top20Songs_df["YearlyPopularityRank"] <= 20]
    Year_bin = spotify_top20_by_year[["Year", "Title", "Artist", "Genre", "Popularity","GenreIcon","Bpm","Energy","Danceability",
                                      "Db","Liveness","Valence","Duration","Acousticness","Speechiness"]]
    # second bar chart in carousel - which song characteristics that contributed to the popularity in that year
    Year_song_char = pd.DataFrame(Year_bin.groupby("Year").sum())

    Year_song_char.drop(columns=["Title","Artist","Genre","GenreIcon","Popularity","Duration"],inplace=True)


    Year_song_char = Year_song_char.to_json(orient="index")
    Year_song_char = json.loads(Year_song_char)

    Year_bin["Song"] = Year_bin.apply(lambda x: dict(Title=x.get("Title"),
                                                     Artist=x.get("Artist"),
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
                           Year_song_char=Year_song_char,genres=genres)

if __name__ == '__main__':
   app.run(port=app_port)