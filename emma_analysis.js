// Initializes the page with a default plot
function init() {
    data = [{
    //   label: "Top 15 Artists that Have More than One Song that Stayed on the Charts for More than One Year"  
      x: ["Rihanna","Justin Bieber","Ed Sheeran","OneRepublic","Taio Cruz","Taylor Swift","Selena Gomez & The Scene","Jonas Blue","One Direction","Flo Rida","Eminem","Swedish House Mafia","The Chainsmokers","Maroon 5","Trey Songz"],
      y: [5,4,3,3,3,3,2,2,2,2,2,2,2,2,2],
      type: "bar"
     }];

    layout = {
        xaxis:{
            title: "Artist"
        },
        yaxis:{
            title: "Number of Songs/Times"
        }
    }
  
    Plotly.newPlot("plot",data,layout);
  }
  
  // Call updatePlotly() when a change takes place to the DOM
  d3.selectAll("#selDataset").on("change", updatePlotly);
  
  // This function is called when a dropdown menu item is selected
  function updatePlotly() {
    // Use D3 to select the dropdown menu
    let dropdownMenu = d3.select("#selDataset");
    // Assign the value of the dropdown menu option to a variable
    let dataset = dropdownMenu.property("value");
  
    // Initialize x and y arrays
    let x = [];
    let y = [];
  
    if (dataset === 'dataset1') {
        x = ["Rihanna","Justin Bieber","Ed Sheeran","OneRepublic","Taio Cruz","Taylor Swift","Selena Gomez & The Scene","Jonas Blue","One Direction","Flo Rida","Eminem","Swedish House Mafia","The Chainsmokers","Maroon 5","Trey Songz"];
        y = [5,4,3,3,3,3,2,2,2,2,2,2,2,2,2];
    }
  
    else if (dataset === 'dataset2') {
      x = ["Rihanna","Drake","Taylor Swift","Eminem","Calvin Harris","Ariana Grande","David Guetta","Ed Sheeran","Kanye West","Justin Bieber","Beyoncé","Usher","Coldplay","Chris Brown","Maroon 5","Black Eyed Peas","Britney Spears","Jason Derulo","Katy Perry","Bruno Mars","The Weeknd","Bad Bunny","Justin Timberlake","Flo Rida","JAY-Z","P!nk","Nelly","Post Malone","Adele","Alicia Keys","Selena Gomez","Enrique Iglesias","Jennifer Lopez","OneRepublic","Ludacris","One Direction","Miley Cyrus","Pitbull","Lady Gaga","Dua Lipa"];
      y = [30,28,23,22,22,20,19,19,19,18,18,17,17,17,17,17,15,14,14,14,14,13,13,12,12,12,12,12,11,11,10,10,10,10,10,10,10,10,10,10];
    }
  
    // Note the extra brackets around 'x' and 'y'
    Plotly.restyle("plot", "x", [x]);
    Plotly.restyle("plot", "y", [y]);
  }
  
  init();
  
  
