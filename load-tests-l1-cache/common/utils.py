def get_resources(client, page):
	"""Grab the assets from the cloud storage"""
	client.get("https://storage.googleapis.com/julianferres-static/assets/js/jquery.min.js")
	client.get("https://storage.googleapis.com/julianferres-static/assets/js/jquery.dropotron.min.js")
	client.get("https://storage.googleapis.com/julianferres-static/assets/js/jquery.scrolly.min.js")
	client.get("https://storage.googleapis.com/julianferres-static/assets/js/browser.min.js")
	client.get("https://storage.googleapis.com/julianferres-static/assets/js/breakpoints.min.js")
	client.get("https://storage.googleapis.com/julianferres-static/assets/js/util.js")
	client.get("https://storage.googleapis.com/julianferres-static/assets/js/main.js")
	client.get("https://storage.googleapis.com/julianferres-static/assets/css/fontawesome-all.min.css")
	client.get("https://fonts.googleapis.com/css?family=Open+Sans:400,400italic,700,700italic|Open+Sans+Condensed:700")
	client.get("https://fonts.gstatic.com/s/opensans/v26/memvYaGs126MiZpBA-UvWbX2vVnXBbObj2OVTS-muw.woff2")
	client.get("https://fonts.gstatic.com/s/opensanscondensed/v15/z7NFdQDnbTkabZAIOl9il_O6KJj73e7Ff0GmDuXMRw.woff2")
	client.get("https://storage.googleapis.com/julianferres-static/images/favicon.png")
	
	if not page or page == "home":
		client.get("https://storage.googleapis.com/julianferres-static/assets/css/images/overlay.png")
		client.get("https://storage.googleapis.com/julianferres-static/images/banner.jpg")
		client.get("https://storage.googleapis.com/julianferres-static/assets/css/images/highlight.png")


def post_visit_and_get_counter(client, page):
	client.post(f"/post-visit?page={page}", json={})
	client.get(f"/get-count?page={page}")
