import os
from flask import Flask, request, abort
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Api, Resource
from flask_bcrypt import Bcrypt, generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_cors import CORS
import datetime


app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///event_manager.db'
db = SQLAlchemy(app)
ma = Marshmallow(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
app.config['JWT_SECRET_KEY'] = 'de03xR0aV7i07k9Ti4ya24Dbb8oOo5pQ'


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    

    def hash_password(self):
        self.password = generate_password_hash(self.password).decode('utf8')


    def check_password(self, password):
        return check_password_hash(self.password, password)


class User_Schema(ma.Schema):
    class Meta:
        fields = ("id", "first_name", "last_name", "email", "password")


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    category_id = db.Column(db.Integer, nullable=False)
    location = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    online = db.Column(db.Boolean, nullable=False)


class Event_Schema(ma.Schema):
    class Meta:
        fields = ("id", "created_at", "user_id", "name", "category_id", "location", "address", "start_date", "end_date", "online")


user_schema = User_Schema()
event_schema = Event_Schema()
events_schema = Event_Schema(many = True)


api = Api(app)


class UserRegistrationResource(Resource):
    def post(self):
        email = request.get_json().get('email', None)
        password = request.get_json().get('password', None)
        first_name = request.get_json().get('first_name', None)
        last_name = request.get_json().get('last_name', None)

        if email is None or password is None or first_name is None or last_name is None:
            return {'error': 'missing data'}, 400

        if User.query.filter_by(email=email).first() is not None:
            return {'error': 'existing user'}, 400

        new_user = User(email=email, password=password, first_name=first_name, last_name=last_name)
        new_user.hash_password()

        db.session.add(new_user)
        db.session.commit()

        return user_schema.dump(new_user)


class UserLoginResource(Resource):
    def post(self):
        email = request.get_json().get('email', None)
        if email is None:
            return {'error': 'email not supplied'}, 400

        user = User.query.filter_by(email=email).first()
        if user is None:
            return {'error': 'user does not exist'}, 401

        password = request.get_json().get('password', None)
        if password is None:
            return {'error': 'password not supplied'}, 400

        authorized = user.check_password(password)
        if not authorized:
            return {'error': 'invalid password'}, 401

        expires = datetime.timedelta(days=1)
        access_token = create_access_token(identity=user.id, expires_delta=expires)

        return {'user_id': user.id, 'name': user.first_name, 'token': access_token}, 200


class UserEventsResource(Resource):
    @jwt_required
    def get(self, user_id):
        user_id_token = get_jwt_identity()
        if user_id != user_id_token:
            return {'error': 'invalid token'}, 401

        User.query.get_or_404(user_id)
        events = Event.query.filter_by(user_id=user_id).order_by(Event.created_at.desc())

        return events_schema.dump(events)


    @jwt_required
    def post(self, user_id):
        User.query.get_or_404(user_id)
        user_id_token = get_jwt_identity()
        if user_id != user_id_token:
            return {'error': 'invalid token'}, 401

        name = request.get_json().get('name', None)
        category_id = request.get_json().get('category_id', None)
        location = request.get_json().get('location', None)
        address = request.get_json().get('address', None)
        start_date = request.get_json().get('start_date', None)
        end_date = request.get_json().get('end_date', None)
        online = request.get_json().get('online', None)
        
        if name is None or category_id is None or location is None or address is None or start_date is None or end_date is None or online is None:
            return {'error': 'missing data'}, 400

        new_event = Event(user_id=user_id, name=name, category_id=category_id, location=location, address=address, 
        start_date=datetime.datetime.strptime(start_date, '%Y-%m-%d'), end_date=datetime.datetime.strptime(end_date, '%Y-%m-%d'), online=online)

        db.session.add(new_event)
        db.session.commit()

        return event_schema.dump(new_event)


class OneEventResource(Resource):
    @jwt_required
    def get(self, event_id):
        event = Event.query.get_or_404(event_id)
        user_id_token = get_jwt_identity()
        if event.user_id != user_id_token:
            return {'error': 'invalid token'}, 401

        return event_schema.dump(event)


    @jwt_required
    def put(self, event_id):
        event = Event.query.get_or_404(event_id)
        user_id_token = get_jwt_identity()
        if event.user_id != user_id_token:
            return {'error': 'invalid token'}, 401

        name = request.get_json().get('name', None)
        category_id = request.get_json().get('category_id', None)
        location = request.get_json().get('location', None)
        address = request.get_json().get('address', None)
        start_date = request.get_json().get('start_date', None)
        end_date = request.get_json().get('end_date', None)
        online = request.get_json().get('online', None)
        
        if name is None or category_id is None or location is None or address is None or start_date is None or end_date is None or online is None:
            return {'error': 'missing data'}, 400

        event.name = name
        event.category_id = category_id
        event.location = location
        event.address = address
        event.start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
        event.end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')
        event.online = online

        db.session.commit()

        return event_schema.dump(event)


    @jwt_required
    def delete(self, event_id):
        event = Event.query.get_or_404(event_id)
        user_id_token = get_jwt_identity()
        if event.user_id != user_id_token:
            return {'error': 'invalid token'}, 401
        
        db.session.delete(event)
        db.session.commit()

        return '', 204


api.add_resource(UserRegistrationResource, '/registration')
api.add_resource(UserLoginResource, '/login')
api.add_resource(UserEventsResource, '/user/<int:user_id>')
api.add_resource(OneEventResource,'/event/<int:event_id>')


if __name__ == '__main__':
    if not os.path.exists('event_manager.db'):
        db.create_all()
    app.run(debug=True)