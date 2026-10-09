/* =========================================================
   Dra. Marina Vale — interações do site
   Sem dependências. Tudo funciona sem JS; o script apenas acrescenta.
   ========================================================= */
(function () {
  'use strict';

  var semMovimento = window.matchMedia('(prefers-reduced-motion: reduce)');

  /* ---------- 0. Agenda compartilhada de rolagem ---------- */
  var tarefas = [];
  var agendado = false;

  function executarTarefas() {
    agendado = false;
    for (var i = 0; i < tarefas.length; i++) {
      try { tarefas[i](); } catch (e) { /* uma tarefa não derruba as outras */ }
    }
  }

  function agendar() {
    if (agendado) return;
    agendado = true;
    window.setTimeout(executarTarefas, 80);
  }

  function aoRolar(tarefa) {
    tarefas.push(tarefa);
    tarefa();
  }

  window.addEventListener('scroll', agendar, { passive: true });
  window.addEventListener('resize', agendar);

  function alturaCabecalho() {
    var cabecalho = document.getElementById('cabecalho');
    return cabecalho ? cabecalho.getBoundingClientRect().height : 68;
  }

  /* ---------- 1. Menu em telas pequenas ---------- */
  (function menuMovel() {
    var botao = document.getElementById('menu-botao');
    var painel = document.getElementById('menu-movel');
    if (!botao || !painel) return;

    var fechar = document.getElementById('menu-fechar');
    var ultimoFoco = null;

    function focaveis() {
      return Array.prototype.filter.call(
        painel.querySelectorAll('a[href], button:not([disabled])'),
        function (el) { return el.offsetParent !== null; }
      );
    }

    function abrir() {
      ultimoFoco = document.activeElement;
      painel.hidden = false;
      document.body.classList.add('sem-rolagem');
      botao.setAttribute('aria-expanded', 'true');
      // força o cálculo de layout para a transição acontecer
      void painel.offsetWidth;
      painel.classList.add('aberto');

      var alvo = fechar || focaveis()[0];
      if (alvo) alvo.focus();
      document.addEventListener('keydown', aoTeclar);
    }

    function fecharMenu(devolverFoco) {
      painel.classList.remove('aberto');
      botao.setAttribute('aria-expanded', 'false');
      document.body.classList.remove('sem-rolagem');
      document.removeEventListener('keydown', aoTeclar);

      var esconder = function () { painel.hidden = true; };
      if (semMovimento.matches) esconder();
      else window.setTimeout(esconder, 220);

      if (devolverFoco !== false && ultimoFoco && ultimoFoco.focus) ultimoFoco.focus();
    }

    function aoTeclar(evento) {
      if (evento.key === 'Escape') {
        evento.preventDefault();
        fecharMenu(true);
        return;
      }
      if (evento.key !== 'Tab') return;

      var lista = focaveis();
      if (!lista.length) return;
      var primeiro = lista[0];
      var ultimo = lista[lista.length - 1];

      if (evento.shiftKey && document.activeElement === primeiro) {
        evento.preventDefault();
        ultimo.focus();
      } else if (!evento.shiftKey && document.activeElement === ultimo) {
        evento.preventDefault();
        primeiro.focus();
      }
    }

    botao.addEventListener('click', abrir);
    if (fechar) fechar.addEventListener('click', function () { fecharMenu(true); });

    painel.addEventListener('click', function (evento) {
      // clique no fundo escuro fecha
      if (evento.target === painel) { fecharMenu(true); return; }
      // escolher uma seção fecha (sem roubar o foco do destino)
      var link = evento.target.closest ? evento.target.closest('a[href]') : null;
      if (link) fecharMenu(false);
    });

    // se a tela crescer, o menu não deve continuar aberto
    var telaGrande = window.matchMedia('(min-width: 900px)');
    var aoMudarTela = function (e) { if (e.matches && !painel.hidden) fecharMenu(false); };
    if (telaGrande.addEventListener) telaGrande.addEventListener('change', aoMudarTela);
    else if (telaGrande.addListener) telaGrande.addListener(aoMudarTela);
  })();

  /* ---------- 2. Cabeçalho ganha borda ao rolar ---------- */
  (function cabecalhoRolado() {
    var cabecalho = document.getElementById('cabecalho');
    if (!cabecalho) return;
    aoRolar(function () {
      cabecalho.classList.toggle('rolado', window.scrollY > 8);
    });
  })();

  /* ---------- 3. Seção atual destacada no menu ---------- */
  (function secaoAtual() {
    var links = Array.prototype.slice.call(
      document.querySelectorAll('.navegacao__lista a[href^="#"]')
    );
    if (!links.length) return;

    var pares = [];
    links.forEach(function (link) {
      var secao = document.getElementById(link.getAttribute('href').slice(1));
      if (secao) pares.push({ link: link, secao: secao });
    });
    if (!pares.length) return;

    aoRolar(function () {
      var limite = alturaCabecalho() + 24;
      var atual = null;

      // a última seção que já passou pelo topo é a seção atual
      pares.forEach(function (par) {
        if (par.secao.getBoundingClientRect().top <= limite) atual = par;
      });

      // no fim da página, destaca a última seção
      if (window.innerHeight + window.scrollY >= document.body.scrollHeight - 4) {
        atual = pares[pares.length - 1];
      }

      pares.forEach(function (par) {
        if (par === atual) par.link.setAttribute('aria-current', 'true');
        else par.link.removeAttribute('aria-current');
      });
    });
  })();

  /* ---------- 4. Entrada discreta dos blocos ---------- */
  (function revelar() {
    var blocos = Array.prototype.slice.call(document.querySelectorAll('.revelar'));
    if (!blocos.length) return;

    function mostrarTudo() {
      blocos.forEach(function (bloco) { bloco.classList.add('visivel'); });
    }

    if (!('IntersectionObserver' in window) || semMovimento.matches) {
      mostrarTudo();
      return;
    }

    // só a partir daqui o CSS esconde os blocos
    document.documentElement.classList.add('com-revelacao');

    var observador = new IntersectionObserver(function (entradas, obs) {
      entradas.forEach(function (entrada) {
        if (entrada.isIntersecting) {
          entrada.target.classList.add('visivel');
          obs.unobserve(entrada.target);
        }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.06 });

    blocos.forEach(function (bloco) { observador.observe(bloco); });

    // rede de segurança: nada pode ficar invisível
    window.setTimeout(function () {
      observador.disconnect();
      mostrarTudo();
    }, 3000);
  })();

  /* ---------- 5. Galeria do consultório ---------- */
  (function galeria() {
    var trilho = document.getElementById('galeria-trilho');
    var contador = document.getElementById('galeria-contador');
    if (!trilho) return;

    var slides = Array.prototype.slice.call(trilho.querySelectorAll('.galeria__slide'));
    var anterior = document.querySelector('[data-galeria="anterior"]');
    var proxima = document.querySelector('[data-galeria="proxima"]');
    if (slides.length < 2) return;

    function indiceAtual() {
      var meio = trilho.scrollLeft + trilho.clientWidth / 2;
      var melhor = 0;
      var menorDistancia = Infinity;
      slides.forEach(function (slide, i) {
        var centro = slide.offsetLeft - trilho.offsetLeft + slide.offsetWidth / 2;
        var distancia = Math.abs(centro - meio);
        if (distancia < menorDistancia) { menorDistancia = distancia; melhor = i; }
      });
      return melhor;
    }

    function atualizar() {
      var i = indiceAtual();
      if (contador) contador.textContent = (i + 1) + ' de ' + slides.length;
      if (anterior) anterior.disabled = trilho.scrollLeft <= 2;
      if (proxima) {
        proxima.disabled = trilho.scrollLeft >= trilho.scrollWidth - trilho.clientWidth - 2;
      }
    }

    function irPara(i) {
      var alvo = slides[Math.max(0, Math.min(slides.length - 1, i))];
      if (!alvo) return;
      var destino = alvo.offsetLeft - trilho.offsetLeft
        - (trilho.clientWidth - alvo.offsetWidth) / 2;
      if (trilho.scrollTo) {
        trilho.scrollTo({ left: destino, behavior: semMovimento.matches ? 'auto' : 'smooth' });
      } else {
        trilho.scrollLeft = destino;
      }
      window.setTimeout(atualizar, 400);
    }

    if (anterior) anterior.addEventListener('click', function () { irPara(indiceAtual() - 1); });
    if (proxima) proxima.addEventListener('click', function () { irPara(indiceAtual() + 1); });

    trilho.addEventListener('keydown', function (evento) {
      if (evento.key === 'ArrowRight') { evento.preventDefault(); irPara(indiceAtual() + 1); }
      if (evento.key === 'ArrowLeft') { evento.preventDefault(); irPara(indiceAtual() - 1); }
    });

    var aguardando = false;
    trilho.addEventListener('scroll', function () {
      if (aguardando) return;
      aguardando = true;
      window.setTimeout(function () { aguardando = false; atualizar(); }, 80);
    }, { passive: true });

    window.addEventListener('resize', atualizar);
    atualizar();
  })();

  /* ---------- 6. Botão fixo de WhatsApp (telas pequenas) ---------- */
  (function whatsappFixo() {
    var botao = document.getElementById('whatsapp-fixo');
    if (!botao) return;

    botao.hidden = false;   // a visibilidade por tamanho de tela fica no CSS

    var abertura = document.getElementById('inicio');
    var contato = document.getElementById('contato');

    aoRolar(function () {
      var passouAbertura = !abertura ||
        abertura.getBoundingClientRect().bottom < alturaCabecalho();
      var contatoAVista = contato &&
        contato.getBoundingClientRect().top < window.innerHeight - 40;
      botao.classList.toggle('visivel', passouAbertura && !contatoAVista);
    });
  })();

  /* ---------- 7. Mostrar/ocultar marcações de pendência ---------- */
  (function pendencias() {
    var botao = document.getElementById('alternar-pendencias');
    if (!botao) return;

    var raiz = document.documentElement;

    function aplicar(ocultas) {
      raiz.classList.toggle('sem-pendencias', ocultas);
      botao.setAttribute('aria-pressed', ocultas ? 'true' : 'false');
      botao.textContent = ocultas ? 'Mostrar marcações de pendência' : 'Ocultar marcações de pendência';
      try {
        localStorage.setItem('mv-pendencias', ocultas ? 'ocultas' : 'visiveis');
      } catch (e) { /* armazenamento indisponível */ }
    }

    aplicar(raiz.classList.contains('sem-pendencias'));
    botao.addEventListener('click', function () {
      aplicar(!raiz.classList.contains('sem-pendencias'));
    });
  })();

})();
