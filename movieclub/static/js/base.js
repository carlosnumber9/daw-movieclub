




function tmdb_get(query, page) {
	url = 'http://api.themoviedb.org/3/';
	api_key = '51aad3497f36ee29ca6359394cc828e4';

	$.ajax({
		type: "GET",
		url: url + query + '?api_key=' +  api_key + '&page=' + page + "&language=es-ES",
		dataType: "jsonp",
	}).error(function() {
		console.log('error')
	}).done(function(response) {
		return response;
	});

}





$(document).ready(function (){

// var divpelis = document.getElementsByClassName("pelicula");
$(".pelicula").hover(
	function() {
	  $(this).css("border","2px solid white");
	}, function() {
		$(this).css("border","none");
	}
  );



});