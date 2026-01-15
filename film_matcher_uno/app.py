from flask import Flask, render_template, request, jsonify
import model
import csv                 
import os                   
from datetime import datetime 

app = Flask(__name__)
model.init_engine()


file_x_feedbakc_utwnti = 'dataset_feedback.csv'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    dati_json = request.json
    frase_utente = dati_json.get('msg', '')
    
    if not frase_utente:
        return jsonify({"risposta": "Devi scrivere almeno una parolaaaaa!"})
    
    risultato = model.get_recommendation(frase_utente)
    
    if risultato.get("error"):
        html_response = "<div class='msg bot error'>c'è stato un errrore del server.</div>"
    elif not risultato["found"]:
        html_response = "<div class='msg bot'>non ho trovato film con queste caratteristiche.</div>"
    else:
        
        html_response = f"""
        <div class='movie-card'>
            <h3> {risultato['titolo']}</h3>
            <span class='badge'>{risultato['genere']}</span>
            <p>{risultato['trama']}</p>
            <small>punteggio di rilevanza: {risultato['score']}</small>
            
            <div class='feedback-buttons'>
                <span class='feedback-text'>Che ne pensi?</span>
                <button class='btn-vote up' onclick='vote("POS", "{risultato['titolo']}", "{frase_utente}", this)'>👍( bel consiglio )</button>
                <button class='btn-vote down' onclick='vote("NEG", "{risultato['titolo']}", "{frase_utente}", this)'>👎( non ci siamo )</button>
            </div>
        </div>
        """
    
    return jsonify({"risposta": html_response})


@app.route('/feedback', methods=['POST'])
def feedback():
    informazioni = request.json
    
    
    file_nuovo = os.path.isfile(file_x_feedbakc_utwnti)
    
    with open(file_x_feedbakc_utwnti, mode='a', newline='', encoding='utf-8') as file:
        scritt = csv.writer(file)
       
        if not file_nuovo:
            scritt.writerow(['Data', 'Query_Utente', 'Film_Consigliato', 'Voto'])
            
        scritt.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            informazioni['query'],
            informazioni['film'],
            informazioni['voto']
        ])
        print("DEBUG: Feedback salvato correttamente.")
        
    return jsonify({"status": "ok appost"})

if __name__ == '__main__':
    app.run(debug=True)