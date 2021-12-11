
<div style="text-align:center"><img src="fushion_recipes.png" /></div>

#### Problem Statement

It is difficult to combine recipes from different cuisines and come up with a good tasting recipe.

#### SUMMARY 

It is possible to create nice tasting recipes create fushion recipes using data science. However, there are occasions where the model produces recipes which humans would not like to taste.

A few models were tested but the best performing model was built using the Spacy library.

#### DATA ANALYSIS
![alt text](./images/ratings_time.jpg)
![alt text](./images/recipe_ingredients.jpg)
#### FUTURE DEVELOPMENTS
Categorise ingredients into core components, split foods into carbs, proteins, veg and different spices. This would allow for recipes to be created with nice balance to them. For example, you would only be given one carb, one protein, two veg and a selection of spiciers.

Cluster recipes by  ingredients, to find out what are some common ingredient combinations.

Optimize run time. As the application you saw on streammlit is only running a model from a small dataset, when this gets increased to 500 thousand recipes it can take some time.  


#### DATA SOURCES
[Original Recipes Dataset](https://www.kaggle.com/shuyangli94/food-com-recipes-and-user-interactions?select=RAW_recipes.csv)

#### DATA DICTIONARY
*The final dataset uses the following data dictionary:*

| Feature        	    | Type   	| Description                                                                                                      	|
|-------------------	|--------	|------------------------------------------------------------------------------------------------------------	|
| RecipeIngredientParts | object  	| All the ingredients for the recipe                                                                      	|
| RecipeCategory   	| object 	| The type of cuisine/category the recipe is e.g. Indian                                  	|
| Name     	| object 	| The name of the recipe
| CookTime   	| float  	| The time it takes to cook the recipe    