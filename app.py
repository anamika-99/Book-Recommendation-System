
#python -m streamlit run app.py
import streamlit as st
import pickle
import numpy as np
import pandas as pd

st.set_page_config(layout="wide")

st.title('Book Recommendation System\n')
top_ratings= pickle.load(open(r"C:/Users/Anamika/Documents/Python scripts/Project/top_ratings.pkl", "rb"))
data_m = pickle.load(open(r"C:/Users/Anamika/Documents/Python scripts/Project/data_m.pkl", "rb"))
similarity_score = pickle.load(open(r"C:/Users/Anamika/Documents/Python scripts/Project/sim_sc.pkl", "rb"))
pt=pickle.load(open(r"C:/Users/Anamika/Documents/Python scripts/Project/pivot.pkl", "rb"))

# with st.sidebar:
#     st.button("Show Popular Books")
#     st.button("Recommend Books")
    
def popular_books():
    book_names=data_m.sort_values('Score', ascending=False)['Book-Title'].unique()
    st.write(book_names[0:10])

if (st.button('Show Popular Books')):
    st.write("Top 10 popular book based on Ratings")
    popular_books()
    
 
def recommend(book):


    indi = np.where(pt.index == book)[0][0]
    similar_items = sorted(list(enumerate(similarity_score[indi])), key=lambda x: x[1], reverse=True)[1:10]

    data = []
    # name = []
    for i in similar_items:
        item = []
        # temp_df1 = book_list[book_list['Book-Title'] == pt.index[i[0]]]
        temp_df = top_ratings[top_ratings['Book-Title'] == pt.index[i[0]]]
        # name.extend(list(temp_df1.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

        data.append(item)
        df=pd.DataFrame(data)
    return df
    
books = top_ratings["Book-Title"].values

Users_book = st.selectbox('Select a books from drop down', books,index=None,
    placeholder="Select book...",key='l')
    

if(st.button('Recommend Books')):
    
   
   st.write('You selected:', Users_book)
   
   
   recommended_book=recommend(Users_book)
   col1, col2, col3 = st.columns(3)

   with col1:
           st.write("Book-Title")
           st.write(recommended_book[0])

   with col2:
           st.write("Book-Author")
           st.write(recommended_book[1])

   with col3:
           st.write("URL")
           st.markdown(recommended_book[2])
       
  
   idx = 0 
   for _ in range(len(recommended_book[2])-1):
       cols = st.columns(4) 
        
       if idx < len(recommended_book[2]): 
           cols[0].image(recommended_book[2][idx], width=150, caption=recommended_book[0][idx])
       idx+=1
        
       if idx < len(recommended_book[2]):
           cols[1].image(recommended_book[2][idx], width=150, caption=recommended_book[0][idx])
       idx+=1

       if idx < len(recommended_book[2]):
           cols[2].image(recommended_book[2][idx], width=150, caption=recommended_book[0][idx])
       idx+=1 
       if idx < len(recommended_book[2]): 
           cols[3].image(recommended_book[2][idx], width=150, caption=recommended_book[0][idx])
           idx = idx + 1
       else:
          break

  # Space out the maps so the first one is 2x the size of the other three
col1, col2, col3 = st.columns((1, 1, 3))
