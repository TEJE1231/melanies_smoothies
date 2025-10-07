# Import required packages
import streamlit as st
from snowflake.snowpark.functions import col

# App UI
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie!")

# Input: Name on the smoothie
name_on_order = st.text_input('Name on Smoothie:')

# Connect to Snowflake
try:
    cnx = st.connection("snowflake")
    session = cnx.session()

    # Load fruit options from Snowflake
    fruit_df = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME"))
    fruit_options = [row["FRUIT_NAME"] for row in fruit_df.collect()]
except Exception as e:
    st.error("🚨 Could not connect to Snowflake or fetch fruit options.")
    st.exception(e)
    st.stop()

# Let user pick ingredients
ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    fruit_options,
    max_selections=5
)

# Handle submission
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
            st.error("❌ Failed to submit order to Snowflake.")
            st.exception(e)
