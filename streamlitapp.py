import streamlit as st
from pymongo import MongoClient
from bertopic import BERTopic
from umap import UMAP
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

load_dotenv()

def load_data():
    try:
        client = MongoClient(st.secrets["MONGO_URI"])
        db = client[st.secrets["PROFESSOR_DB"]]
        collection = db[st.secrets["PAPER_POOL"]]
        
        pipeline = [{'$project': {'_id': 0, 'passage': {'$concat': ['$title', ' ', '$description']}}}]
        results = collection.aggregate(pipeline)
        return [doc['passage'] for doc in results]
    except Exception as e:
        st.error(f"Database connection failed: {e}")
        return []

def main():
    st.title("Academic Paper Topic Modeling")
    
    with st.status("Loading data..."):
        content = load_data()
        if not content:
            st.warning("No documents found in collection")
            return
        
    with st.status("Generating embeddings..."):
        sentence_model = SentenceTransformer("all-MiniLM-L6-v2")
        embeddings = sentence_model.encode(content, show_progress_bar=False)
    
    with st.status("Training topic model..."):
        topic_model = BERTopic()
        topics = topic_model.fit(content, embeddings=embeddings)
    
    tab1, tab2, tab3 = st.tabs(["Topic Visualization", "Heatmap", "Document Map"])
    
    # In your tab section:
    with tab1:
        fig = topic_model.visualize_topics()
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        fig = topic_model.visualize_heatmap()
        st.plotly_chart(fig, use_container_width=True)

    with tab3:
        reducer = UMAP(n_neighbors=10, n_components=2, min_dist=0.0, metric='cosine')
        reduced_embeds = reducer.fit_transform(embeddings)
        fig = topic_model.visualize_documents(content, reduced_embeddings=reduced_embeds)
        st.plotly_chart(fig, use_container_width=True)


if __name__ == "__main__":
    main()
