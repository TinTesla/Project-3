console.log(artist_stats)

var labels = artist_stats['Graph_data']['labels'];
var datasets = artist_stats['Graph_data']['datasets'];

var data = {"labels": labels,"datasets": datasets};

//creating radar using chart.js for each artist
var ctx = $("#artist-canvas");
new Chart(ctx, {
        type: 'radar',
        data: data,
        options: {
        elements: {
          line: {
            borderWidth: 3
          }
        },
        plugins: {
                  legend: {
                     display: true,
                     position: 'bottom'
                  }
      }
      }
      });
