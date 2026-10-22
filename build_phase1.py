import os

files = {
    "c:/cep/documentready/requirements.txt": """Flask==3.0.3
python-dotenv==1.0.1
jsonschema==4.21.1
pytest==8.1.1
""",
    "c:/cep/documentready/.env.example": """SECRET_KEY=super-secret-key-change-me
FLASK_ENV=development
""",
    "c:/cep/documentready/config.py": """import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-default'
    JSON_SORT_KEYS = False

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
""",
    "c:/cep/documentready/run.py": """from app import create_app

app = create_app('development')

if __name__ == '__main__':
    app.run(debug=True)
""",
    "c:/cep/documentready/app/__init__.py": """from flask import Flask

def create_app(config_name='development'):
    app = Flask(__name__)
    
    if config_name == 'development':
        app.config.from_object('config.DevelopmentConfig')
    elif config_name == 'testing':
        app.config.from_object('config.TestingConfig')
    else:
        app.config.from_object('config.ProductionConfig')

    @app.after_request
    def set_security_headers(response):
        response.headers['Content-Security-Policy'] = "default-src 'self'"
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['Referrer-Policy'] = 'no-referrer'
        return response
        
    @app.errorhandler(404)
    def page_not_found(e):
        return {"error": {"code": "NOT_FOUND", "message": "Resource not found"}}, 404
        
    @app.errorhandler(500)
    def internal_server_error(e):
        return {"error": {"code": "INTERNAL_ERROR", "message": "Internal server error"}}, 500

    from .routes import api, pages
    # app.register_blueprint(api.bp)
    # app.register_blueprint(pages.bp)

    return app
""",
    "c:/cep/documentready/app/routes/__init__.py": "",
    "c:/cep/documentready/app/routes/api.py": """from flask import Blueprint, jsonify

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/health')
def health():
    return jsonify({
        "data": {"status": "ok", "services": 0, "documents": 0},
        "meta": {"disclaimer": "Document requirements may vary...", "api_version": "1"}
    })
""",
    "c:/cep/documentready/app/routes/pages.py": """from flask import Blueprint, render_template

bp = Blueprint('pages', __name__)

@bp.route('/')
def index():
    return "DocumentReady"
""",
    "c:/cep/documentready/app/static/css/variables.css": """:root{
  --navy:#1F4E79; --ink:#14324F; --teal:#0E8C8C; --tint:#EAF1F8; --teal-tint:#E1F3F2;
  --green:#2E8B57; --green-tint:#E4F4EA; --amber:#C8701A; --amber-tint:#FDF0E0;
  --grey:#56677A; --line:#C5D3E0; --white:#FFFFFF;
  --radius:10px; --space:8px; --font:system-ui,"Segoe UI",Calibri,Arial,sans-serif;
}
"""
}

for path, content in files.items():
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

print("Phase 1 files written.")
