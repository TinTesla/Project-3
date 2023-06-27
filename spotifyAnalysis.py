import pandas as pd
import json
import sqlite3
#import os

#This program will provide the data behind the flask API

app_config_file = "config/config.json"
app_config = {}
app_data_path = None
genre_by_country_file = None
spotify_data_file = None
countries_file = None

genre_icons = {
'Hip hop/Rap/R&b': 'https://img.icons8.com/color-glass/24/hip-hop-music--v2.png',
'EDM': 'https://img.icons8.com/arcade/24/electronic-music.png',
'Pop': 'https://img.icons8.com/arcade/24/musical-stories.png',
'Rock/Metal': 'https://img.icons8.com/3d-fluency/24/rock-music.png',
'Latin/Reggaeton': 'https://img.icons8.com/external-flaticons-flat-flat-icons/24/external-reggae-music-festival-flaticons-flat-flat-icons.png',
'Other': 'https://img.icons8.com/color/24/international-music.png',

}

with open(app_config_file,"r") as configobj:
    app_config = json.load(configobj)
    app_data_path = app_config.get("appdataDirectory")
    genre_by_country_file = app_config.get("Genres_by_country_filename")
    spotify_data_file = app_config.get("Spotify_data_filename")
    countries_file = app_config.get("Countries_lat_lng")

    db_path = app_config.get("db_path")
    db_filename = app_config.get("db_filename")
    db_filename = "{0}/{1}".format(db_path, db_filename)

conn = sqlite3.connect(db_filename,check_same_thread=False)

#Create a class SpotifyData. On initialization of the class, each required function gets called which will read the csv file
#into df, convert df to string of json(to_json), and then json.loads converts the string to actual json output(list of dictionaries)

