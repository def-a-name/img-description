from db import db
from db.models import user_datastore
from db.models import User, UserRequest, AiResponse, Query
from flask import jsonify
from datetime import datetime

__all__ = ['add_error_request', 'add_success_request', 'add_error_response', 'add_success_response', 
           'get_debug_data', 'add_query', 'get_queries']

def get_user_by_uuid(user_id):
    return User.query.filter_by(fs_uniquifier=user_id).first()

def get_user_by_id(user_id):
    return User.query.filter_by(id=user_id).first()

def get_user_by_name(name):
    return User.query.filter_by(username=name).first()

def get_all_users():
    return User.query.all()

def delete_user_by_id(user_id):
    user = get_user_by_id(user_id)
    if (user):
        db.session.delete(user)
        db.session.commit()
    return user

def register_user(user_name, hashed_passwd):
    user = User(
        username=user_name,
        password=hashed_passwd
    )
    db.session.add(user)
    db.session.commit()
    return user

def change_user_password(user_id, hashed_passwd):
    user = get_user_by_id(user_id)
    if (user):
        user.password = hashed_passwd
        db.session.commit()
    return user

def update_db():
    db.session.commit()

def add_error_request(uid, up_time, msg):
    req = UserRequest(user_id=uid,
                      upload_time=up_time, 
                      request_time='', 
                      token_count=0,
                      status_code=400, 
                      error_message=msg)
    db.session.add(req)
    db.session.commit()
    return jsonify({'error': msg}), 400

def add_success_request(uid, up_time, tok_cnt):
    time_str = datetime.now().strftime('%Y%m%d %H:%M:%S')
    req = UserRequest(user_id=uid,
                      upload_time=up_time, 
                      request_time=time_str, 
                      token_count=tok_cnt,
                      status_code=200, 
                      error_message='')
    db.session.add(req)
    db.session.commit()
    return req

def add_error_response(uid, req_id, msg):
    time_str = datetime.now().strftime('%Y%m%d %H:%M:%S')
    res = AiResponse(user_id=uid,
                     request_id=req_id, 
                     respond_time=time_str, 
                     model='', 
                     description='无效描述', 
                     token_count=0,
                     status_code=500, 
                     error_message=msg)
    db.session.add(res)
    db.session.commit()
    return res

def add_success_response(uid, req_id, mdl, desc, tok_cnt):
    time_str = datetime.now().strftime('%Y%m%d %H:%M:%S')
    res = AiResponse(user_id=uid,
                     request_id=req_id, 
                     respond_time=time_str, 
                     model=mdl, 
                     description=desc, 
                     token_count=tok_cnt,
                     status_code=200, 
                     error_message='')
    db.session.add(res)
    db.session.commit()
    return res

def get_debug_data(uid):
    user_requests = UserRequest.query.filter_by(user_id=uid) \
                                     .order_by(UserRequest.id.desc()).all()
    ai_responses = AiResponse.query.filter_by(user_id=uid) \
                                   .order_by(AiResponse.id.desc()).all()
    return user_requests, ai_responses

def add_query(uid, uname, up_time, req_time, res_time, model, desc, tok_cnt, scode, err_msg):
    query = Query(user_id=uid,
                  username=uname,
                  upload_time=up_time,
                  request_time=req_time,
                  respond_time=res_time,
                  model=model,
                  description=desc,
                  token_used=tok_cnt,
                  status_code=scode,
                  error_message=err_msg)
    db.session.add(query)
    db.session.commit()
    return query

def get_queries():
    return Query.query.order_by(Query.id.desc()).all()