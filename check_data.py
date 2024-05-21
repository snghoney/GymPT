import sqlite3

# 데이터베이스 파일 경로
db_path = 'data.sqlite'

# 데이터베이스 연결
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# User 테이블과 exercise_data 테이블 조인하여 모든 데이터 조회
query = """
SELECT 
    user.id, user.name, user.phone, 
    exercise_data.count, 
    exercise_data.left_forearm_innerbody, 
    exercise_data.left_forearm_outterbody, 
    exercise_data.right_forearm_innerbody, 
    exercise_data.right_forearm_outterbody
FROM 
    user
LEFT JOIN 
    exercise_data
ON 
    user.id = exercise_data.user_id
"""
cursor.execute(query)
combined_data = cursor.fetchall()

# 결합된 데이터 출력
print("Combined User and Exercise Data:")
for data in combined_data:
    print(f"User ID: {data[0]}, Name: {data[1]}, Phone: {data[2]}, Count: {data[3]}, "
          f"Left Forearm Inner Body: {data[4]}, Left Forearm Outter Body: {data[5]}, "
          f"Right Forearm Inner Body: {data[6]}, Right Forearm Outter Body: {data[7]}")

# 연결 종료
conn.close()
