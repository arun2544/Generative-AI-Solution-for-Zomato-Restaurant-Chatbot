# # File: app.py
# from src.config import CSV_PATH, SYSTEM_PROMPT, EMBEDDING_MODEL
# from src.data_loader import load_and_preprocess_data
# from src.vector_db import RestaurantVectorDB
# from src.rag_pipeline import RAGSystem

# def main():
#     # Initialize system
#     df = load_and_preprocess_data(CSV_PATH)
    
#     # Build vector DB
#     vector_db = RestaurantVectorDB(EMBEDDING_MODEL)
#     vector_db.build_from_dataframe(df)
    
#     # Create RAG system
#     rag = RAGSystem(vector_db, SYSTEM_PROMPT)
    
#     # Example queries
#     queries = [
#         "Which restaurants in Tilak Nagar have high ratings?",
#         "What's the price range for Punjab Grill?",
#         "Does Molecule Air Bar have outdoor seating?"  # Out of scope
#     ]
    
#     for query in queries:
#         print(f"\nQuery: {query}")
#         print(f"Response: {rag.generate_response(query)}")

# if __name__ == "__main__":
#     main()


# # File: app.py
# import streamlit as st
# from src.data_loader import load_and_preprocess_data
# from src.vector_db import RestaurantVectorDB
# from src.config import EMBEDDING_MODEL, SYSTEM_PROMPT
# import pandas as pd

# # Custom CSS for Zomato-style styling
# st.markdown("""
# <style>
#     [data-testid=stAppViewContainer] {
#         background-color: #F8F8F8;
#         font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
#     }
#     .stChatInput {
#         background-color: #FFFFFF;
#         border-radius: 25px;
#         padding: 15px;
#     }
#     .stChatMessage {
#         border-radius: 15px;
#         box-shadow: 0 2px 4px rgba(0,0,0,0.1);
#     }
#     .restaurant-card {
#         border: 1px solid #E0E0E0;
#         border-radius: 12px;
#         padding: 15px;
#         margin: 10px 0;
#         background: white;
#     }
#     .rating-badge {
#         background-color: #E23744;
#         color: white;
#         padding: 2px 8px;
#         border-radius: 4px;
#         font-size: 0.8em;
#     }
# </style>
# """, unsafe_allow_html=True)

# # Initialize RAG system
# @st.cache_resource
# def initialize_system():
#     df = load_and_preprocess_data("data/restaurant_data.csv")
#     vector_db = RestaurantVectorDB(EMBEDDING_MODEL)
#     vector_db.build_from_dataframe(df)
#     return vector_db

# vector_db = initialize_system()

# # Chat UI Setup
# st.title("🍽️ Kanpur Restaurant Assistant")
# st.caption("Powered by Zomato Data | Ask about restaurants in Kanpur")

# # Initialize chat history
# if "messages" not in st.session_state:
#     st.session_state.messages = []

# # Display chat messages
# for message in st.session_state.messages:
#     with st.chat_message(message["role"]):
#         if message["role"] == "assistant":
#             if "restaurants" in message:
#                 for restaurant in message["restaurants"]:
#                     with st.container():
#                         st.markdown(f"""
#                         <div class='restaurant-card'>
#                             <div style="display:flex; gap:20px; align-items:center">
#                                 <img src="{restaurant['images']}" width="100" style="border-radius:8px">
#                                 <div>
#                                     <h3 style="margin:0">{restaurant['names']}</h3>
#                                     <div style="display:flex; gap:15px; align-items:center; margin:5px 0">
#                                         <span class="rating-badge">⭐ {restaurant['ratings']}</span>
#                                         <span>💰 {restaurant['price for one']}</span>
#                                     </div>
#                                     <p style="color:#666; margin:0">{restaurant['cuisine']}</p>
#                                     <p style="color:#E23744; margin:5px 0 0 0">
#                                         📍 {restaurant['location'].title()}
#                                     </p>
#                                 </div>
#                             </div>
#                         </div>
#                         """, unsafe_allow_html=True)
#             st.markdown(message["content"])
#         else:
#             st.markdown(message["content"])

