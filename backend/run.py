from app import create_app
from app.admin_routes import admin_bp

app.register_blueprint(admin_bp)


app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)