#declaring the class for web.py
class SpotifyData:
    def __init__(self):
        self.CountriesCoords = self.getCountries_db()
        self.GenrebyCountry,self.Genres = self.getGenrebyCountry_db()
        self.YearlySpotifyData = self.getSpotifyData_DB()
        self.Top3Genres,self.TopGenres,self.UniqueGenres,self.CountriesbyGenre = self.getTopNGenresbyCountry_db()
        self.Songs_by_year,self.Spotify_top_songs,self.Songs,self.Year_by_artists = self.getSongsMultipleOccurences_db()


        #self.TopN = 20
    #function to get data from the genres by country dataset- to feed into the map
    #fetches the country coordinates from the countries file(getCountries function) and returns unique genres list
    #along with their icons



    def getGenrebyCountry_db(self):
        """
        - Fetches all Genre data from the country_genres_data table in spotify_db
        - Merges the country coordinates from countries table: getCountries_db
        :return:
        - unique genres list
        - genres data json
        """
        query = 'Select Country,"Hip hop/Rap/R&b",EDM,Pop,"Rock/Metal","Latin/Reggaeton",Other,"Most Popular Genre" from country_genres_data;'
        df = pd.read_sql(query,con=conn)
        df["GenreIcon"] = df["Most Popular Genre"].apply(self.getGenreIcon)
        df["latitude"] = df["Country"].apply(lambda x:self.getCoordinates(country=x,type="latitude"))
        df["longitude"] = df["Country"].apply(lambda x: self.getCoordinates(country=x, type="longitude"))
        df["CountryCode"] = df["Country"].apply(lambda x: self.getCoordinates(country=x, type="code"))
        unique_genres_df = df[["Most Popular Genre","GenreIcon"]].drop_duplicates()
        unique_genres_df = unique_genres_df.to_json(orient="records")
        unique_genres_df = json.loads(unique_genres_df)
        df = df.to_json(orient="records")
        df = json.loads(df) #returns a json dataset
        return df,unique_genres_df


    def getCountries_db(self):
        """
          - Fetches all countries data from the countries table in spotify_db

          :return:
          - countries dictionary
          """
        query = "Select CountryCode,Country,Latitude,Longitude from countries;"
        df = pd.read_sql(query,con=conn)
        df["ID"] = df["Country"]
        df.set_index("ID",inplace=True)
        df = df.to_json(orient="index")
        df = json.loads(df)  # returns a json dataset
        return df

    #country look up to fecth coordinates for map
    def getCoordinates(self,country,type):
        """
           - Returns latitude or longitude of a country based on the type parameter

           :return:
           - if type is latitude returns latitude
           - if type is longitude returns longitude
           - if type is code returns country code
           """
        return_data = ""
        if type == "latitude":
            country_data = self.CountriesCoords.get(country)
            if country_data:
                return_data=country_data.get("Latitude")
        if type == "longitude":
            country_data = self.CountriesCoords.get(country)
            if country_data:
                return_data=country_data.get("Longitude")
        if type == "code":
            country_data = self.CountriesCoords.get(country)
            if country_data:
                return_data=country_data.get("CountryCode")
        return return_data

    def getGenreIcon(self,genre):
        """
             - Returns the icon based on genre

             :return:
             - icon url
        """
        return genre_icons.get(genre) or 'https://img.icons8.com/color/24/international-music.png'



    def getSpotifyData_DB(self):
        """
                - function to read the Spotify dataset having yearly data of songs and artists since year 2000
                - database table name:spotify_data

                :return:
                - spotify data json
           """
        query = "Select Title,Artist,Genre,Year,Bpm,Energy,Danceability,Db,Liveness,Valence,Duration,Acousticness,Speechiness,Popularity,Artist_ID from spotify_data" \
                " where Year >= 2000;"
        raw_spotify_data_df = pd.read_sql(query,con=conn)
        raw_spotify_data_df["YearlyPopularityRank"] = raw_spotify_data_df.groupby("Year")["Popularity"].rank(ascending=False)
        raw_spotify_data_df["GenreIcon"] = raw_spotify_data_df["Genre"].apply(self.getGenreIcon)
        raw_spotify_json = raw_spotify_data_df.to_json(orient="records")
        raw_spotify_json = json.loads(raw_spotify_json)  # returns a json dataset
        return raw_spotify_json

    def setRank(self,rankvalue):
        """
                - sets the popularity rank text based on the popularity rank value
                - this sets the value for the drop down for map plot

                :return:
                - rank text
           """
        ranktext = ""
        if rankvalue == 1:
            ranktext = "Most Popular"
        if rankvalue == 2:
            ranktext = "Second Most Popular"
        if rankvalue == 3:
            ranktext = "Third Most Popular"
        return ranktext

    def getTopNGenresbyCountry_db(self):
        """
                - Returns top 3 popular genres by country
                :return:
                - topGenres,unique_genres,CountriesbyGenre json
           """
        query = 'Select Country,"Hip hop/Rap/R&b",EDM,Pop,"Rock/Metal","Latin/Reggaeton",Other,"Most Popular Genre" from country_genres_data;'
        df = pd.read_sql(query, con=conn)

        df = df.T
        countries = list(df.loc["Country"])

        all_country_data = []
        for country in countries:
            country_index = countries.index(country)
            country_data = df[country_index]

            cols=list(genre_icons.keys())

            country_data = pd.DataFrame(country_data.loc[cols])


            country_data_col = list(country_data.columns)[0]

            country_data["GenreRank"] = country_data[country_data_col].rank(ascending=False)
            country_data = country_data[country_data["GenreRank"] <= 3] #Top 3 genre
            country_data["Ranktext"] = country_data["GenreRank"].apply(self.setRank)
            country_data["CountryName"] = country
            country_data = country_data.reset_index()
            country_data.rename(columns={"index":"Genre",country_data_col : "DataValue"},inplace=True)
            all_country_data.append(country_data)

        df_all_countries = pd.concat(all_country_data)
        df_all_countries["GenreIcon"] = df_all_countries["Genre"].apply(self.getGenreIcon)
        df_unique_genres = df_all_countries[["Genre","GenreIcon"]].drop_duplicates()
        df_all_countries["latitude"] = df_all_countries["CountryName"].apply(lambda x: self.getCoordinates(country=x, type="latitude"))
        df_all_countries["longitude"] = df_all_countries["CountryName"].apply(lambda x: self.getCoordinates(country=x, type="longitude"))
        df_all_countries["CountryCode"] = df_all_countries["CountryName"].apply(lambda x: self.getCoordinates(country=x, type="code"))
        df_all_countries["Location"] = df_all_countries.apply(lambda x:{"lat":x["latitude"],
                                                                        "lng":x["longitude"],
                                                                        "countrycode":x["CountryCode"],
                                                                        "country": x["CountryName"],
                                                                        "countryiconURL":"/static/images/flags/"+x["CountryCode"]+".png",
                                                                        "genre":x["Genre"],
                                                                        "genreIcon": x["GenreIcon"]
                                                                        },axis=1)


        topGenres = pd.DataFrame(df_all_countries.groupby(["GenreRank","Ranktext"])["Location"].apply(list)).reset_index()

        CountriesbyGenre = pd.DataFrame(df_all_countries.groupby(["Genre"])["CountryName"].apply(list))


        unique_genres = df_unique_genres.to_json(orient="records")
        unique_genres = json.loads(unique_genres)
        topGenres = topGenres.to_json(orient="records")
        topGenres = json.loads(topGenres)
        CountriesbyGenre = CountriesbyGenre.to_json(orient="index")
        CountriesbyGenre = json.loads(CountriesbyGenre)

        #to be replaced
        top3genres_countries_json = df_all_countries.to_json(orient="records")
        top3genres_countries_json = json.loads(top3genres_countries_json)


        return top3genres_countries_json,topGenres,unique_genres,CountriesbyGenre


    def setSongTitle(self,row):
        return "{0} By {1}".format(row['Title'],row['Artist'])


    #Song appearances in the charts more than a year
    def getSongsMultipleOccurences_db(self):
        """
                 - Returns songs appearing in the top charts over multiple years
                 :return:
                 - songs_by_year,spotify_top_songs,songs,year_by_artists json
            """
        query = "Select Title,Artist,Genre,Year,Bpm,Energy,Danceability,Db,Liveness,Valence,Duration,Acousticness," \
                "Speechiness,Popularity,Artist_ID from spotify_data where Year >= 2000;"

        spotify_data_df = pd.read_sql(query,con=conn)
        spotify_data_df["GenreIcon"] = spotify_data_df["Genre"].apply(self.getGenreIcon)
        spotify_data_df["Song_Title"] = spotify_data_df.apply(lambda x:self.setSongTitle(row=x),axis=1)

        artists_songs_cnt = pd.DataFrame(spotify_data_df.groupby(["Year","Artist","Artist_ID"])["Title"].count())

        #filtering out the artists who have at least 2 songs
        artists_songs_cnt = artists_songs_cnt[artists_songs_cnt["Title"] > 1]
        spotify_data_df["Artist_details"] = spotify_data_df.apply(lambda x:dict(Title=x.get("Title"),Genre=x.get("Genre"),GenreIcon=x.get("GenreIcon")),axis=1)

        artists_songs = pd.DataFrame(spotify_data_df.groupby(["Year","Artist","Artist_ID"])["Artist_details"].apply(list))

        #joining 2 dataframes to get the artists details
        artists_songs = pd.merge(artists_songs,artists_songs_cnt,how="inner",left_index=True,right_index=True).reset_index()


        unique_years = list(artists_songs["Year"].drop_duplicates())
        year_by_artists = []

        for yr in unique_years:
            df_year = artists_songs[artists_songs["Year"] == yr]
            if len(df_year) > 0:
                df_year = df_year.to_json(orient="records")
                df_year = json.loads(df_year)
                year_data = {"Year": yr, "Data": df_year}
                year_by_artists.append(year_data)

        songs_by_year = pd.DataFrame(spotify_data_df.groupby("Song_Title")["Year"].nunique())
        songs_by_year = songs_by_year[songs_by_year["Year"] > 1]
        songs_by_year = songs_by_year.reset_index()

        songs = list(songs_by_year["Song_Title"].drop_duplicates())

        spotify_top_songs = spotify_data_df[spotify_data_df["Song_Title"].isin(songs)]
        songs_by_year.sort_values("Year", ascending=False, inplace=True)
        songs_by_year.rename(columns={"Year": "Number of Years"}, inplace=True)

        songs_by_year = songs_by_year.to_json(orient="records")
        songs_by_year = json.loads(songs_by_year)

        spotify_top_songs = spotify_top_songs.to_json(orient="records")
        spotify_top_songs = json.loads(spotify_top_songs)

        artists_songs = artists_songs.to_json(orient="records")
        artists_songs = json.loads(artists_songs)

        return songs_by_year,spotify_top_songs,songs,year_by_artists

    def getSongCharacteristics(self,year):
        """
                    - Returns songs characteristics vs Popularity for each year
                    :return:
                    - yearly_df json
               """

        query = "Select Title,Artist,Genre,Year,Bpm,Energy,Danceability,Db,Liveness,Valence,Duration,Acousticness," \
                "Speechiness,Popularity,Artist_ID from spotify_data where Year = {0};".format(year)

        spotify_df = pd.read_sql(query,con=conn)

        yearly_df_popularity = spotify_df.groupby("Year")["Popularity"].apply(list)
        yearly_df_bpm = spotify_df.groupby("Year")["Bpm"].apply(list)
        yearly_df_energy = spotify_df.groupby("Year")["Energy"].apply(list)
        yearly_df_dance = spotify_df.groupby("Year")["Danceability"].apply(list)
        yearly_df_live = spotify_df.groupby("Year")["Liveness"].apply(list)
        yearly_df_valence = spotify_df.groupby("Year")["Valence"].apply(list)
        yearly_df_duration = spotify_df.groupby("Year")["Duration"].apply(list)
        yearly_df_acoustic = spotify_df.groupby("Year")["Acousticness"].apply(list)
        yearly_df_speech = spotify_df.groupby("Year")["Speechiness"].apply(list)

        yearly_df = pd.merge(yearly_df_popularity,yearly_df_bpm,how='inner',left_index=True,right_index=True)
        yearly_df = pd.merge(yearly_df, yearly_df_energy, how='inner', left_index=True, right_index=True)
        yearly_df = pd.merge(yearly_df, yearly_df_dance, how='inner', left_index=True, right_index=True)
        yearly_df = pd.merge(yearly_df, yearly_df_live, how='inner', left_index=True, right_index=True)
        yearly_df = pd.merge(yearly_df, yearly_df_valence, how='inner', left_index=True, right_index=True)
        yearly_df = pd.merge(yearly_df, yearly_df_duration, how='inner', left_index=True, right_index=True)
        yearly_df = pd.merge(yearly_df, yearly_df_acoustic, how='inner', left_index=True, right_index=True)
        yearly_df = pd.merge(yearly_df, yearly_df_speech, how='inner', left_index=True, right_index=True)

        yearly_df = yearly_df.reset_index()

        yearly_df = yearly_df.to_json(orient="records")
        yearly_df = json.loads(yearly_df)

        return yearly_df

    #artists-their songs and characteristics across all years
    def getArtistdata(self,artist_id):
        """
                    - Query the Spotify database and return songs and their characteristics for a specific artist
                    :return:
                    - artist_data json
               """


        query = "Select Title,Artist,Genre,Year,Bpm,Energy,Danceability,Db,Liveness,Valence,Duration,Acousticness," \
                "Speechiness,Popularity,Artist_ID from spotify_data where Artist_ID = '{0}';".format(artist_id)

        artist_df = pd.read_sql(query, con=conn)
        artist_df["GenreIcon"] = artist_df["Genre"].apply(self.getGenreIcon)

        artist_stats_df = artist_df[["Title","Bpm","Energy","Danceability","Db","Liveness","Valence","Duration","Acousticness","Speechiness"]].drop_duplicates()

        #setting the values for the chart.js
        labels= ["Bpm","Energy","Danceability","Db","Liveness","Valence","Duration","Acousticness","Speechiness"]

        titles = list(artist_df["Title"])

        datasets = artist_df[["Bpm","Energy","Danceability","Db","Liveness","Valence","Duration","Acousticness","Speechiness"]]

        datasets = datasets.values.tolist()

        graph_datasets = []

        for title in titles:
            title_index = titles.index(title)
            title_dataset = datasets[title_index]
            obj = {"label":title,"data":title_dataset}
            graph_datasets.append(obj)

        graph_data = {"labels":labels,"datasets":graph_datasets}
        artist = list(artist_df["Artist"])[0]

        artist_details = artist_df.to_json(orient="records")
        artist_details = json.loads(artist_details)

        artist_data = {"Artist_Name": artist,"Details":artist_details,"Graph_data":graph_data}

        return artist_data







