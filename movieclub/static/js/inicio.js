



	function ver(id){

		//var idpeli = $(this).attr('id');

		$('.titsec, .conjunto').fadeOut(2000);

		query = "movie/" + id;

		$.ajax({
			type: "GET",
		url: url + query + '?api_key=' +  api_key + "&language=es-ES",
			dataType: "jsonp"
		}).error(function() {
			console.log('error')
		}).done(function(response) {
			$('body').append('<div class="container-fluid"><div class="row"><div class="d-none col-lg-10 rounded border m-5"><h3>' 
			+ response.title + 
			'</h3></div></div></div>');
		})

	}




function get_content(query, page){

	url = 'http://api.themoviedb.org/3/';
	api_key = '51aad3497f36ee29ca6359394cc828e4';
	tmd = "https://image.tmdb.org/t/p/w500/";

	$.ajax({
		type: "GET",
		url: url + query + '&api_key=' +  api_key + '&page=' + page + "&language=es-ES",
		dataType: "jsonp"
	}).error(function() {
		console.log('error')
	}).done(function(response) {
		$('body').append('<div class="container-fluid conjunto"><div class="row align-items-center" id="contmov' + page + '"></div></div>');
		for (var i = 0; i < response.results.length; i++) {
			var imagen = (response.results[i].poster_path == null) ? "white" : "url(" + tmd + response.results[i].poster_path + ")";
			var indice = parseInt(i+((page-1)*20));
			$('#contmov' + page).append('<a onClick="ver(' + response.results[i].id + ')"><div id="' + response.results[i].id + '" class="col-lg-2 col-md-3 col-xs-12 m-1 rounded m-3 pelicula" style="background:' + imagen + '"><h5 class="padding-none titmov">' +  response.results[i].title +  '</h5></div></a>');
			//setTimeout(function(){ $('#movie' + i).fadeIn(500);}, 3000);
		}
	})
};








$(document).ready(function (){




	$('.titsec').fadeIn(2000);




	$('.bver').click(function(){
		$(this).fadeOut();

		/*

		var codigo = parseInt($('.titulo').attr('id'));

		url = 'https://api.themoviedb.org/3/movie/' + codigo + '/videos';
		api_key = '51aad3497f36ee29ca6359394cc828e4';
*/

		$('.videomov').fadeIn(1000);




/*
		$.ajax({
			type: "GET",
			url: url + '&api_key=' +  api_key + '&append_to_response=videos&language=es-ES&callback=test',
			dataType: "jsonp",
			contentType: "application/json",
			*/

/*
		$.ajax({
			type: "GET",
			url: url,
			contentType: "application/json",
        	crossDomain: true,
			data: {
				'api_key': api_key,
				'append_to_response': 'videos',
				'language': 'es-ES',
				'callback': 'test'
			}
		}).error(function() {
			console.log('error')
		}).done(function(response) {
			$('body').append('<iframe width="560" height="315" src="https://www.youtube.com/embed/' + response.results[0].key + '" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>').fadeIn(1500);
	});

*/

});
	







	

});