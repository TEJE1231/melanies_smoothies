# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# App title
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie!")

# Input for smoothie name
name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your smoothie will be:', name_on_order)

# Connect to Snowflake
cnx = st.connection("snowflake")
session = cnx.session()

# Get fruit options from Snowflake table
fruit_table = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME"))
fruit_options = [row["FRUIT_NAME"] for row in fruit_table.collect()]

# Ingredient selection
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    fruit_options,
    max_selections=5
)

# If ingredients are selected, show a submit button
if ingredients_list and name_on_order:
    ingredients_string = ', '.join(ingredients_list)  # More readable
    insert_sql = f"""
        INSERT INTO smoothies.public.orders (ingredients, name_on_order)
        VALUES ('{ingredients_string}', '{name_on_order}')
    """

    if st.button('Submit Order'):
        session.sql(insert_sql).collect()
        st.success(f'✅ Your Smoothie is ordered, {name_on_order}!')
