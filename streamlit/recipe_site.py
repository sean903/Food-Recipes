# pip install streamlit
import streamlit as st
import pandas as pd
import numpy as np
import requests
import json
import time
import pickle

# recipes10_df = pd.read_pickle(r"./data/recipes_clean_10k")

navigation = st.sidebar.radio("Navigation", ['Seans Fushion Recipes', "What's left in the fridge?", 'Search recipes'])

if navigation == "What's left in the fridge?":
    st.title("What's left in the fridge?")

    ingredients = st.text_input('Input ingredients followed by a comma and space', value="", max_chars=None, key=None, type="default", help=None, autocomplete=None, on_change=None, args=None, kwargs=None, placeholder='e.g. bacon, ham, cheese')

    API_TOKEN = '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'
    API_URL = "https://api-inference.huggingface.co/models/flax-community/t5-recipe-generation"
    headers = {"Authorization": f"Bearer {API_TOKEN}"}

    def query(payload):
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.json()

    if ingredients:
        with st.spinner('Creating your recipe...'):
            time.sleep(5)
            
        output = query({"inputs": ingredients})
        str_output = json.dumps(output)
        start_title = str_output.split(':', 2)[2]
        recipe_title = start_title.split('ingredients')[0]
        ingredient_list = start_title.split(':', 2)[1][:-10]
        instructions = start_title.split(':', 2)[2][:-3]
        
        st.header(recipe_title)
        st.subheader(ingredient_list)
        st.markdown(instructions)
        
if navigation == 'Search recipes':
    st.title('Search recipes')
    ingredients = st.text_input('Input ingredients followed by a comma and space', value="", max_chars=None, key=None, type="default", help=None, autocomplete=None, on_change=None, args=None, kwargs=None, placeholder='e.g. bacon, ham, cheese')
    
    # def user_search(user_ingredients):
    
    #     for x in range(len(recipes10_df)):
    #         rand_ingred2 = recipes10_df['RecipeIngredientParts'][x]
    #         rand_ingred2_lower = [item.lower() for item in rand_ingred2]
    #         # If second recipe has two matching ingredients with first recipe: combine them 
    #         if set(user_ingredients).issubset(set(rand_ingred2_lower)):
    #             return print(recipes10_df['Name'][x]), recipes10_df['RecipeIngredientParts'][x]
    #     else:
    #         return 'No ingredients match with chosen ingredients'