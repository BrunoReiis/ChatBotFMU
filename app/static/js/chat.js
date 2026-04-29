// Chat UI — state machine: cpf → cadastro ou chat normal

document.addEventListener("DOMContentLoaded", function () {
    const chatForm     = document.getElementById("chat-form");
    const chatInput    = document.getElementById("chat-input");
    const chatMessages = document.getElementById("chat-messages");

    // ── Estados possíveis ─────────────────────────────────────────────────────
    const STATES = {
        ASK_CPF        : "ask_cpf",
        REG_NOME       : "reg_nome",
        REG_IDADE      : "reg_idade",
        REG_ENDERECO   : "reg_endereco",
        REG_CARD_NUM   : "reg_card_num",
        REG_CARD_VENC  : "reg_card_venc",
        CHAT           : "chat",
        ADD_TRANS_VALOR: "add_trans_valor",
        ADD_TRANS_DATA : "add_trans_data",
    };

    let state   = STATES.ASK_CPF;
    let session = {};   // dados coletados durante o fluxo

    // Pergunta inicial
    botMsg("Olá! 👋 Para começar, por favor informe o seu CPF (somente números):");
    chatInput.placeholder = "Digite seu CPF...";

    // ── Submit ────────────────────────────────────────────────────────────────
    chatForm.addEventListener("submit", function (e) {
        e.preventDefault();
        const text = chatInput.value.trim();
        if (!text) return;

        userMsg(text);
        chatInput.value    = "";
        chatInput.disabled = true;

        handleState(text).finally(() => {
            chatInput.disabled = false;
            chatInput.focus();
        });
    });

    // ── Máquina de estados ────────────────────────────────────────────────────
    async function handleState(input) {
        const typing = showTyping();

        try {
            if (state === STATES.ASK_CPF) {
                await handleCpf(input);

            } else if (state === STATES.REG_NOME) {
                session.nome = input;
                state = STATES.REG_IDADE;
                botMsg("Qual é a sua idade?");
                chatInput.placeholder = "Digite sua idade...";

            } else if (state === STATES.REG_IDADE) {
                if (isNaN(parseInt(input))) { botMsg("Por favor, informe uma idade válida."); return; }
                session.idade = parseInt(input);
                state = STATES.REG_ENDERECO;
                botMsg("Qual é o seu endereço completo?");
                chatInput.placeholder = "Digite seu endereço...";

            } else if (state === STATES.REG_ENDERECO) {
                session.endereco = input;
                const res = await post("/cliente", {
                    nome    : session.nome,
                    idade   : session.idade,
                    endereco: session.endereco,
                    cpf     : session.cpf,
                });
                if (!res.ok && res.status !== 200) throw new Error("Erro ao criar cliente.");
                botMsg(`✅ Cadastro realizado com sucesso! Bem-vindo(a), ${session.nome}! 🎉`);
                botMsg("Agora vamos criar o seu cartão. Qual é o número do cartão? (13 a 19 dígitos)");
                chatInput.placeholder = "Digite o número do cartão...";
                state = STATES.REG_CARD_NUM;

            } else if (state === STATES.REG_CARD_NUM) {
                const num = input.replace(/\s/g, "");
                if (!/^\d{13,19}$/.test(num)) { botMsg("Número inválido. Digite entre 13 e 19 dígitos."); return; }
                session.card_numero = num;
                state = STATES.REG_CARD_VENC;
                botMsg("Qual é a data de vencimento do cartão? (formato AAAA-MM-DD)");
                chatInput.placeholder = "Ex: 2028-12-31";

            } else if (state === STATES.REG_CARD_VENC) {
                if (!/^\d{4}-\d{2}-\d{2}$/.test(input)) { botMsg("Formato inválido. Use AAAA-MM-DD (ex: 2028-12-31)."); return; }
                session.card_venc = input;
                const res = await post("/cartao", {
                    nome      : session.nome,
                    numero    : session.card_numero,
                    vencimento: session.card_venc,
                    cpf       : session.cpf,
                });
                if (!res.ok && res.status !== 200) throw new Error("Erro ao criar cartão.");
                botMsg("💳 Cartão cadastrado com sucesso!");
                botMsg("Tudo pronto! Agora pode me fazer suas perguntas sobre limite, fatura, pagamento, saldo e muito mais. 😊");
                chatInput.placeholder = "Digite sua pergunta...";
                state = STATES.CHAT;

            } else if (state === STATES.CHAT) {
                await handleChat(input);

            } else if (state === STATES.ADD_TRANS_VALOR) {
                const val = parseFloat(input.replace(",", "."));
                if (isNaN(val) || val <= 0) {
                    botMsg("Valor inválido. Por favor, informe um número positivo (ex: 150.00).");
                    return;
                }
                session.trans_valor = val;
                state = STATES.ADD_TRANS_DATA;
                botMsg("Qual a data da transação? (formato AAAA-MM-DD) — ou digite 'hoje'");
                chatInput.placeholder = "Ex: 2026-04-29 ou hoje";

            } else if (state === STATES.ADD_TRANS_DATA) {
                const dataStr = input.toLowerCase() === "hoje" ? null : input;
                if (dataStr && !/^\d{4}-\d{2}-\d{2}$/.test(dataStr)) {
                    botMsg("Formato inválido. Use AAAA-MM-DD (ex: 2026-04-29) ou 'hoje'.");
                    return;
                }
                const res = await post("/add_transacao", {
                    cpf  : session.cpf,
                    valor: session.trans_valor,
                    data : dataStr,
                });
                if (!res.ok) throw new Error("Erro ao salvar a transação.");
                botMsg(`✅ Transação de R$ ${session.trans_valor.toFixed(2)} salva com sucesso!`);
                botMsg("Posso ajudar com mais alguma coisa?");
                state = STATES.CHAT;
                chatInput.placeholder = "Digite sua pergunta...";
            }

        } catch (err) {
            botMsg("❌ " + (err.message || "Ocorreu um erro. Tente novamente."));
        } finally {
            removeTyping(typing);
        }
    }

    // ── CPF ───────────────────────────────────────────────────────────────────
    async function handleCpf(cpf) {
        const res  = await post("/check_cpf", { cpf });
        const data = await res.json();

        if (data.exists) {
            session.nome = data.nome;
            session.cpf  = cpf;
            botMsg(`Bem-vindo(a) de volta, ${data.nome}! 😊 Como posso te ajudar?`);
            chatInput.placeholder = "Digite sua pergunta...";
            state = STATES.CHAT;
        } else {
            session.cpf = cpf;
            botMsg("CPF não encontrado na nossa base. Vamos fazer o seu cadastro! 📋");
            botMsg("Qual é o seu nome completo?");
            chatInput.placeholder = "Digite seu nome completo...";
            state = STATES.REG_NOME;
        }
    }

    // ── Chat normal ───────────────────────────────────────────────────────────
    async function handleChat(message) {
        const norm = message.toLowerCase()
            .normalize("NFD").replace(/[\u0300-\u036f]/g, "");

        // Detecta intenção de adicionar transação
        if (norm.includes("adicionar") && (norm.includes("transacao") || norm.includes("trans"))) {
            session.trans_valor = null;
            state = STATES.ADD_TRANS_VALOR;
            botMsg("Certo! Vamos registrar uma transação. 💳");
            botMsg("Qual o valor da transação? (ex: 150.00)");
            chatInput.placeholder = "Digite o valor...";
            return;
        }

        // Detecta pagamento da fatura
        if (norm.includes("paguei") && norm.includes("fatura")) {
            const res = await post("/pagar_fatura", { cpf: session.cpf });
            if (!res.ok) throw new Error("Erro ao registrar pagamento.");
            botMsg("✅ Pagamento registrado! Sua fatura foi zerada com sucesso. 🎉");
            botMsg("Posso ajudar com mais alguma coisa?");
            return;
        }

        // Resposta padrão do chatbot
        const res  = await post("/ask", { message, cpf: session.cpf });
        const data = await res.json();
        const text = typeof data.response === "string"
            ? data.response
            : (data.response?.resposta || JSON.stringify(data.response));
        botMsg(text);
    }

    // ── Helpers ───────────────────────────────────────────────────────────────
    async function post(url, body) {
        return fetch(url, {
            method : "POST",
            headers: { "Content-Type": "application/json" },
            body   : JSON.stringify(body),
        });
    }

    function userMsg(text) {
        const div = document.createElement("div");
        div.classList.add("message", "user-message");
        div.textContent = text;
        chatMessages.appendChild(div);
        scrollBottom();
    }

    function botMsg(text) {
        const div = document.createElement("div");
        div.classList.add("message", "bot-message");
        div.textContent = text;
        chatMessages.appendChild(div);
        scrollBottom();
    }

    function showTyping() {
        const id  = "typing-" + Date.now();
        const div = document.createElement("div");
        div.classList.add("message", "bot-message", "typing");
        div.id          = id;
        div.textContent = "● ● ●";
        chatMessages.appendChild(div);
        scrollBottom();
        return id;
    }

    function removeTyping(id) {
        const el = document.getElementById(id);
        if (el) el.remove();
    }

    function scrollBottom() {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
});
