
$("canvas[data-year]").each(function(i,data){
    var data_year = $(data).attr("data-year");
    var year_info = Year_metrics[data_year];
    if(year_info)
    {
    var data_labels = year_info["Genre"];
    var data_values = year_info["Songcounts"];

    //creating bar chart using chart.js
    var ctx = $(data);
    new Chart(ctx, {
            type: 'bar',
            data: {
              labels: data_labels,
              datasets: [{
                label: 'Songs by Genre',
                data: data_values,
                borderWidth: 1
              }]
            },
            options: {
             indexAxis: 'y',
            }
          });
    }

});



$("canvas[data-yearinfo]").each(function(i,data){
    var data_year = $(data).attr("data-yearinfo");
    var year_info = Year_song_char[data_year];
    if(year_info)
    {
    var data_labels = Object.keys(year_info);
    var data_values = Object.values(year_info);

    //creating bar chart using chart.js
    var ctx = $(data);
    new Chart(ctx, {
            type: 'doughnut',
            data: {
              labels: data_labels,
              datasets: [{
                label: 'Song characteristics',
                data: data_values

              }]
            }

          });
    }

});

$(".slider").slick({

  // normal options...
  infinite: true,
  autoplay: true,
  slidesToShow: 2,
 dots: true,
  speed: 500

});

var map_markers = {};

var map = L.map('map').setView([36.1408, 5.3536], 1.5);

var Stamenlayer = L.tileLayer('https://stamen-tiles-{s}.a.ssl.fastly.net/toner/{z}/{x}/{y}.{ext}', {
    attribution: 'Map tiles by <a href="http://stamen.com">Stamen Design</a>, <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a> &mdash; Map data &copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
   //subdomains: 'abcd',
   minZoom: 1,
   maxZoom: 2,
   ext: 'png'
});

map.addLayer(Stamenlayer);

$(mapdata).each(function(i,data){
var countryname = data['Country'];
var countrycode = data['CountryCode'];
var popularGenre = data['Most Popular Genre'];
var genreIcon = data['GenreIcon'];
var lat = data['latitude'];
var lng = data['longitude'];
var countryurl = "/static/images/flags/"+countrycode+".png"
console.log(countryurl)

var mapIcon = L.icon({
    iconUrl: genreIcon,
    iconSize: [24, 24]
});

var marker = L.marker([lat, lng], {icon: mapIcon});
marker.addTo(map);
marker.bindTooltip('<p><img style="padding:2px" src='+countryurl+' width="40"  height="30"><b>Country: </b>'+countryname + "</p><hr/><p><b>Popular Genre: </b>"+popularGenre+"</p>");

map_markers[popularGenre] = marker;

})



