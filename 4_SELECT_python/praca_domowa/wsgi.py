from app import create_app

# Procfile use 'app' variable from this module
# look: http://flask.pocoo.org/docs/1.0/patterns/appfactories/
#       https://stackoverflow.com/questions/25319690/how-do-i-run-a-flask-app-in-gunicorn-if-i-used-the-application-factory-pattern
app = create_app()
