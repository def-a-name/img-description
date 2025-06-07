from db import db
import zlib

class UserRequest(db.Model):
    __tablename__ = 'user_requests'
    id = db.Column(db.Integer, primary_key=True)
    upload_time = db.Column(db.String(32))
    request_time = db.Column(db.String(32))
    token_count = db.Column(db.Integer)
    status_code = db.Column(db.Integer)
    error_message = db.Column(db.Text, default='')

    response = db.relationship('AiResponse', backref='request', uselist=False)

class AiResponse(db.Model):
    __tablename__ = 'ai_responses'
    id = db.Column(db.Integer, primary_key=True)
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
