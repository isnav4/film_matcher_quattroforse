import pandas as pd
import kagglehub
import os
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


df = None
model = None
embeddings = None

def init_engine():
    """mo carico il database e preparo il modello all'avvio."""
    global df, model, embeddings
    print(" il modello : dammi un minute porfavor che carico il database...")
    
    try:
        
        path = kagglehub.dataset_download("harshitshankhdhar/imdb-dataset-of-top-1000-movies-and-tv-shows")
        csv_path = os.path.join(path, "imdb_top_1000.csv")
        daticsv = pd.read_csv(csv_path)
        
        
        df = daticsv[['Series_Title', 'Overview', 'Genre']].rename(
            columns={'Series_Title': 'titolo', 'Overview': 'trama', 'Genre': 'genere'}
        ).dropna()
        
        print(f" il modello : caricato il Database con ben: {len(df)} film.")

        
        print("il modello: ora procedo a caricare la mia incredibile rete neurale")
        model = SentenceTransformer('all-MiniLM-L6-v2')
        
        #
        print(" il modello : it's time to calcolare gli embeddingssss")
        embeddings = model.encode(df['trama'].tolist(), show_progress_bar=True)
        print(" il modello: now the sistema is pronto!")
        return True
    except Exception as e:
        print(f"il modello : NOOOOOOOOO , c'è un ERRORE critico: {e}")
        return False

def get_recommendation(user_query):
    """quando RICEVO il testo dell' utente -> RESTITUISCO poi il film consigliato"""
    if df is None or model is None:
        return {"error": "aspetta che non sono pronto."}

    
    query_vec = model.encode([user_query])
    

    scores = cosine_similarity(query_vec, embeddings)[0]
    
   
    id_film = scores.argmax()
    alto_score = scores[id_film]
    
    film = df.iloc[id_film]
    
    
    if alto_score < 0.29:
        return {"found": False}
    
    return {
        "found": True,
        "titolo": film['titolo'],
        "trama": film['trama'],
        "genere": film['genere'],
        "score": str(round(alto_score, 2))
    }