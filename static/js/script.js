document.addEventListener('DOMContentLoaded', () => {
    // Animação de corações voando
    const heartsBackground = document.querySelector('.hearts-background');

    function createHeart() {
        const heart = document.createElement('div');
        heart.classList.add('heart');
        const size = Math.random() * 20 + 10; // Tamanho entre 10 e 30px
        heart.style.width = `${size}px`;
        heart.style.height = `${size}px`;
        heart.style.left = `${Math.random() * 100}vw`;
        heart.style.animationDuration = `${Math.random() * 5 + 5}s`; // Duração entre 5 e 10s
        heart.style.opacity = Math.random() * 0.7 + 0.3; // Opacidade entre 0.3 e 1
        heart.style.bottom = `-50px`; // Começa abaixo da tela
        heartsBackground.appendChild(heart);

        heart.addEventListener('animationend', () => {
            heart.remove();
        });
    }

    // Cria um coração a cada 0.5 segundos
    setInterval(createHeart, 500);

    // Adiciona uma pequena animação de "pulse" ao botão ao passar o mouse
    const buttons = document.querySelectorAll('button');
    buttons.forEach(button => {
        button.addEventListener('mouseover', () => {
            button.style.animation = 'heartBeat 0.5s ease-in-out infinite';
        });
        button.addEventListener('mouseout', () => {
            button.style.animation = 'none';
        });
    });
});