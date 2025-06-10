from db import db
from flask_security import UserMixin, RoleMixin
from flask_security import SQLAlchemyUserDatastore
import zlib
import uuid

roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16), unique=True, nullable=False)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    active = db.Column(db.Boolean(), default=True)
    
    username = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    fs_uniquifier = db.Column(db.String(64), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))

    requests = db.relationship('UserRequest', backref='user', lazy=True)
    queries = db.relationship('Query', backref='user', lazy=True)

user_datastore = SQLAlchemyUserDatastore(db, User, Role)

class UserRequest(db.Model):
    __tablename__ = 'user_requests'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) 
    
    upload_time = db.Column(db.String(32))
    request_time = db.Column(db.String(32))
    token_count = db.Column(db.Integer)
    status_code = db.Column(db.Integer)
    error_message = db.Column(db.Text, default='')

    response = db.relationship('AiResponse', backref='request', uselist=False)

class AiResponse(db.Model):
    __tablename__ = 'ai_responses'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) 
    
    request_id = db.Column(db.Integer, db.ForeignKey('user_requests.id'), nullable=False)
    respond_time = db.Column(db.String(32))
    model = db.Column(db.String(32))
    description_compressed = db.Column(db.LargeBinary)  # 使用压缩后的字段
    token_count = db.Column(db.Integer)
    status_code = db.Column(db.Integer)
    error_message = db.Column(db.Text, default='')

    @property
    def description(self):
        if self.description_compressed:
            return zlib.decompress(self.description_compressed).decode('utf-8')
        return ''

    @description.setter
    def description(self, value):
        self.description_compressed = zlib.compress(value.encode('utf-8'))

class Query(db.Model):
    __tablename__ = 'queries'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) 

    username = db.Column(db.String(64), unique=True, nullable=False)
    upload_time = db.Column(db.String(32))
    request_time = db.Column(db.String(32))
    respond_time = db.Column(db.String(32))
    model = db.Column(db.String(32))
    description_compressed = db.Column(db.LargeBinary)  # 使用压缩后的字段
    token_used = db.Column(db.Integer)
    status_code = db.Column(db.Integer)
    error_message = db.Column(db.Text, default='')

    @property
    def description(self):
        if self.description_compressed:
            return zlib.decompress(self.description_compressed).decode('utf-8')
        return ''

    @description.setter
    def description(self, value):
        self.description_compressed = zlib.compress(value.encode('utf-8'))
