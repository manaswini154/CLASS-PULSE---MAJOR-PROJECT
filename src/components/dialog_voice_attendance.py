import streamlit as st
from src.pipelines.voice_pipelines import process_bulk_audio
from src.database.config import supabase
from datetime import datetime
import pandas as pd
from src.components.dialog_attendance_result import show_attendance_result

@st.dialog("Voice Attendance")

def voice_attendance_dialog(selected_subject_id):
    st.write("Record auido of Students and submit. AI will recognise!")

    audio_data = None

    audio_data = st.audio_input("Record audio for attendance", key = 'attendance_audio')
    if st.button("Analyse audio", width= 'stretch', type = 'primary', icon=":material/mic:"):
        with st.spinner("Processing audio, please wait..."):
            enrolled_res = supabase.table('subject_students').select('*, students(*)').eq('subject_id', selected_subject_id).execute()
            enrolled_students = enrolled_res.data

            if not enrolled_students:
                st.warning("No students enrolled in this subject!")
                return
            
            candidates_dict ={
                s['students']['student_id']: s['students']['voice_embedding'] for s in enrolled_students if s['students'].get('voice_embedding') 
                }
            if not candidates_dict:
                st.error("No enrolled studetns have voice profiles registered! Voice attendance can not be processed!")
                return
            
            if audio_data is not None:
                audio_bytes = audio_data.read()
            else:
                st.warning("Please upload or record audio first.")
                return

            detected_scores  =process_bulk_audio(audio_bytes, candidates_dict)
            results,attendance_to_log = [],[]
            current_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            for node in enrolled_students:
                student = node['students']
                score = detected_scores.get(student['student_id'], 0.0)
                is_present = bool(score > 0.7)  # Assuming a threshold of 0.7 for attendance
                results.append({"Name": student['name'], "ID": student['student_id'], "Source" : score if is_present else '-', "Status": "✅ Present" if is_present else "❌ Absent"})
                attendance_to_log.append({'student_id': student['student_id'], 'subject_id': selected_subject_id, 'timestamp': current_timestamp, 'is_present': bool(is_present)})
        
            st.session_state.voice_attendance_results = (pd.DataFrame(results),attendance_to_log)

    if st.session_state.get('voice_attendance_results'):
        st.divider()
        df_results, logs = st.session_state.voice_attendance_results
        show_attendance_result(df_results, logs)
