from flask import render_template

def webapp(request):
    """HTTP Cloud Function.
    Args:
        request (flask.Request): The request object.
        <https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data>
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <https://flask.palletsprojects.com/en/1.1.x/api/#flask.make_response>.
    """
    # Set CORS headers for the preflight request
    if request.method == 'OPTIONS':
        # Allows GET requests from any origin with the Content-Type
        # header and caches preflight response for an 3600s
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600'
        }

        return ('', 204, headers)

    # Set CORS headers for the main request
    headers = {
        'Access-Control-Allow-Origin': '*'
    }

    valid_pages = ["home", "jobs", "about", "about_legals", "about_offices"]
    
    request_args = request.args

    if request_args and 'page' in request_args and request_args['page'] in valid_pages:
        page = request_args['page']
    elif not request_args:
        page = 'home'        
    else:
        return ('Page not found. Expected ?page=...', 404, headers)

    return (render_template(f"{page}.html"), 200, headers)
