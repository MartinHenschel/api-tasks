from flask import Flask
from models import db
from routes import init_routes
from flask_jwt_extended import JWTManager
from flask_cors import CORS

app = Flask(__name__)

CORS(app)  # 👈 AGORA SIM (depois de criar o app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['JWT_SECRET_KEY'] = 'segredo_super_secreto'

db.init_app(app)
jwt = JWTManager(app)

init_routes(app)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)