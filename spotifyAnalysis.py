import pandas as pd
import json
#import os

#This program will provide the data behind the flask API

app_config_file = "config/config.json"
app_config = {}
app_data_path = None
genre_by_country_file = None
spotify_data_file = None
countries_file = None
genre_icons = {
'Hip hop/Rap/R&b': '/static/images/hiphop.png',
'EDM': '/static/images/EDM.png',
'Pop': '/static/images/pop.png',
'Rock/Metal': '/static/images/rock-music.png',
'Latin/Reggaeton': '/static/images/reggae.png',
'Other': '/static/images/othergenres.png',

}

with open(app_config_file,"r") as configobj:
    app_config = json.load(configobj)
    app_data_path = app_config.get("appdataDirectory")
    genre_by_country_file = app_config.get("Genres_by_country_filename")
    spotify_data_file = app_config.get("Spotify_data_filename")
    countries_file = app_config.get("Countries_lat_lng")

#Create a class SpotifyData. On initialization of the class, getGenrebyCountry function gets called which will read the csv file
#into df, convert df to string of json(to_json), and then json.loads converts the string to actual json(list of dictionaries)
#GenrebyCountry will hold the json output
class SpotifyData:
    def __init__(self):
        self.CountriesCoords = self.getCountries()
        self.GenrebyCountry,self.Genres = self.getGenrebyCountry()
        self.YearlySpotifyData = self.getSpotifyData()
        self.Top3Genres = self.getTopNGenresbyCountry()

        self.TopN = 20

    def getGenrebyCountry(self):
        filepath = "{0}/{1}".format(app_data_path,genre_by_country_file)
        df = pd.read_csv(filepath,sep=",")
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

    def getCountries(self):
        filepath = "{0}/{1}".format(app_data_path, countries_file)
        df = pd.read_csv(filepath, sep=",")
        df["ID"] = df["Country"]
        df["ID"] = df["ID"].apply(lambda x:x.lower().replace(" ","_"))
        df.set_index("ID",inplace=True)
        df = df.to_json(orient="index")
        df = json.loads(df)  # returns a json dataset
        return df

    #country look up to fecth coordinates for map
    def getCoordinates(self,country,type):
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
        return genre_icons.get(genre) or '/static/images/othergenres.png'

    def getSpotifyData(self):
        filepath = "{0}/{1}".format(app_data_path, spotify_data_file)
        raw_spotify_data_df = pd.read_csv(filepath, sep=";")
        raw_spotify_data_df["YearlyPopularityRank"] = raw_spotify_data_df.groupby("Year")["Popularity"].rank(ascending=False)
        raw_spotify_data_df["GenreIcon"] = raw_spotify_data_df["Genre"].apply(self.getGenreIcon)
        raw_spotify_json = raw_spotify_data_df.to_json(orient="records")
        raw_spotify_json = json.loads(raw_spotify_json)  # returns a json dataset
        return raw_spotify_json

    def getTopNGenresbyCountry(self):
        filepath = "{0}/{1}".format(app_data_path,genre_by_country_file)
        df = pd.read_csv(filepath,sep=",")

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
            country_data["CountryName"] = country
            country_data = country_data.reset_index()
            country_data.rename(columns={"index":"Genre",country_data_col : "DataValue"},inplace=True)
            all_country_data.append(country_data)

        df_all_countries = pd.concat(all_country_data)
        df_all_countries["GenreIcon"] = df_all_countries["Genre"].apply(self.getGenreIcon)
        df_all_countries["latitude"] = df_all_countries["CountryName"].apply(lambda x: self.getCoordinates(country=x, type="latitude"))
        df_all_countries["longitude"] = df_all_countries["CountryName"].apply(lambda x: self.getCoordinates(country=x, type="longitude"))
        df_all_countries["CountryCode"] = df_all_countries["CountryName"].apply(lambda x: self.getCoordinates(country=x, type="code"))
        top3genres_countries_json = df_all_countries.to_json(orient="records")
        top3genres_countries_json = json.loads(top3genres_countries_json)

        return top3genres_countries_json