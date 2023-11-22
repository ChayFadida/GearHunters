from flask import Flask, render_template
from routes.products import products_bp
import os

# Verify dot env path
env_file_path = os.path.join(os.path.dirname(__file__), '..', '.env')

app = Flask(__name__)

# Add the following lines to configure the static folder
app.config['STATIC_FOLDER'] = 'static'

# Register the authentication Blueprint
app.register_blueprint(products_bp)


@app.route('/')
def index():
    """
    Render the main web page.

    This route is responsible for rendering the main web page, displaying data from the data handler.

    Returns:
        Flask Response: The rendered HTML template.
    """
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)