from sentence_transformers import SentenceTransformer, util
import streamlit as st

@st.cache_data
def load_model():
  return SentenceTransformer('all-MiniLM-L6-v2')

# Use model
model = load_model()

def similarity(key):
  
  #Encode all sentences
  embeddings = model.encode(sentences)

  key_embedding = model.encode(key)

  # #Compute cosine similarity between all pairs
  cos_sim = util.cos_sim(embeddings, key_embedding)

  all_sentence_combinations = []
  for i in range(len(cos_sim)):
    all_sentence_combinations.append([cos_sim[i], i])

  #Sort list by the highest cosine similarity score
  all_sentence_combinations = sorted(all_sentence_combinations, key=lambda x: x[0], reverse=True)

  print("Top-5 most similar pairs:")
  for score, i in all_sentence_combinations[0:5]:
    st.write("{} \t {}".format(cos_sim[i], sentences[i]))

st.subheader('Raw data')

key = st.text_input('Keyword')

# Sentence example
sentences = [
          'A man is eating a piece of bread.',
          'The girl is carrying a baby.',
          'A man is riding a horse.',
          'A woman is playing violin.',
          'Two men pushed carts through the woods.',
          'A man is riding a white horse on an enclosed ground.',
          'A monkey is playing drums.'
          ]

st.write(sentences)

if key:
  similarity(key)