# # Handle user input
# if prompt := st.chat_input("Ask about restaurants..."):
#     # Add user message to chat history
#     st.session_state.messages.append({"role": "user", "content": prompt})
    
#     # Display user message
#     with st.chat_message("user"):
#         st.markdown(prompt)

#     # Get RAG response
#     try:
#         results = vector_db.search(prompt, top_k=3)
#         response = f"Here are some restaurants that match your query:"
        
#         # Format restaurant cards
#         restaurant_cards = []
#         for res in results:
#             card = f"""
#             **{res['names']}**  
#             ⭐ {res['ratings']} | 💰 {res['price for one']}  
#             🍴 {res['cuisine']}  
#             📍 {res['location'].title()}
#             """
#             restaurant_cards.append(card)

#         # Add assistant response
#         with st.chat_message("assistant"):
#             st.markdown(response)
#             for card in restaurant_cards:
#                 card_html = card.replace('\n', '<br>')
#                 st.markdown(
#                     f"<div class='restaurant-card'>{card_html}</div>",
#                     unsafe_allow_html=True
#                 )

            
#         # Store response with restaurant data
#         st.session_state.messages.append({
#             "role": "assistant",
#             "content": response,
#             "restaurants": results
#         })

#     except Exception as e:
#         st.error(f"Error processing request: {str(e)}")


# File: app.py
import streamlit as st
from src.data_loader import load_and_preprocess_data
from src.vector_db import RestaurantVectorDB
from src.rag_pipeline import RAGSystem
from src.config import CSV_PATH, SYSTEM_PROMPT, EMBEDDING_MODEL

# Custom CSS for consistent styling
st.markdown("""
<style>
    [data-testid=stAppViewContainer] {
        background-color: #F8F8F8;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }
    .stChatInput {
        background-color: #FFFFFF;
        border-radius: 25px;
        padding: 15px;
        margin-top: 20px;
    }
    .stChatMessage {
        border-radius: 15px!important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1)!important;
    }
    [data-testid="stChatMessage"] {
        max-width: 80%;
    }
    [data-testid="stChatMessage"][aria-label="Posted by assistant"] {
        margin-left: 20%;
        background-color: #FFFFFF;
    }
    [data-testid="stChatMessage"][aria-label="Posted by user"] {
        margin-right: 20%;
        background-color: #E2374410;
    }
</style>
""", unsafe_allow_html=True)

# Initialize RAG system
@st.cache_resource
def initialize_rag():
    df = load_and_preprocess_data(CSV_PATH)
    vector_db = RestaurantVectorDB(EMBEDDING_MODEL)
    vector_db.build_from_dataframe(df)
    return RAGSystem(vector_db, SYSTEM_PROMPT)

rag_system = initialize_rag()

# Chat interface setup
st.title("🍽️ Kanpur Restaurant Assistant")
st.caption("Powered by Zomato Data | Ask about restaurants in Kanpur")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"], unsafe_allow_html=True)

# Process user input
if prompt := st.chat_input("Ask about restaurants..."):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get RAG response
    try:
        response = rag_system.generate_response(prompt)
        
        # Format response with Markdown
        formatted_response = response.replace('₹', '💰 ').replace('rating', '⭐')
        formatted_response = formatted_response.replace(' - ', '  \n• ')  # Line breaks for lists
        
        # Display assistant response
        with st.chat_message("assistant"):
            st.markdown(f"""
            <div style='line-height: 1.6;'>
                {formatted_response}
            </div>
            """, unsafe_allow_html=True)
        
        # Add to history
        st.session_state.messages.append({
            "role": "assistant",
            "content": formatted_response
        })
        
    except Exception as e:
        st.error(f"Error processing request: {str(e)}")


