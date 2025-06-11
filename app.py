from flask import Flask, render_template, request, redirect, url_for, session
import os  # <<< ADICIONE ESTA LINHA AQUI!

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY') or 'minha_chave_local_padrao' # Use esta linha!

# Perguntas do Quiz
perguntas = [
     {
        'pergunta': 'Qual foi a primeira vez que sentimos uma tensão rolando entre nós?',
        'opcoes': ['Pico do Urubu (Maio 2024)', 'For Save 2024', 'Chácara no aniversário do meu pai', 'No teatro do ZOE'],
        'resposta': 'No teatro do ZOE'
    },
    {
        'pergunta': 'Qual frase eu usei pra tentar te provocar no ZOE?',
        'opcoes': ['Não estou afim de ninguém por enquanto', 'Não tem nenhuma menina bonita nesse zoe', 'A minha eposa é a mulher mais linda desse mundo, só não sei quem é ainda (olhando pra você)', 'To querendo namorar, mas só daqui 2 anos '],
        'resposta': 'A minha eposa é a mulher mais linda desse mundo, só não sei quem é ainda (olhando pra você)'
    },
    {
        'pergunta': 'Quantos meses depois do nosso primeiro beijo que começamos a namorar?',
        'opcoes': ['6 meses, pra dar tempo de se conhecer bastante', '3 meses, pra ver se realmente o sentimento era real', '2 meses, pra nos adaptarmos um ao outro e entender as intenções', '1 mês, porque sim.'],
        'resposta': '1 mês, porque sim.'
    },
    {
        'pergunta': 'Qual o motivo do nosso dia de namoro ser dia 22?',
        'opcoes': ['Porque era a única data que tinha disponível no restaurante', 'Porque foi o dia que eu comprei as alianças', 'Porque o dia 22 simboliza a idade que tínhamos quando nos conhecemos, nos beijamos e começamos a namorar (além de ter relação com 2002, o ano que nascemos)', 'Porque 22 são dois patinhos na lagoa'],
        'resposta': 'Porque o dia 22 simboliza a idade que tínhamos quando nos conhecemos, nos beijamos e começamos a namorar (além de ter relação com 2002, o ano que nascemos)'
    },
    {
        'pergunta': 'Das músicas que eu toquei no pedido de namoro, qual foi a música para a letra B?',
        'opcoes': ['BB (Garupa de moto Amarela) / Tim Bernardes', 'Beijinho no Ombro / Valesca Popozuda', 'Bumbum Granada / MC Zaac', 'Batom de Cereja / Israel e Rodolfo'],
        'resposta': 'BB (Garupa de moto Amarela) / Tim Bernardes'
    },
    {
        'pergunta': 'Como uma expressão de loucura de amor, qual foi a frase que pichei no muro pra você?',
        'opcoes': ['Fe & Bia <3', 'Felipe Teofilo & Beatriz Ferreira', 'Deus é fiel', 'Nenhuma das anteriores, pois eu não sou louco de fazer isso, e de acordo com a Lei de Crimes Ambientais (Lei nº 9.605/98). O crime é tipificado no artigo 65 da lei, que prevê pena de detenção de três meses a um ano, e multa, para quem pichar, grafitar ou por outro meio conspurcar edificação ou monumento urbano. '],
        'resposta': 'Fe & Bia <3'
    },
    {
        'pergunta': 'No fatídico dia do Pico do Urubu, qual loucura nós cometemos?',
        'opcoes': ['Te pedi em casamento e falei que te amo', 'Nos beijamos loucamente como se não houvesse o amanhã', 'Declaramos amor um ao outro com todas as 5 linguagens do amor', 'Todas alternativas acima'],
        'resposta': 'Todas alternativas acima'
    },
    {
        'pergunta': 'No nosso segundo beijo, na rua da Padaria Dona Augusta, qual era a temperatura exata do dia, levando em conta que era um dia chuvoso?',
        'opcoes': ['17.3 ºC', '20.4 ºC', '14.9 ºC', 'A temperatura exata não sei, só sei que o beijo estava pegando fogo 🥵'],
        'resposta': 'A temperatura exata não sei, só sei que o beijo estava pegando fogo 🥵'
    },
    {
        'pergunta': 'O que fizemos no nosso segundo dia 22?',
        'opcoes': ['Fomos na sorveteria em Ferraz', 'Mó chatão aquele filme do cinema, mas o date foi bom demais', 'Fomos no Max Feffer', 'Fomos no rodízio de hamburguer Hi Guys'],
        'resposta': 'Mó chatão aquele filme do cinema, mas o date foi bom demais'
    },
    {
        'pergunta': 'Por que eu te amo tanto?',
        'opcoes': ['Pq vc é mó gente boa', 'Pq tem que amar o próximo', 'Pq amar é grátis', 'Porque você é tudo que eu sempre quis pra minha vida, dona do meu coração, rainha da sabedoria, minha mulher maravilha, minha Vênus, minha arte moderna, minha Afrodite, minha Garota de Ipanema, minha musa do verão, o Amor da Minha Vida!'],
        'resposta': 'Porque você é tudo que eu sempre quis pra minha vida, dona do meu coração, rainha da sabedoria, minha mulher maravilha, minha Vênus, minha arte moderna, minha Afrodite, minha Garota de Ipanema, minha musa do verão, o Amor da Minha Vida!'
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
