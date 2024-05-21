from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import timedelta
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'
app.permanent_session_lifetime = timedelta(minutes=30)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    phone = db.Column(db.String(20), unique=True)

    def __repr__(self):
        return f'<User {self.name}>'

class ExerciseData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    count = db.Column(db.Integer)
    left_forearm_innerbody = db.Column(db.Integer)
    left_forearm_outterbody = db.Column(db.Integer)
    right_forearm_innerbody = db.Column(db.Integer)
    right_forearm_outterbody = db.Column(db.Integer)
    user = db.relationship('User', backref=db.backref('exercise_data', lazy=True))

    def __repr__(self):
        return f'<ExerciseData User: {self.user_id}, Count: {self.count}>'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        session.permanent = True
        name = request.form['name']
        phone = request.form['phone']
        user = User.query.filter_by(name=name).first()
        
        if user is None:
            user = User(name=name, phone=phone)
            db.session.add(user)
            db.session.commit()
        else:
            if user.phone != phone:
                flash('전화번호가 일치하지 않습니다.')
                return redirect(url_for('home'))

        session['name'] = user.name
        session['phone'] = user.phone
        session['user_id'] = user.id
        flash('로그인 성공!')
        return redirect(url_for('select'))
    return render_template('index.html')

@app.route('/logout')
def logout():
    session.pop('name', None)
    session.pop('phone', None)
    session.pop('user_id', None)
    flash('로그아웃 되었습니다.')
    return redirect(url_for('home'))

@app.route('/select')
def select():
    if 'name' in session and 'phone' in session:
        name = session['name']
        return render_template('select.html', name=name)
    else:
        flash('로그인이 필요합니다.')
        return redirect(url_for('home'))

@app.route('/rank')
def rank():
    return render_template('rank.html')

@app.route('/anal')
def anal():
    return render_template('anal.html')

@app.route('/exercise1')
def exercise1():
    return render_template('exercise1.html')

@app.route('/exercise2')
def exercise2():
    return render_template('exercise2.html')

@app.route('/exercise3')
def exercise3():
    return render_template('exercise3.html')

@app.route('/save_exercise_data', methods=['POST'])
def save_exercise_data():
    if 'user_id' not in session:
        return jsonify({'error': 'User not logged in'}), 400
    
    data = request.json
    user_id = session['user_id']
    # 로그 추가: 요청 데이터를 출력
    print("Received data:", data)
    
    count = data.get('count')
    left_forearm_innerbody = data.get('left_forearm_innerbody')
    left_forearm_outterbody = data.get('left_forearm_outterbody')
    right_forearm_innerbody = data.get('right_forearm_innerbody')
    right_forearm_outterbody = data.get('right_forearm_outterbody')
    count = data.get('count')
    left_forearm_innerbody = data.get('left_forearm_innerbody')
    left_forearm_outterbody = data.get('left_forearm_outterbody')
    right_forearm_innerbody = data.get('right_forearm_innerbody')
    right_forearm_outterbody = data.get('right_forearm_outterbody')

# 로그 추가: 데이터가 올바르게 추출되었는지 확인
    print("Parsed data:", count, left_forearm_innerbody, left_forearm_outterbody, right_forearm_innerbody, right_forearm_outterbody)
    exercise_data = ExerciseData(
        user_id=user_id,
        count=count,
        left_forearm_innerbody=left_forearm_innerbody,
        left_forearm_outterbody=left_forearm_outterbody,
        right_forearm_innerbody=right_forearm_innerbody,
        right_forearm_outterbody=right_forearm_outterbody
    )

    db.session.add(exercise_data)
    db.session.commit()
    # 로그 추가: 데이터가 커밋된 후 로그 출력
    print("Data committed to database")
    return jsonify({'message': 'Exercise data saved successfully'}), 200

if __name__ == '__main__':
    app.run(debug=True)
