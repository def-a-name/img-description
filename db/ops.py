from db import db
from db.models import UserRequest, AiResponse
from flask import jsonify
from datetime import datetime

__all__ = ['add_error_request', 'add_success_request', 'add_error_response', 'add_success_response', 'get_debug_data']

def add_error_request(up_time, msg):
    req = UserRequest(upload_time=up_time, 
                      request_time='', 
                      token_count=0,
                      status_code=400, 
                      error_message=msg)
    db.session.add(req)
    db.session.commit()
    return jsonify({'error': msg}), 400

def add_success_request(up_time, tok_cnt):
    time_str = datetime.now().strftime('%Y%m%d %H:%M:%S')
    req = UserRequest(upload_time=up_time, 
                      request_time=time_str, 
                      token_count=tok_cnt,
                      status_code=200, 
                      error_message='')
    db.session.add(req)
    db.session.commit()
    return req

def add_error_response(req_id, msg):
    time_str = datetime.now().strftime('%Y%m%d %H:%M:%S')
    res = AiResponse(request_id=req_id, 
                     respond_time=time_str, 
                     model='', 
                     description='无效描述', 
                     token_count=0,
                     status_code=500, 
                     error_message=msg)
    db.session.add(res)
    db.session.commit()
    return jsonify({'error': msg}), 500

def add_success_response(req_id, mdl, desc, tok_cnt):
    time_str = datetime.now().strftime('%Y%m%d %H:%M:%S')
    res = AiResponse(request_id=req_id, 
                     respond_time=time_str, 
                     model=mdl, 
                     description=desc, 
                     token_count=tok_cnt,
                     status_code=200, 
                     error_message='')
    db.session.add(res)
    db.session.commit()
    return res

def get_debug_data():
    return UserRequest.query.order_by(UserRequest.id.desc()).all(), \
           AiResponse.query.order_by(AiResponse.id.desc()).all()
    