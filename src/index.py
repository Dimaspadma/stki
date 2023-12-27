from sentence_transformers import SentenceTransformer, util
import streamlit as st
import os

@st.cache_data
def load_model():
  return SentenceTransformer('all-MiniLM-L6-v2')

# Use model
model = load_model()

file_name = {}
file_url = {}

# List all file in docs folder
# then read all text file
# return to dictionary
def read_file():
  conn = st.connection("postgresql", type="sql")
  df = conn.query('SELECT * FROM github;', ttl="0")

  file_dict = {}
  for row in df.itertuples():

    file_url[row.id] = row.url
    file_name[row.id] = row.name

    with open(row.path, 'r') as f:
      file_dict[row.id] = f.read()
  return file_dict

# loop file_dict from read_file() function
# print all file name
# then print all file content
def show_file(files):
  for file in files:
    st.write(file)

def similarity(key, files):

  # turn dictionary to list
  sentences = list(files.values())

  if len(sentences) <= 0:
    st.error('No file uploaded')
    return
  
  #Encode all sentences
  embeddings = model.encode(sentences)

  key_embedding = model.encode(key)

  # #Compute cosine similarity between all pairs
  cos_sim = util.cos_sim(embeddings, key_embedding)

  all_sentence_combinations = []
  for i in range(len(cos_sim)):
    all_sentence_combinations.append([cos_sim[i], i, ])

  #Sort list by the highest cosine similarity score
  all_sentence_combinations = sorted(all_sentence_combinations, key=lambda x: x[0], reverse=True)

  print("Top-5 most similar pairs:")
  for score, i in all_sentence_combinations[0:5]:
    st.markdown("[{}]({})".format(file_name[list(files.keys())[i]], file_url[list(files.keys())[i]]))

st.subheader('Raw data')
# show_file(files)

key = st.text_input('Keyword')

if key:
  files = read_file()
  similarity(key, files)