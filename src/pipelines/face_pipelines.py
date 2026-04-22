import dlib
import numpy as np
import face_recognition_models
from src.database.db import get_all_students
import streamlit as st
from sklearn.svm import SVC
from collections import defaultdict

@st.cache_resource
def load_dlib_models():
    detector = dlib.get_frontal_face_detector()

    sp = dlib.shape_predictor(
        face_recognition_models.pose_predictor_model_location()
    )

    face_rec = dlib.face_recognition_model_v1(
        face_recognition_models.face_recognition_model_location()
    )

    return detector, sp, face_rec

def get_face_emb(np_image):
    detector, sp, face_rec = load_dlib_models()
    faces = detector(np_image,1)

    encoding = []

    for face in faces:
        shape = sp(np_image, face)
        face_des = face_rec.compute_face_descriptor(np_image, shape, 1) #128 embddings

        encoding.append(np.array(face_des))

    return encoding

@st.cache_resource
def get_trained_model():
    X = []
    y = []

    student_db = get_all_students()

    if not student_db:
        return None
    for student in student_db:
        embedding = student.get('face_embedding')
        if embedding:
            X.append(np.array(embedding))
            y.append(student.get('student_id'))

    if len(X) ==0:
        return 0
    
    clf = SVC(kernel = 'linear', probability = True, class_weight = 'balanced')

    try:
       clf.fit(X, y)
    except Exception as e:
        print("Training error:", e)
        return None

    return {'clf': clf, 'X':X, 'y': y}
def trained_classifier():
    st.cache_resource.clear()
    model_data = get_trained_model()
    return bool(model_data)

def predict_attendance(class_img_np):
    encodings = get_face_emb(class_img_np)

    detected_student = {}
    
    model_data = get_trained_model()

    if not model_data:
        return detected_student, [], len(encodings)
    
    clf = model_data['clf']
    X_train = model_data['X']
    y_train = model_data['y']

    all_students = sorted(list(set(y_train)))

    for encoding in encodings:
        if len(all_students)>=2:
            predicted_id = int(clf.predict([encoding])[0])
        else:
            predicted_id = int(all_students[0])

        stu_emb = X_train[y_train.index(predicted_id)]
        
        best_match_score = np.linalg.norm(stu_emb - encoding)
        threshold = 0.6

        if best_match_score < threshold:
            detected_student[predicted_id] = True
    return detected_student, all_students, len(encodings)      





    
