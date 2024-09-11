#Modules
import streamlit as st
import pyrebase
from datetime import datetime



#Firebase Config
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

#Firebase Authentication
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

#Firebase Database
db = firebase.database()
storage = firebase.storage()

st.title('Hyper Archive')
choice = st.selectbox('Select an option', ['Login', 'SignUp'])

if choice == 'SignUp':
    email = st.text_input('Email')
    password = st.text_input('Password', type='password')
    if st.button('SignUp'):
        try:
            user = auth.create_user_with_email_and_password(email, password)
            st.success('User created successfully')
            db.child('users').child(user['localId']).child('email').set(email)
            db.child('users').child(user['localId']).child('password').set(password)
            db.child('users').child(user['localId']).child('created_at').set(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        except Exception as e:
            st.error(e)

elif choice == 'Login':
    email = st.text_input('Email')
    password = st.text_input('Password', type='password')
    if st.button('Login'):
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            st.success('Logged in successfully')
            st.write('User ID:', user['localId'])
        except Exception as e:
            st.error(e)