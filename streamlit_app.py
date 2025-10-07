# Import packages
import streamlit as st
from snowflake.snowpark.functions import col

# App title
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie!")

# User input
name_on_order = st.text_input('Name on Smoothie:')

# Connect to Snowflake
cnx = st.connection("snowflake")
session = cnx.session()

# ✅ Make sure the column name matches exactly: "FRUIT_NAME"
try:
    fruit_df = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME"))
    fruit_options = [row["FRUIT_NAME"] for row in fruit_df.collect()]
except Exception as e:
    st.error("🚨 Failed to fetch fruit options. Check your table and column names in Snowflake.")
    st.exception(e)
    st.stop()

# Ingredient selection (max 5)
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    fruit_options,
    max_selections=5
)

# Submit button logic
if ingredients_list and name_on_order:
    ingredients_string = ', '.join(ingredients_list)
    insert_sql = f"""
        INSERT INTO smoothies.public.orders (ingredients, name_on_order)
        VALUES ('{ingredients_string}', '{name_on_order}')
    """

    if st.button("Submit Order"):
        try:
            session.sql(insert_sql).collect()
            st.success(f"✅ Your Smoothie is ordered, {name_on_order}!")
        except Exception as e:
            st.error("🚨 Failed to submit order.")
            st.exception(e)
