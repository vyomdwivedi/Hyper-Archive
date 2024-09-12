import streamlit as st  #pip install streamlit
import pyrebase  #pip install pyrebase4
from datetime import datetime  #pip install datetime
import app  #Importing the app.py file



# ---STREAMLIT CONFIGURATION---
st.set_page_config(page_title='Hyper Archive Tool', page_icon=':floppy_disk:', layout='centered', initial_sidebar_state='auto')
st.title('Hyper Archive Tool')



# ---FIREBASE CONFIGURATION---
firebaseConfig = {
  'apiKey': "AIzaSyB7PC8cpDxNJ_9XnJBdZ3B6ltssIapryDc",
  'authDomain': "hyper-archive.firebaseapp.com",
  'projectId': "hyper-archive",
  'databaseURL': "https://console.firebase.google.com/project/hyper-archive/database/hyper-archive-default-rtdb/data/~2F",
  'storageBucket': "hyper-archive.appspot.com",
  'messagingSenderId': "156682157980",
  'appId': "1:156682157980:web:de90d0ca7eee35f8861259",
  'measurementId': "G-DN1H547D6D"
}



# ---FIREBASE AUTHENTICATION---
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()



# ---FIREBASE DATABASE---
db = firebase.database()
storage = firebase.storage()



# ---FIREBASE AUTHENTICATION---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if st.session_state.logged_in:
    app.main()  # Calling the main() from app.py
else:
    choice = st.selectbox('Choose Action', ['Sign Up', 'Login'])

    if choice == 'Sign Up':
        name = st.text_input('Name')
        email = st.text_input('Email')
        st.session_state.email = email
        password = st.text_input('Password', type='password')
        if st.button('Sign Up'):
            try:
                user = auth.create_user_with_email_and_password(email, password)
                st.success('User created successfully')
                db.child('users').child(user['localId']).child('email').set(email)
                db.child('users').child(user['localId']).child('password').set(password)
                db.child('users').child(user['localId']).child('created_at').set(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            except Exception as e:
                st.error("Email already exists")

    elif choice == 'Login':
        email = st.text_input('Email')
        st.session_state.email = email
        password = st.text_input('Password', type='password')
        if st.button('Login'):
            try:
                user = auth.sign_in_with_email_and_password(email, password)
                st.success('Logged in successfully')
                st.warning('Please click on the Login button to continue')
                st.session_state.logged_in = True
                st.experimental_set_query_params(logged_in=True)  # Set query param to trigger rerun
            except Exception as e:
                st.error("Invalid email or password")
                st.error(e)
