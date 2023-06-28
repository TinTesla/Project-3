CREATE TABLE spotify_data(
	Title varchar NOT NULL,
	Artist varchar NOT NULL,
	Genre varchar(30),
	Year INT,
	Bpm INT,
	Energy INT,
	Danceability INT,
	dB INT,
	Liveliness INT,
	Valence INT,
	Duration INT,
	Acousticness INT,
	Speechiness INT,
	Spotify_Rating INT,
	CONSTRAINT SD_data PRIMARY KEY (Title,Artist,Year)
);

CREATE TABLE countries(
	Country_code VARCHAR(3) NOT NULL,
	Country varchar(50) NOT NULL PRIMARY KEY,
	Latitude float,
	Longitude float
);

CREATE TABLE country_genres(
	Country varchar(50) NOT NULL PRIMARY KEY,
	HipHop_Rap_RB INT,
	EDM INT,
	Pop INT,
	Rock_Metal INT,
	Latin_Reggaeton INT,
	Other INT, 
	MostPopularGenre varchar(20) NOT NULL,
	FOREIGN KEY(Country) references countries(Country)
);