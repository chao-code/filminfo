import os
from app import create_app

app = create_app(os.environ.get('FLASK_ENV', 'development'))

from app import cache

@app.shell_context_processor
def make_shell_context():
    return dict(cache=cache)
