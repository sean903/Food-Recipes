# pip install streamlit
# import spacy 
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
# nlp = spacy.load("en_core_web_lg")
# from spacy.lang.en import English
from ast import literal_eval


sidebar_title = st.sidebar.header('Navigation')
navigation = st.sidebar.radio('',['Fushion Recipes', "What's left in the fridge?", 'Search recipes'])
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
            time.sleep(1)
        
        def query(payload):
            response = requests.post(API_URL, headers=headers, json=payload)
            return response.json()
            
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
            

if navigation == 'Fushion Recipes':
    
    cuisine_df = pd.read_csv('../data/cuisine.csv')
    cuisine_df2 = cuisine_df[cuisine_df['RecipeIngredientParts'].str.len() > 15 ].reset_index()
    
    option = st.selectbox(
     'Pick Cuisine 1',
     ('Chinese', 'Thai', 'Japanese', 'African', 'Indian'))
    
    option2 = st.selectbox(
     'Pick Cuisine 2',
     ('Chinese', 'Thai', 'Japanese', 'African', 'Indian'))
    
    option3= st.selectbox(
     'Pick Ingedient',
     ('chicken', 'fish', 'rice', 'pasta', 'cheese'))
       
    st.button('Create Fushion Recipe', key=None, help=None, on_click=None, args=None, kwargs=None)

    def list_convert(dataframe, column):
        for count, value in enumerate(dataframe[f'{column}']): 
    #         if dataframe[f'{column}'].str.contains('char'):
    #             dataframe[f'{column}'][count] = "NA"
            
            
            dataframe[f'{column}']= dataframe[f'{column}'][count].replace('c(', '')
            dataframe[f'{column}'][count] = dataframe[f'{column}'][count].replace(')', '')
            dataframe[f'{column}'][count] = dataframe[f'{column}'][count].replace('0', '')
            dataframe[f'{column}'][count] = dataframe[f'{column}'][count].replace('(', '')
            dataframe[f'{column}'][count] = dataframe[f'{column}'][count].replace('\n', '')
    #         dataframe[f'{column}'][count] = dataframe[f'{column}'][count].replace('character', '')
            
            dataframe[f'{column}'][count] = ast.literal_eval(str(dataframe[f'{column}'][count]))
            
            return dataframe
        
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
        list_convert(cuisine_sample.reset_index(), 'RecipeIngredientParts')
        list_convert(cuisine2_df.reset_index(), 'RecipeIngredientParts')
        
        ultimate_recipe5 = fushion_recipe(cuisine_sample, cuisine2_df)
        
        return ultimate_recipe5

    st.write(ultimate_recipe5)
