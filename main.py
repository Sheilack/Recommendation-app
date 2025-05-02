import streamlit as st
import pandas as pd
import ast

st.title("Market Basket Recommendation system")
st.markdown("Select an item to see frequently bought-together recommendations!")

# Load association rules

@st.cache_data
def load_rules():
    rules = pd.read_csv("association_rules.csv")
    def safe_eval(val):
      try:
        result = ast.literal_eval(val)
        if isinstance(result, (set, list, tuple)) and all(isinstance(x, str) for x in result):
            return set(result)
        return set()
      except (ValueError, SyntaxError, TypeError):
        return set()  
      
    rules['antecedents'] = rules['antecedents'].apply(safe_eval)
    rules['consequents'] = rules['consequents'].apply(safe_eval)
    return rules

rules = load_rules()

st.write("Sample antecedents:", rules['antecedents'].head())


# 👇 Only include non-empty sets
items = sorted({item for s in rules['antecedents'] if s for item in s})

st.write("Total items loaded into dropdown:", len(items))  # debug

# Build dropdown list
items = sorted({item for s in rules['antecedents'] if s for item in s})

# User input and Dropdown input

name = st.text_input("Enter your name:")
selected = st.selectbox("Choose an item:", items, key="item_selector")

# selected = st.selectbox("Choose an item:", items)

# Filter rules where the selected item is in antecedents

recommendations = rules[rules['antecedents'].apply(lambda x: selected in x)]

if not recommendations.empty:
    st.subheader("🧾 Recommendations:")
    for _, row in recommendations.iterrows():
        suggested = ", ".join(row['consequents'])
        st.markdown(f"**{suggested}** (Confidence: {row['confidence']:.2f}, Lift: {row['lift']:.2f})")
else:
    st.warning("No recommendations found for this item.")


# Optional extras
st.markdown("---")
st.caption("Made with ❤️ using Streamlit")
