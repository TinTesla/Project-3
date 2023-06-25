// Function to fetch JSON data
async function fetchData() {
  try {
    const response = await fetch("https://raw.githubusercontent.com/TinTesla/Project-3/main/Clean/json%20copies/cleaned_spotify_data.json");
    const data = await response.json();
    return data;
  } catch (error) {
    console.error("Error fetching data:", error);
  }
}

// Function to populate the drop-down menu with unique genres
function populateGenreDropdown(data) {
  const dropdown = document.getElementById("genre");
  const genres = [...new Set(data.map(entry => entry.Genre))];
  genres.forEach(genre => {
    const option = document.createElement("option");
    option.value = genre;
    option.text = genre;
    dropdown.appendChild(option);
  });
}

// Function to create the bubble chart
function createBubbleChart(data, selectedGenre) {
  const filteredData = selectedGenre ? data.filter(entry => entry.Genre === selectedGenre) : data;

  const bubbleData = [{
    x: filteredData.map(entry => entry.Bpm),
    y: filteredData.map(entry => entry.Valence),
    text: filteredData.map(entry => entry.Title),
    mode: "markers",
    marker: {
      size: filteredData.map(entry => entry["Duration (in seconds)"] / 10),
      color: filteredData.map(entry => getYearColor(entry.Year)),
      colorscale: "Rainbow"
    }
  }];

  const bubbleLayout = {
    xaxis: { title: "Bpm" },
    yaxis: { title: "Valence" }
  };

  Plotly.newPlot("bubble", bubbleData, bubbleLayout);
}

// Function to get color based on year
function getYearColor(year) {
  if (year <= 1999) {
    return "red";
  } else if (2000 <= year && year <= 2004) {
    return "orange";
  } else if (2005 <= year && year <= 2009) {
    return "yellow";
  } else if (2010 <= year && year <= 2014) {
    return "green";
  } else if (2015 <= year && year <= 2019) {
    return "blue";
  } else if (year >= 2020) {
    return "purple";
  } else {
    return "black";
  }
}

// Function to fetch JSON data for choropleth map
async function fetchCountryData() {
  try {
    const response = await fetch("https://raw.githubusercontent.com/TinTesla/Project-3/main/Clean/json%20copies/cleaned_country_data.json");
    const countryData = await response.json();
    return countryData;
  } catch (error) {
    console.error("Error fetching country data:", error);
  }
}

// Function to create the choropleth map
function createChoroplethMap(countryData, selectedGenre) {
  const countryNames = countryData.map(entry => entry.Country);
  const genreValues = countryData.map(entry => entry[selectedGenre]);

  const defaultColor = "grey";
  const defaultZ = 0;

  const choroplethData = [{
    type: "choropleth",
    locations: countryNames,
    z: genreValues,
    locationmode: "country names",
    colorscale: getGenreColorScale(selectedGenre),
    zmin: 0,
    zmax: getMaxValue(countryData, selectedGenre),
    // Set default color and value for missing countries
    marker: {
      line: {
        color: defaultColor
      }
    },
    zhoverformat: ".2f"
  }];

  // Find missing countries and set default values
  const missingCountries = getAllCountries().filter(country => !countryNames.includes(country));
  missingCountries.forEach(country => {
    choroplethData[0].locations.push(country);
    choroplethData[0].z.push(defaultZ);
  });

  const choroplethLayout = {
    title: selectedGenre,
    geo: {
      showframe: false,
      showcoastlines: false,
      projection: {
        type: "natural earth",
      },
    },
  };

  Plotly.newPlot("choropleth", choroplethData, choroplethLayout);
}

// Function to get all countries
function getAllCountries() {
  return Object.keys(countryData);
}

// Function to get the maximum value for a selected genre
function getMaxValue(data, genre) {
  return Math.max(...data.map(entry => entry[genre]));
}

// Function to get the colorscale for a selected genre
function getGenreColorScale(genre) {
  switch (genre) {
    case "Hip hop/Rap/R&b":
      return "Reds";
    case "EDM":
      return "Oranges";
    case "Pop":
      return "Yellows";
    case "Rock/Metal":
      return "Greens";
    case "Latin/Reggaeton":
      return "Blues";
    case "Other":
      return "Purples";
    default:
      return "Greys";
  }
}

// Update all the plots when a new genre is selected
function updateGraph() {
  const selectedGenre = document.getElementById("genre").value;
  createBubbleChart(data, selectedGenre);
  createChoroplethMap(countryData, selectedGenre);
}

// Fetch data and initialize the graph and map
let data;
let countryData;
Promise.all([fetchData(), fetchCountryData()])
  .then(results => {
    data = results[0];
    countryData = results[1];
    populateGenreDropdown(data);
    createBubbleChart(data, null);
    createChoroplethMap(countryData, null);
  })
  .catch(error => console.error("Error:", error));
