from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import timedelta, datetime
import os
import openai

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.secret_key = 'your_secret_key'
app.permanent_session_lifetime = timedelta(minutes=30)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

openai.api_key = "OPENAI API KEY 작성"

diagnosis_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'diagnosis')

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
    diagnosis = db.Column(db.Text)  # 진단 결과를 저장할 필드 추가
    exercise_time = db.Column(db.Integer)  # 운동 시간을 저장할 필드 추가 (밀리초 단위)
    date = db.Column(db.DateTime, default=datetime.utcnow)  # 운동 날짜를 저장할 필드 추가
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

def get_gpt_response(log_data):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "너는 아주 친절하고 박학다식한 한국인 트레이너이자 운동처방사야."},
                {"role": "user", "content": f"주어진 불균형 데이터는 숄더프레스 진행시 좌우측 전완근 거리이고 한쪽이 다른 한 쪽에 대해서 불균형하게 벌어질 경우 불균형이라고 판단해. 총 불균형 중 우측 혹은 좌측 중 더 불균형이 자주 일어나는 부분에 대해 알려줘. 그리고 그러한 불균형이 왜 일어나는지 운동 역학적, 기능 해부학적(어떤 근육인지 해부학적용어를 활용해 설명)으로 설명해줘. 그 다음에 앞으로 이렇게 계속 불균형이 발생할 경우 어떤 결과를 초래하게 될 것이라고 이야기 해줘. 마지막으로는 이러한 불균형을 개선하기 위해서는 어떠한 스트레칭이 필요한지 구체적으로 운동 종목을 알려주거나 어떤 운동을 해서 개선할 수 있는지 아주 자세하게 설명해줘. 말투는 친절하고 상냥하게 해줘. 그리고 시작은 회원님~ 이렇게 트레이너처럼 말해주면 좋을 것 같아. 주의: 진단은 일회성으로 끝날것이므로 혹시 더 궁금한 점이 있으시면 언제든지 물어봐 주세요 와 같은 말은 안들어가야함.\n\n{log_data}"}
            ]
        )
        diagnosis = response.choices[0]['message']['content']
        print(f"GPT-3 response: {diagnosis}")  # 진단 결과 로그 출력
        return diagnosis
    except Exception as e:
        error_message = f"진단 중 오류 발생: {str(e)}"
        print(error_message)  # 오류 로그 출력
        return error_message

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
    exercise_time = data.get('exercise_time')  # 운동 시간을 데이터로 받음

    # GPT-3 진단 생성
    log_data = f"Count: {count}, Left Forearm Inner Body: {left_forearm_innerbody}, Left Forearm Outter Body: {left_forearm_outterbody}, Right Forearm Inner Body: {right_forearm_innerbody}, Right Forearm Outter Body: {right_forearm_outterbody}"
    diagnosis = get_gpt_response(log_data)

    # 로그 추가: 데이터가 올바르게 추출되었는지 확인
    print("Parsed data:", count, left_forearm_innerbody, left_forearm_outterbody, right_forearm_innerbody, right_forearm_outterbody)
    print("GPT Diagnosis:", diagnosis)  # 진단 결과 로그 출력

    exercise_data = ExerciseData(
        user_id=user_id,
        count=count,
        left_forearm_innerbody=left_forearm_innerbody,
        left_forearm_outterbody=left_forearm_outterbody,
        right_forearm_innerbody=right_forearm_innerbody,
        right_forearm_outterbody=right_forearm_outterbody,
        diagnosis=diagnosis,
        exercise_time=exercise_time,  # 운동 시간 저장
        date=datetime.utcnow()  # 현재 날짜 저장
    )

    db.session.add(exercise_data)
    db.session.commit()
    # 로그 추가: 데이터가 커밋된 후 로그 출력
    print("Data committed to database")
    return jsonify({'message': 'Exercise data and diagnosis saved successfully'}), 200

if __name__ == '__main__':
    app.run(debug=True)
