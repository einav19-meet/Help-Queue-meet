from model import *

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import datetime

engine = create_engine('sqlite:///space.db')
Base.metadata.create_all(engine)
DBSession = sessionmaker(bind=engine)
session = DBSession()

def add_request(student, question):
    i = session.query(Reqs).filter_by(answered = False).all()
    if len(i) > 0:
        i = i[-1].place + 1
    else:
        i = 0
    req = Reqs(student = student, question = question, answered = False, place = i)
    session.add(req)
    session.commit()

def get_student_reqs(student):
    reqs = session.query(Reqs).filter_by(student = student, answered = False).all()
    return reqs

def get_reqs():
    return session.query(Reqs).filter_by(answered = False).all()

def get_first_req(student):
    req = session.query(Reqs).filter_by(student = student).first()
    return req

def update(id, username):
    student = session.query(Reqs).filter_by(id = id).first().student
    student = get_first_req(student)
    student.answered = True
    student.student = "answered"
    session.commit()
    reqs = get_reqs()
    for r in reqs:
        r.place -= 1
        session.commit()
    
    get_user(username).counter += 1
    session.commit()

def add_user(username, password, role):
    user = Users(username = username, password = password, role = role, counter = 0)
    session.add(user)
    session.commit()

def get_all_students():
    return session.query(Users).filter_by(role = "student").all()

def get_student(username):
    student = session.query(Users).filter_by(username = username).first()
    return student

def get_user(username):
    user = session.query(Users).filter_by(username = username).first()
    return user

def check_username(username):
    users = session.query(Users).filter_by(username = username).all()
    if len(users) > 0:
        return True
    else:
        return False

def check_password(username, password):
    if check_username(username):
        if get_student(username).password == password:
            return True

    return False

# add_user("noam2", "1", "staff")