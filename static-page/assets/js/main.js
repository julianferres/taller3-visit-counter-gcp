(function ($) {

	const BASE_PATH = 'https://southamerica-east1-taller3-julianferres.cloudfunctions.net';

	const search_params = new URLSearchParams(window.location.search);
	const page_type = search_params.get('page');

	// Endpoints para agregar y obtener la cantidad de visitas
	fetch(BASE_PATH + '/post-visit?visit_type=' + page_type)

	fetch(BASE_PATH + '/get-count?visit_type=' + page_type)
		.then(response => response.text())
		.then(data => { $('#contador').text('Contador de visitas: ' + data); })
		.catch(function (error) {
			console.log('Looks like there was a problem: \n', error);
		});

	// Dropdowns.
	$('#nav > ul').dropotron({
		mode: 'fade',
		noOpenerFade: true,
		alignment: 'center'
	});

})(jQuery);