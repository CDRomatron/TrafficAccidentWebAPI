$(document).ready(function(){
    function getLocation() {
      if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(showPosition);
      }
      else
      {
        x.innerHTML = "Geolocation is not supported by this browser";
      }
    }
    
    var plat = 0;
    var plong = 0;

    function showPosition(position) {
      plat = position.coords.latitude;
      plong = position.coords.longitude;
    }
    
    getLocation();

    setTimeout(function(){
      $.post("/post/", {lat:plat, long:plong}, function(result){
        document.write(result);
      }); 
    }, 100);

    
});
