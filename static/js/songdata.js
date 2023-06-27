
function generateColor(){
      var colorR = Math.floor((Math.random() * 256));
      var colorG = Math.floor((Math.random() * 256));
      var colorB = Math.floor((Math.random() * 256));

      var BGColor = "rgb(" + colorR + "," + colorG + "," + colorB + ")";

      return BGColor;

}

$('#song-div').jstree();

$('#artist-years').jstree();

$('#artist-songs').jstree();

/*
$('#song-div').jstree({
  "core" : {
    "themes" : {
      "variant" : "large"
    }
  }
});*/
