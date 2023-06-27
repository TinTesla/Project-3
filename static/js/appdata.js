//var genresbyrank = {};
//var genresbylocation = {};
//var country_markers = {};
var marker_array = [];


//create basemaps
var Stamenlayer = L.tileLayer('https://stamen-tiles-{s}.a.ssl.fastly.net/toner/{z}/{x}/{y}.{ext}', {
    attribution: 'Map tiles by <a href="http://stamen.com">Stamen Design</a>, <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a> &mdash; Map data &copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
   //subdomains: 'abcd',
   minZoom: 1,
   maxZoom: 3,
   ext: 'png'
});
var map = L.map('map').setView([36.1408, 5.3536], 2);
map.addLayer(Stamenlayer);

//canvas - slider - Top 20 songs - See chart.js
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
                label: 'Number of Songs by Genre',
                data: data_values,
                borderWidth: 1,
                backgroundColor:"red"
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

//var map_markers = {};


//for select button - By Genre popularity - Stamen map
function explorebyGenrePopularity(target_genre)
{
    let selected_val = $('#genreselector').val();
    $('a[data-genre]').hide();
    $(marker_array).each(function(j,mrk){
    map.removeLayer(mrk);
    });
    $(TopGenres).each(function(i,data)
    {
        var genrerank = data['GenreRank'];
        var ranktext = data["Ranktext"];
        var ranklocation = data["Location"];
        if(ranktext==selected_val){
            $(ranklocation).each(function(j,locationdata){
                var lat = locationdata["lat"];
                //lat = lat + j;
                var lng = locationdata["lng"];
                var countryiconurl = locationdata["countryiconURL"];
                var countryname = locationdata["country"]
                var genre = locationdata["genre"];
                if(target_genre){
                    if(target_genre==genre){
                        var genreicon = locationdata["genreIcon"]
                        var iconsize = [30,30];

                        var mapIcon = L.icon({
                            iconUrl: genreicon,
                            iconSize: iconsize//size of the icon
                        });

                        var marker = L.marker([lat, lng], {icon: mapIcon});
                        marker.bindTooltip('<p><img style="padding:2px" src='+countryiconurl+' width="40"  height="30"><b>Country: </b>'+countryname + "</p><hr/><p><b> Genre: </b>"+genre+"</p>");
                        map.addLayer(marker)

                        marker_array.push(marker);
                         $('a[data-genre="'+genre+'"]').show();
                    }

                }
                else{
                    var genreicon = locationdata["genreIcon"]
                    var iconsize = [30,30];

                    var mapIcon = L.icon({
                        iconUrl: genreicon,
                        iconSize: iconsize//size of the icon
                    });

                    var marker = L.marker([lat, lng], {icon: mapIcon});
                    marker.bindTooltip('<p><img style="padding:2px" src='+countryiconurl+' width="40"  height="30"><b>Country: </b>'+countryname + "</p><hr/><p><b> Genre: </b>"+genre+"</p>");
                    map.addLayer(marker)

                    marker_array.push(marker);
                    $('a[data-genre="'+genre+'"]').show();

                }

            })

        }


    })

}

function showMarkersByGenre(genre_val){
   explorebyGenrePopularity(target_genre=genre_val);

}
//function call for map
explorebyGenrePopularity(target_genre=null);

//on-click event handling for all buttons for the map
$("a.genrelink").on("click",function(){
    let selected_genre = $(this).attr("data-genre");
    showMarkersByGenre(selected_genre);
    return false;
});

//clear filter handling
$("#reset").on("click",function(){
    explorebyGenrePopularity(target_genre=null);
    return false;

})

