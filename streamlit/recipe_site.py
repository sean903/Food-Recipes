# pip install streamlit
import streamlit as st
import pandas as pd
import numpy as np
import requests
import json
import time
import pickle
from pathlib import Path
import base64
from ast import literal_eval


sidebar_title = st.sidebar.header('Navigation')
navigation = st.sidebar.radio('',['Seans Fushion Recipes', "What's left in the fridge?", 'Search recipes'])
st.sidebar.markdown('''
<small>Summary of the [docs](https://docs.streamlit.io/en/stable/api.html), as of [Streamlit v1.0.0](https://www.streamlit.io/).</small>
    ''', unsafe_allow_html=True)


if navigation == "What's left in the fridge?":
    st.title("What's left in the fridge?")

    fridge_ingredients = st.text_input('Input ingredients followed by a comma and space', value="", max_chars=None, key=None, type="default", help=None, autocomplete=None, on_change=None, args=None, kwargs=None, placeholder='e.g. bacon, ham, cheese')

    API_TOKEN = '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'
    API_URL = "https://api-inference.huggingface.co/models/flax-community/t5-recipe-generation"
    headers = {"Authorization": f"Bearer {API_TOKEN}"}

    def query(payload):
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.json()

    if fridge_ingredients:
        with st.spinner('Creating your recipe...'):
            time.sleep(5)
            
        output = query({"inputs": fridge_ingredients})
        str_output = json.dumps(output)
        start_title = str_output.split(':', 2)[2]
        recipe_title = start_title.split('ingredients')[0]
        ingredient_list = start_title.split(':', 2)[1][:-10]
        instructions = start_title.split(':', 2)[2][:-3]
        
        st.header('Name: ' + recipe_title)
        st.subheader('Ingredients: ' + ingredient_list)
        st.markdown('Instructions: ' + instructions)
        
if navigation == 'Search recipes':
    recipes10_df = pd.read_csv('./data/recipes_clean_10k_df.csv')
    for count, value in enumerate(recipes10_df['RecipeIngredientParts']):
        recipes10_df['RecipeIngredientParts'][count] = literal_eval(recipes10_df['RecipeIngredientParts'][count])
    st.title('Search recipes')
    search_ingredients = st.text_input('Input ingredients followed by a comma and space', value="", max_chars=None, key=None, type="default", help=None, autocomplete=None, on_change=None, args=None, kwargs=None, placeholder='e.g. bacon, ham, cheese')
    
    if search_ingredients:
        def user_search(user_ingredients):
            for x in range(len(recipes10_df)):
                rand_ingred2 = recipes10_df['RecipeIngredientParts'][x]
                rand_ingred2_lower = [item.lower() for item in rand_ingred2]                # If second recipe has two matching ingredients with first recipe: combine them 
                if set(user_ingredients).issubset(set(rand_ingred2_lower)):
                    st.title(recipes10_df['Name'][x])
                    st.subheader(', '.join(recipes10_df['RecipeIngredientParts'][x]))
                    search_instructions = ''.join(recipes10_df['RecipeInstructions'][x])
                    st.markdown(search_instructions[2:-2].replace("'", ""))
                    
        user_search(search_ingredients.split(', '))    
            

def img_to_bytes(img_path):
    img_bytes = Path(img_path).read_bytes()
    encoded = base64.b64encode(img_bytes).decode()
    return encoded
       
# st.sidebar.markdown('''[<img src='data:image/png;base64,{}' class='img-fluid' width=32 height=32>](https://streamlit.io/)'''.format(img_to_bytes("logomark_website.png")), unsafe_allow_html=True)

