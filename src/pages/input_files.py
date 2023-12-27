import streamlit as st
import os
import psycopg2

st.subheader('Input Files')

# Initialize connection.
conn = psycopg2.connect(database="stki",
                        host="stki-db",
                        user="stki",
                        password="stki123",
                        port="5432")

uploaded_file = st.file_uploader("Choose a file")

if uploaded_file is not None:

  name = st.text_input('Name')

  if name:

    url = st.text_input('Url')

    if url:
      
      # To read file as bytes:
      filename = abs(hash(uploaded_file.getvalue()))
      path = 'docs/{}.md'.format(filename)

      with open(path, 'wb') as f:
          f.write(uploaded_file.getvalue())
      
      df = conn.cursor()
      query = "INSERT INTO github (name, path, url) VALUES (%s,%s,%s)"    
      args = (name, path, url)
      
      try:
        cursor = conn.cursor()
        cursor.execute(query, args)
        conn.commit()
        
        st.success('Record added Successfully')
      
      except:
        os.remove(path)
        st.error('Record failed to add')