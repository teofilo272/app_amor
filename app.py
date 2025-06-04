from flask import Flask, render_template, request, redirect, url_for, session
import os  # <<< ADICIONE ESTA LINHA AQUI!

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY') or 'minha_chave_local_padrao' # Use esta linha!

# Perguntas do Quiz
perguntas = [
    {
        'pergunta': 'Qual foi o nosso primeiro encontro?',
        'opcoes': ['Cafeteria', 'Parque', 'Cinema', 'Restaurante'],
        'resposta': 'Cafeteria'
    },
    {
        'pergunta': 'Qual é a sua comida favorita que eu cozinho?',
        'opcoes': ['Lasanha', 'Pizza caseira', 'Risoto', 'Massa com molho'],
        'resposta': 'Pizza caseira'
    },
    {
        'pergunta': 'Qual é a nossa música?',
        'opcoes': ['Thinking Out Loud', 'Perfect', 'All of Me', 'Outra'],
        'resposta': 'Perfect'
    },
    {
        'pergunta': 'Onde demos o nosso primeiro beijo?',
        'opcoes': ['Na porta da sua casa', 'No meu carro', 'Na balada', 'No cinema'],
        'resposta': 'Na porta da sua casa'
    },
    {
        'pergunta': 'Qual é o seu filme favorito para ver comigo?',
        'opcoes': ['Comédia romântica', 'Filme de ação', 'Terror', 'Animação'],
        'resposta': 'Comédia romântica'
    },
    {
        'pergunta': 'Qual a cor dos meus olhos?',
        'opcoes': ['Castanhos', 'Azuis', 'Verdes', 'Pretos'],
        'resposta': 'Castanhos'
    },
    {
        'pergunta': 'Qual é a nossa piada interna favorita?',
        'opcoes': ['A do pato', 'A do pinguim', 'A do tomate', 'Não temos uma'],
        'resposta': 'A do pato'
    },
    {
        'pergunta': 'Qual é o presente que eu mais gostei de te dar?',
        'opcoes': ['Viagem', 'Livro', 'Flor', 'Jóia'],
        'resposta': 'Viagem'
    },
    {
        'pergunta': 'Qual o nosso lugar favorito para passear?',
        'opcoes': ['Praia', 'Montanha', 'Cidade', 'Campo'],
        'resposta': 'Praia'
    },
    {
        'pergunta': 'Se pudéssemos viajar para qualquer lugar agora, qual seria?',
        'opcoes': ['Paris', 'Maldivas', 'Tóquio', 'Roma'],
        'resposta': 'Paris'
    }
]

@app.route('/')
def index():
    session['respostas'] = []
    session['pergunta_atual'] = 0
    return render_template('index.html')

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if 'respostas' not in session:
        session['respostas'] = []
        session['pergunta_atual'] = 0

    if request.method == 'POST':
        resposta_usuario = request.form['resposta']
        session['respostas'].append(resposta_usuario)
        session['pergunta_atual'] += 1
        if session['pergunta_atual'] >= len(perguntas):
            return redirect(url_for('resultado_quiz'))
        else:
            return redirect(url_for('quiz'))
    else:
        if session['pergunta_atual'] < len(perguntas):
            pergunta_atual = perguntas[session['pergunta_atual']]
            return render_template('quiz_pergunta.html', pergunta=pergunta_atual, numero_pergunta=session['pergunta_atual'] + 1, total_perguntas=len(perguntas))
        else:
            return redirect(url_for('resultado_quiz'))

@app.route('/resultado_quiz')
def resultado_quiz():
    acertos = 0
    resultados_detalhados = []
    for i, resposta_usuario in enumerate(session['respostas']):
        pergunta = perguntas[i]
        correto = (resposta_usuario == pergunta['resposta'])
        if correto:
            acertos += 1
        resultados_detalhados.append({
            'pergunta': pergunta['pergunta'],
            'sua_resposta': resposta_usuario,
            'resposta_correta': pergunta['resposta'],
            'correto': correto
        })
    return render_template('quiz_resultado.html', acertos=acertos, total=len(perguntas), resultados=resultados_detalhados)

@app.route('/declaracao')
def declaracao():
    return render_template('declaracao.html')

@app.route('/proximo_passo')
def proximo_passo():
    return render_template('proximo_passo.html')

@app.route('/musica')
def musica():
    youtube_link = "https://www.youtube.com/watch?v=dQw4w9WgXcQ" # ***Substitua pelo link da sua música!***
    return render_template('musica.html', youtube_link=youtube_link)

if __name__ == '__main__':
    app.run(debug=True)
