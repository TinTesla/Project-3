

var x = [];
var y = [];
var result_x = [];
var result_y = [];
var r2;
var equation;
var result;
var ctx;

//Only for bpm vs popularity
var bpm_popularity = yearly_characteristics_data["bpm"];
result = regression.linear(bpm_popularity);

r2 = result["r2"];
equation = result["string"];

$(bpm_popularity).each(function(i,bpm_data){
    x.push(bpm_data[0])
    y.push(bpm_data[1])

})

$(result["points"]).each(function(i,bpm_resultdata){
    result_x.push(bpm_resultdata[0])
    result_y.push(bpm_resultdata[1])

})

//creating bar chart using chart.js , bpm vs popularity
ctx = $("#bpm");
new Chart(ctx, {
        type: 'scatter',
        data: {
          labels: x,
          datasets: [{
            label: 'Bpm vs Popularity',
            data: y,
            borderWidth: 1,
            borderColor: "black",
            backgroundColor: "orange",
            yAxisID: 'y'
          },
          {
            label: 'Regression points',
            data: result_y,
            borderWidth: 1,
            borderColor: "black",
            backgroundColor: "blue",
            yAxisID: 'y'
          }]
        }
      });

$('#bpm-eq').text(equation)
$('#bpm-eq-r2').text(r2)


//Only for energy vs popularity
var energy_popularity = yearly_characteristics_data["energy"];
result = regression.linear(energy_popularity);

r2 = result["r2"];
equation = result["string"];

$(energy_popularity).each(function(i,energy_data){
    x.push(energy_data[0])
    y.push(energy_data[1])

})

$(result["points"]).each(function(i,energy_resultdata){
    result_x.push(energy_resultdata[0])
    result_y.push(energy_resultdata[1])

})

//creating line chart using chart.js , energy vs popularity
ctx = $("#energy");
new Chart(ctx, {
        type: 'scatter',
        data: {
          labels: x,
          datasets: [{
            label: 'Energy vs Popularity',
            data: y,
            borderWidth: 1,
            borderColor: "black",
            backgroundColor: "orange",
            yAxisID: 'y'
          },
          {
            label: 'Regression points',
            data: result_y,
            borderWidth: 1,
            borderColor: "black",
            backgroundColor: "blue",
            yAxisID: 'y'
          }]
        }
      });

$('#energy-eq').text(equation)
$('#energy-eq-r2').text(r2)



//Only for danceability vs popularity
var dance_popularity = yearly_characteristics_data["danceability"];
result = regression.linear(dance_popularity);

r2 = result["r2"];
equation = result["string"];

$(dance_popularity).each(function(i,data){
    x.push(data[0])
    y.push(data[1])

})

$(result["points"]).each(function(i,resultdata){
    result_x.push(resultdata[0])
    result_y.push(resultdata[1])

})

//creating line chart using chart.js , danceability vs popularity
ctx = $("#dance");
new Chart(ctx, {
        type: 'scatter',
        data: {
          labels: x,
          datasets: [{
            label: 'Danceability vs Popularity',
            data: y,
            borderWidth: 1,
            borderColor: "black",
            backgroundColor: "orange",
            yAxisID: 'y'
          },
          {
            label: 'Regression points',
            data: result_y,
            borderWidth: 1,
            borderColor: "black",
            backgroundColor: "blue",
            yAxisID: 'y'
          }]
        }
      });

$('#dance-eq').text(equation)
$('#dance-eq-r2').text(r2)


//Only for liveness vs popularity
var live_popularity = yearly_characteristics_data["liveness"];
result = regression.linear(live_popularity);

r2 = result["r2"];
equation = result["string"];

$(live_popularity).each(function(i,data){
    x.push(data[0])
    y.push(data[1])

})

$(result["points"]).each(function(i,resultdata){
    result_x.push(resultdata[0])
    result_y.push(resultdata[1])

})

//creating line chart using chart.js , liveness vs popularity
ctx = $("#liveness");
new Chart(ctx, {
        type: 'scatter',
        data: {
          labels: x,
          datasets: [{
            label: 'Liveness vs Popularity',
            data: y,
            borderWidth: 1,
            borderColor: "black",
            backgroundColor: "orange",
            yAxisID: 'y'
          },
          {
            label: 'Regression points',
            data: result_y,
            borderWidth: 1,
            borderColor: "black",
            backgroundColor: "blue",
            yAxisID: 'y'
          }]
        }
      });

