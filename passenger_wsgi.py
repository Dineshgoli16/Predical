import os
import sys
import traceback

# Add the application directory to the path
sys.path.insert(0, os.path.dirname(__file__))

def application(environ, start_response):
    try:
        from main import app as flask_app
        return flask_app(environ, start_response)
    except Exception as e:
        # If it crashes, show the error in the browser
        status = '500 Internal Server Error'
        response_headers = [('Content-type', 'text/plain')]
        start_response(status, response_headers)
        return [f"App Startup Failed:\n\n{traceback.format_exc()}".encode('utf-8')]
