# pip install streamlit
import spacy 
import re
import ast
import streamlit as st
import pandas as pd
import numpy as np
import requests
import json
import time
from sklearn.feature_extraction.text import CountVectorizer
import pickle
from pathlib import Path
import base64
from ast import literal_eval
# from spacy.lang.en import English

# cache - and put in function
# nlp = spacy.load("en_core_web_lg")

st.sidebar.image("./images/fusion_recipes.png", width = 300)
sidebar_title = st.sidebar.header('Navigation')
navigation = st.sidebar.radio('',['Fusion Recipes', "What's left in the fridge?", 'Search recipes'])



if navigation == "What's left in the fridge?":
    st.title("What's left in the fridge?")

    fridge_ingredients = st.text_input('Input ingredients followed by a comma and space', value="")

    def query(payload):
            API_TOKEN = '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'
            API_URL = "https://api-inference.huggingface.co/models/flax-community/t5-recipe-generation"
            headers = {"Authorization": f"Bearer {API_TOKEN}"}
            response = requests.post(API_URL, headers=headers, json=payload)
            return response.json()

    if fridge_ingredients:
        # spinner
        output = query({"inputs": fridge_ingredients})
        str_output = json.dumps(output)
        start_title = str_output.split(':', 2)[2]
        recipe_title = start_title.split('ingredients')[0]
        ingredient_list = start_title.split(':', 2)[1][:-10]
        try:
            instructions = start_title.split(':', 2)[2][:-3]
            st.header('Name: ' + recipe_title)
            st.subheader('Ingredients: ' + ingredient_list)
            st.markdown('Instructions: ' + instructions)
        except:
            st.warning('Sorry - I could not generate a new recipe based on the ingredients you have selected. PLEASE TRY AGAIN')

        
    
        
if navigation == 'Search recipes':
    
    @st.cache  
    def read_recipes():
        recipes10_df = pd.read_csv('./data/recipes_clean_10k_df.csv')
        for count, value in enumerate(recipes10_df['RecipeIngredientParts']):
            recipes10_df['RecipeIngredientParts'][count] = literal_eval(recipes10_df['RecipeIngredientParts'][count])
        return recipes10_df
    
    st.title('Search recipes')
    search_ingredients = st.text_input('Input ingredients followed by a comma and space', value="", max_chars=None, key=None, type="default")
    
    if search_ingredients:

        def user_search(user_ingredients):
            recipes10_df =read_recipes()
            for x in range(len(recipes10_df)):
                rand_ingred2 = recipes10_df['RecipeIngredientParts'][x]
                rand_ingred2_lower = [item.lower() for item in rand_ingred2]                # If second recipe has two matching ingredients with first recipe: combine them 
                if set(user_ingredients).issubset(set(rand_ingred2_lower)):
                    st.title(recipes10_df['Name'][x])
                    st.subheader(', '.join(recipes10_df['RecipeIngredientParts'][x]))
                    search_instructions = ''.join(recipes10_df['RecipeInstructions'][x])
                    st.markdown(search_instructions[2:-2].replace("'", ""))
                    
        user_search(search_ingredients.split(', '))    
            

if navigation == 'Fushion Recipes':
    
    nlp = spacy.load("en_core_web_sm")
    
    option = st.selectbox(
     'Pick Cuisine 1',
     ('Chinese', 'Thai', 'Japanese', 'African', 'Indian'))
    
    option2 = st.selectbox(
     'Pick Cuisine 2',
     ('African', 'Thai', 'Japanese', 'African', 'Indian'))
    
    option3= st.selectbox(
     'Pick Ingedient',
     ('chicken', 'fish', 'rice', 'cheese', 'salt'))
       
    cuisine_df = pd.read_csv('data/cuisine.csv')
    cuisine_df2 = cuisine_df[cuisine_df['RecipeIngredientParts'].str.len() > 15 ].reset_index(drop = True)
        
    def fushion_recipe(X1, X2):
        x1_recipe = str(X1['RecipeIngredientParts'][:1])

        vectorizer = CountVectorizer()
            # X1_vect = vectorizer.fit_transform(X1['RecipeIngredientParts'])
        X2_vect = vectorizer.fit_transform(X2['RecipeIngredientParts'])

        similarity_score = []

        for row in X2['RecipeIngredientParts']:
            score = nlp(x1_recipe).similarity(nlp(str(row)))
            similarity_score.append(score)

        best_match = max(range(len(similarity_score)), key=similarity_score.__getitem__)
        worst_match = min(range(len(similarity_score)), key=similarity_score.__getitem__)

        cuisine2_bmatch = X2['RecipeIngredientParts'][best_match:best_match+1]
        cuisine2_wmatch = X2['RecipeIngredientParts'][worst_match:worst_match+1]

        ultimate_recipe = cuisine2_bmatch.values[0] + X1['RecipeIngredientParts'].values[0]
        ultimate_recipe2 = ultimate_recipe.split(',')

        ultimate_recipe3 = [re.sub(r"[-()\"#/@;:<>{}`+=~|.!?,]", "", file) for file in ultimate_recipe2]
        ultimate_recipe4 = set(ultimate_recipe3)
        
        return ultimate_recipe4
    
    def filter_recipes(cuisine1, cuisine2, ingredient):
    
        # Filter by cuisine and ingredient
        cuisine1_df = cuisine_df[(cuisine_df['RecipeCategory'].str.contains(f'{cuisine1}')) & (cuisine_df['RecipeIngredientParts'].str.contains(f'{ingredient}'))]
        cuisine2_df = cuisine_df[(cuisine_df['RecipeCategory'].str.contains(f'{cuisine2}')) & (cuisine_df['RecipeIngredientParts'].str.contains(f'{ingredient}'))]
        
        # Get the sample for cuisne 1
    #     cuisine1_df = cuisine1_df.reset_index()
        cuisine_sample = cuisine1_df.sample(n=1)

    #     Call function to clean data
        # list_convert(cuisine_sample.reset_index(), 'RecipeIngredientParts')
        # list_convert(cuisine2_df.reset_index(), 'RecipeIngredientParts')
        
        ultimate_recipe5 = fushion_recipe(cuisine_sample, cuisine2_df)
        list_recipe = list(ultimate_recipe5)
        
        for ingredient_best in list_recipe[:14]:
            st.write(ingredient_best)
        
    if st.button('Create Fushion Recipe', key=None, help=None, on_click=None, args=None, kwargs=None):
        st.header('Ingredients: ')
        filter_recipes(option, option2, option3)
    