$('#liveness-eq').text(equation)
$('#liveness-eq-r2').text(r2)


//Only for valence vs popularity
var valence_popularity = yearly_characteristics_data["valence"];
result = regression.linear(valence_popularity);

r2 = result["r2"];
equation = result["string"];

$(valence_popularity).each(function(i,data){
    x.push(data[0])
    y.push(data[1])

})

$(result["points"]).each(function(i,resultdata){
    result_x.push(resultdata[0])
    result_y.push(resultdata[1])

})

//creating line chart using chart.js , valence vs popularity
ctx = $("#valence");
new Chart(ctx, {
        type: 'scatter',
        data: {
          labels: x,
          datasets: [{
            label: 'Valence vs Popularity',
            data: y,
            borderWidth: 1,
            borderColor: "black",
            backgroundColor: "orange",
            yAxisID: 'y'
          },
          {
            label: 'Regression points',
            data: result_y,
            borderWidth: 1,
            borderColor: "black",
            backgroundColor: "blue",
            yAxisID: 'y'
          }]
        }
      });

$('#val-eq').text(equation)
$('#val-eq-r2').text(r2)




//Only for duration vs popularity
var duration_popularity = yearly_characteristics_data["duration"];
result = regression.linear(duration_popularity);

r2 = result["r2"];
equation = result["string"];

$(duration_popularity).each(function(i,data){
    x.push(data[0])
    y.push(data[1])

})

$(result["points"]).each(function(i,resultdata){
    result_x.push(resultdata[0])
    result_y.push(resultdata[1])

})

//creating line chart using chart.js , duration vs popularity
ctx = $("#duration");
new Chart(ctx, {
        type: 'scatter',
        data: {
          labels: x,
          datasets: [{
            label: 'Duration vs Popularity',
            data: y,
            borderWidth: 1,
            borderColor: "black",
            backgroundColor: "orange",
            yAxisID: 'y'
          },
          {
            label: 'Regression points',
            data: result_y,
            borderWidth: 1,
            borderColor: "black",
            backgroundColor: "blue",
            yAxisID: 'y'
          }]
        }
      });

$('#dur-eq').text(equation)
$('#dur-eq-r2').text(r2)



//Only for acousticness vs popularity
var acoust_popularity = yearly_characteristics_data["acousticness"];
result = regression.linear(acoust_popularity);

r2 = result["r2"];
equation = result["string"];

$(acoust_popularity).each(function(i,data){
    x.push(data[0])
    y.push(data[1])

})

$(result["points"]).each(function(i,resultdata){
    result_x.push(resultdata[0])
    result_y.push(resultdata[1])

})

//creating line chart using chart.js , acousticness vs popularity
ctx = $("#acousticness");
new Chart(ctx, {
        type: 'scatter',
        data: {
          labels: x,
          datasets: [{
            label: 'Acousticness vs Popularity',
            data: y,
            borderWidth: 1,
            borderColor: "black",
            backgroundColor: "orange",
            yAxisID: 'y'
          },
          {
            label: 'Regression points',
            data: result_y,
            borderWidth: 1,
            borderColor: "black",
            backgroundColor: "blue",
            yAxisID: 'y'
          }]
        }
      });

$('#acc-eq').text(equation)
$('#acc-eq-r2').text(r2)


//Only for speechiness vs popularity
var speech_popularity = yearly_characteristics_data["speechiness"];
result = regression.linear(speech_popularity);

r2 = result["r2"];
equation = result["string"];

$(speech_popularity).each(function(i,data){
    x.push(data[0])
    y.push(data[1])

})

$(result["points"]).each(function(i,resultdata){
    result_x.push(resultdata[0])
    result_y.push(resultdata[1])

})

//creating line chart using chart.js , speechiness vs popularity
ctx = $("#speechiness");
new Chart(ctx, {
        type: 'scatter',
        data: {
          labels: x,
          datasets: [{
            label: 'Speechiness vs Popularity',
            data: y,
            borderWidth: 1,
            borderColor: "black",
            backgroundColor: "orange",
            yAxisID: 'y'
          },
          {
            label: 'Regression points',
            data: result_y,
            borderWidth: 1,
            borderColor: "black",
            backgroundColor: "blue",
            yAxisID: 'y'
          }]
        }
      });

$('#sph-eq').text(equation)
$('#sph-eq-r2').text(r2)
