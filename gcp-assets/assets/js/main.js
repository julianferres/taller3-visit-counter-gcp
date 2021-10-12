/*
	TXT by HTML5 UP
	html5up.net | @ajlkn
	Free for personal and commercial use under the CCA 3.0 license (html5up.net/license)
*/

(function ($) {

	var $window = $(window),
		$body = $('body'),
		$nav = $('#nav');

	const WEB_APP = 'https://europe-west2-taller3-julianferres.cloudfunctions.net';
	const search_params = new URLSearchParams(window.location.search);
	const page = search_params.get('page');

	// Endpoints para agregar y obtener la cantidad de visitas
	let data = {};

	fetch(WEB_APP + '/post-visit?page=' + page, {
		method: "POST",
		body: JSON.stringify(data)
	}).then(res => {
		console.log("Request to increment complete for page: " + page + "! response:", res);
	}).catch(function (error) {
		console.log('A problem have ocurred :/ : \n', error);
	});

	fetch(WEB_APP + '/get-count?page=' + page)
		.then(response => response.text())
		.then(data => { $('#count').text('Cantidad de visitas: ' + data); })
		.catch(function (error) {
			console.log('A problem have ocurred :/ : \n', error);
		});

	// Breakpoints.
	breakpoints({
		xlarge: ['1281px', '1680px'],
		large: ['981px', '1280px'],
		medium: ['737px', '980px'],
		small: ['361px', '736px'],
		xsmall: [null, '360px']
	});

	// Play initial animations on page load.
	$window.on('load', function () {
		window.setTimeout(function () {
			$body.removeClass('is-preload');
		}, 100);
	});

	// Dropdowns.
	$('#nav > ul').dropotron({
		mode: 'fade',
		noOpenerFade: true,
		speed: 300,
		alignment: 'center'
	});

	// Scrolly
	$('.scrolly').scrolly({
		speed: 1000,
		offset: function () { return $nav.height() - 5; }
	});

	// Nav.

	// Title Bar.
	$(
		'<div id="titleBar">' +
		'<a href="#navPanel" class="toggle"></a>' +
		'<span class="title">' + $('#logo').html() + '</span>' +
		'</div>'
	)
		.appendTo($body);

	// Panel.
	$(
		'<div id="navPanel">' +
		'<nav>' +
		$('#nav').navList() +
		'</nav>' +
		'</div>'
	)
		.appendTo($body)
		.panel({
			delay: 500,
			hideOnClick: true,
			hideOnSwipe: true,
			resetScroll: true,
			resetForms: true,
			side: 'left',
			target: $body,
			visibleClass: 'navPanel-visible'
		});

})(jQuery);