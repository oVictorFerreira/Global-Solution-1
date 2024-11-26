document.addEventListener('DOMContentLoaded', () => {
   
    const loadingScreen = document.querySelector('.loading-screen');
    const progress = document.querySelector('.progress');
    const progressText = document.querySelector('.progress-text');
    const mainContent = document.querySelector('.conteudo-principal');
    
    let width = 0;
    const interval = setInterval(() => {
        if (width >= 100) {
            clearInterval(interval);
            setTimeout(() => {
                loadingScreen.classList.add('fade-out');
                mainContent.style.opacity = '1';
                setTimeout(() => {
                    loadingScreen.style.display = 'none';
                }, 500);
            }, 500);
        } else {
            width += Math.random() * 6;
            if (width > 100) width = 100;
            progress.style.width = width + '%';
            progressText.textContent = Math.round(width) + '%';
        }
    }, 50);

    
    const menuToggle = document.querySelector('.menu-toggle');
    const menu = document.querySelector('.menu');
    const fecharMenu = document.querySelector('.fechar-menu');
    const menuOverlay = document.querySelector('.menu-overlay');
    const menuLinks = document.querySelectorAll('.menu a');

    function toggleMenu() {
        menu.classList.toggle('active');
        menuOverlay.classList.toggle('active');
        document.body.style.overflow = menu.classList.contains('active') ? 'hidden' : '';
    }

    menuToggle.addEventListener('click', toggleMenu);
    fecharMenu.addEventListener('click', toggleMenu);
    menuOverlay.addEventListener('click', toggleMenu);

    menuLinks.forEach(link => {
        link.addEventListener('click', () => {
            toggleMenu();
            const targetId = link.getAttribute('href');
            const targetElement = document.querySelector(targetId);
            
            if (targetElement) {
                const headerOffset = 80;
                const elementPosition = targetElement.getBoundingClientRect().top;
                const offsetPosition = elementPosition + window.pageYOffset - headerOffset;

                window.scrollTo({
                    top: offsetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });

   
    const carousel = document.querySelector('.carousel');
    const slides = document.querySelectorAll('.slide');
    const dots = document.querySelectorAll('.dot');
    const prevBtn = document.querySelector('.carousel-btn.prev');
    const nextBtn = document.querySelector('.carousel-btn.next');
    
    let currentSlide = 0;
    const totalSlides = slides.length;

    
    function updateCarousel() {
        carousel.style.transform = `translateX(-${currentSlide * 100}%)`;
        
        
        dots.forEach((dot, index) => {
            dot.classList.toggle('active', index === currentSlide);
        });
    }

   
    function nextSlide() {
        currentSlide = (currentSlide + 1) % totalSlides;
        updateCarousel();
    }

   
    function prevSlide() {
        currentSlide = (currentSlide - 1 + totalSlides) % totalSlides;
        updateCarousel();
    }

    
    nextBtn.addEventListener('click', nextSlide);
    prevBtn.addEventListener('click', prevSlide);

    
    dots.forEach((dot, index) => {
        dot.addEventListener('click', () => {
            currentSlide = index;
            updateCarousel();
        });
    });

    
    let carouselInterval = setInterval(nextSlide, 5000);

    
    const carouselContainer = document.querySelector('.carousel-container');
    carouselContainer.addEventListener('mouseenter', () => {
        clearInterval(carouselInterval);
    });

    carouselContainer.addEventListener('mouseleave', () => {
        carouselInterval = setInterval(nextSlide, 5000);
    });

    
    const form = document.getElementById('formContato');
    form.addEventListener('submit', (e) => {
        e.preventDefault();
        
        const nome = document.getElementById('nome').value;
        const email = document.getElementById('email').value;
        const mensagem = document.getElementById('mensagem').value;
        
        if (!nome || !email || !mensagem) {
            mostrarAlerta('Por favor, preencha todos os campos!', 'erro');
            return;
        }

        if (!validarEmail(email)) {
            mostrarAlerta('Por favor, insira um email válido!', 'erro');
            return;
        }

        mostrarAlerta('Mensagem enviada com sucesso!', 'sucesso');
        form.reset();
    });

    
    const calculadoraForm = document.getElementById('calculadoraForm');
    const aparelhoSelect = document.getElementById('aparelho');
    const consumoKwh = document.getElementById('consumoKwh');
    const custoMensal = document.getElementById('custoMensal');
    const dicaEconomia = document.getElementById('dicaEconomia');

    const TARIFA_ENERGIA = 0.75;

    const DICAS_ECONOMIA = {
        ar: "Mantenha o filtro limpo e configure para 23°C, temperatura ideal para conforto e economia.",
        chuveiro: "Tome banhos mais curtos e evite usar na potência máxima no verão.",
        geladeira: "Não guarde alimentos quentes e evite abrir a porta desnecessariamente.",
        tv: "Desligue a TV quando ninguém estiver assistindo e reduza o brilho da tela.",
        micro: "Descongele os alimentos naturalmente antes de usar o micro-ondas."
    };

    aparelhoSelect.addEventListener('change', () => {
        const aparelho = aparelhoSelect.value;
        if (aparelho && DICAS_ECONOMIA[aparelho]) {
            dicaEconomia.textContent = DICAS_ECONOMIA[aparelho];
        } else {
            dicaEconomia.textContent = "Selecione um aparelho para ver dicas de economia.";
        }
    });

    calculadoraForm.addEventListener('submit', (e) => {
        e.preventDefault();
        
        const aparelho = aparelhoSelect.options[aparelhoSelect.selectedIndex];
        const potencia = parseFloat(aparelho.dataset.potencia);
        const horas = parseFloat(document.getElementById('horas').value);
        const dias = parseFloat(document.getElementById('dias').value);
        
        if (!potencia || !horas || !dias) {
            mostrarAlerta('Por favor, preencha todos os campos!', 'erro');
            return;
        }
        
       
        const consumoMensal = (potencia * horas * dias) / 1000;
        const custoEstimado = consumoMensal * TARIFA_ENERGIA;
        
        
        animarContador(consumoKwh, 0, consumoMensal.toFixed(2));
        animarContador(custoMensal, 0, custoEstimado.toFixed(2));
        
        mostrarAlerta('Cálculo realizado com sucesso!', 'sucesso');
    });

    function animarContador(elemento, inicio, fim) {
        const duracao = 1000; // 1 segundo
        const incremento = (fim - inicio) / (duracao / 16);
        let atual = inicio;
        
        const animar = () => {
            atual += incremento;
            if (atual <= fim) {
                elemento.textContent = atual.toFixed(2);
                requestAnimationFrame(animar);
            } else {
                elemento.textContent = fim;
            }
        };
        
        animar();
    }

    
    function validarEmail(email) {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(email);
    }

    
    function mostrarAlerta(mensagem, tipo) {
        const alertaDiv = document.createElement('div');
        alertaDiv.className = `alerta ${tipo}`;
        
        
        const conteudo = document.createElement('div');
        conteudo.className = 'alerta-conteudo';
        
        
        const icone = document.createElement('div');
        icone.className = 'alerta-icone';
        icone.innerHTML = tipo === 'sucesso' ? '✓' : '✕';
        
        
        const mensagemDiv = document.createElement('div');
        mensagemDiv.className = 'alerta-mensagem';
        mensagemDiv.textContent = mensagem;
        
        
        const btnFechar = document.createElement('button');
        btnFechar.className = 'alerta-fechar';
        btnFechar.innerHTML = '×';
        btnFechar.onclick = () => fecharAlerta(alertaDiv);
        
        
        const progressoDiv = document.createElement('div');
        progressoDiv.className = 'alerta-progresso';
        
        const progressoBar = document.createElement('div');
        progressoBar.className = 'alerta-progresso-bar';
        
        
        conteudo.appendChild(icone);
        conteudo.appendChild(mensagemDiv);
        conteudo.appendChild(btnFechar);
        progressoDiv.appendChild(progressoBar);
        
        alertaDiv.appendChild(conteudo);
        alertaDiv.appendChild(progressoDiv);
        
        document.body.appendChild(alertaDiv);
        
        
        progressoBar.style.animation = 'progressBar 3s linear forwards';
        
        
        setTimeout(() => fecharAlerta(alertaDiv), 3000);
        
        return alertaDiv;
    }

    function fecharAlerta(alertaDiv) {
        if (!alertaDiv.classList.contains('fadeOut')) {
            alertaDiv.classList.add('fadeOut');
            setTimeout(() => {
                if (alertaDiv.parentElement) {
                    alertaDiv.remove();
                }
            }, 500);
        }
    }


function isElementVisible(element) {
    const rect = element.getBoundingClientRect();
    return (
        rect.top >= 0 &&
        rect.left >= 0 &&
        rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
        rect.right <= (window.innerWidth || document.documentElement.clientWidth)
    );
}

function atualizarContador() {
    const contadores = document.querySelectorAll('.contador');
    let continuarContando = false;
    
    contadores.forEach(contador => {
        if (!contador.hasAttribute('data-started') && isElementVisible(contador)) {
            contador.setAttribute('data-started', 'true');
            contador.textContent = '0';
        }

        if (contador.hasAttribute('data-started')) {
            const meta = parseInt(contador.getAttribute('data-meta'));
            const atual = parseInt(contador.textContent);
            
            if (atual < meta) {
                contador.textContent = atual + 1;
                continuarContando = true;
            }
        }
    });

    if (continuarContando) {
        setTimeout(atualizarContador, 30);
    }
}


function iniciarContadores() {
    const contadores = document.querySelectorAll('.contador');
    contadores.forEach(contador => {
        contador.textContent = '0';
    });
    atualizarContador();
}


const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            iniciarContadores();
        }
    });
}, { threshold: 0.5 });


document.addEventListener('DOMContentLoaded', () => {
    const secaoConsumidores = document.getElementById('consumidores');
    if (secaoConsumidores) {
        observer.observe(secaoConsumidores);
    }
});


window.addEventListener('scroll', () => {
    const secaoConsumidores = document.getElementById('consumidores');
    if (secaoConsumidores && isElementVisible(secaoConsumidores)) {
        const contadores = document.querySelectorAll('.contador');
        contadores.forEach(contador => {
            if (!contador.hasAttribute('data-started')) {
                iniciarContadores();
            }
        });
    }
});
});
