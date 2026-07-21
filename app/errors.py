from flask import render_template

# Error handlers for the application
def page_not_found(error):
    return render_template('errors/404.html', error=error), 404

def internal_server_error(error):
    return render_template('errors/500.html', error=error), 500