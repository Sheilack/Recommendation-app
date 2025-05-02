import streamlit as st
import pandas as pd

st.title("Market Basket Recommendation system")
st.markdown("Select an item to see frequently bought-together recommendations!")

# Load rules

@st.cache_data
def load_rules():
    rules = pd.read_csv("association_rules.csv")
    rules['antecedents'] = rules['antecedents'].apply(eval).apply(set)
    rules['consequents'] = rules['consequents'].apply(eval).apply(set)
    return rules

rules = load_rules()

# user input and a dropdown list from antecedents

name = st.text_input("Enter your name:")
items = sorted({item for s in rules['antecedents'] if s for item in s})
st.write("Total items loaded into dropdown:", len(items))  # DEBUG
selected = st.selectbox("Choose an item:", items, key="item_selector")

# Show recommendations

if selected:
    recommendations = rules[rules['antecedents'].apply(lambda x: selected in x)]

    if not recommendations.empty:
        st.subheader("🧾 Recommended Items:")
        for _, row in recommendations.iterrows():
            suggested = ", ".join(row['consequents'])
            st.markdown(f"**{suggested}** (Confidence: {row['confidence']:.2f}, Lift: {row['lift']:.2f})")
    else:
        st.warning("No recommendations found for this item.")
