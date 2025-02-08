// ***Front de recomendação dos produtos***

let pedido = new Map();
let numeroProdutos = 0;
let paginaAnterior = document.querySelector("#main").innerHTML;
const pesquisar = document.querySelector("#barra-de-pesquisa");
const isEmpty = str => !str.trim().length;

// Verifica click na barra de pesquisa
pesquisar.addEventListener("click", () => {
    const recomendacoes = document.querySelector("#recomendacoes");
    recomendacoes.hidden = false;
    document.querySelector("#aviso-nenhum-produto").innerHTML = '';
});

// Verifica se barra de pesquisa está vazia
pesquisar.addEventListener("input", function () {
    if (isEmpty(this.value) && numeroProdutos == 0) {
        document.querySelector("#aviso-nenhum-produto").innerHTML = '<p class="py-5 my-5" style="font-size: .8em;">Nenhum produto adicionado ainda.</p>';
        recomendacoes.hidden = true;
    } else {
        const recomendacoes = document.querySelector("#recomendacoes");
        recomendacoes.hidden = false;
        document.querySelector("#aviso-nenhum-produto").innerHTML = '';
    };
});

// ***Lógica de adicionar produto e quantidade ao pedido***

function adicionarProduto(id_produto) {

    let jaAdicionado = false

    if (pedido.has(id_produto)) {
        jaAdicionado = true
    }

    let qnt_produto = document.getElementById(id_produto + "_qnt").value;

    pedido.set(id_produto, qnt_produto);

    if (!jaAdicionado) {
        atualizarRecomendacoes();
    }
}

function atualizarRecomendacoes() {

    document.querySelectorAll('.recomendacao button').forEach(produto => {
        pedido.forEach(() => {

            if (pedido.has(produto.getAttribute('id'))) {
                let tdNode = produto.parentNode;
                let trNode = tdNode.parentNode;
                trNode.hidden = true;
            }

        })
    })

    if (pedido.size == document.getElementsByClassName('recomendacao').length) {
        let recomendacoes = document.querySelector("#recomendacoes");
        recomendacoes.hidden = true;
        document.querySelector("#aviso-nenhum-produto").innerHTML = '<p class="pt-5 mt-5" style="font-size: .8em;">Não há mais produtos para se adicionar ao pedido.</p><p style="font-size: .6em;">Caso deseje editar algum valor, clique no icone de caixa acima.</p>';
    }

    numeroProdutos = pedido.size
    document.querySelector("#numero-produtos").hidden = false;
    document.querySelector("#numero-produtos-btn").hidden = false;
    document.querySelector("#numero-produtos").innerHTML = numeroProdutos;
    paginaAnterior = document.querySelector("#main").innerHTML;
}

function verPedido() {

    let todosProdutos = document.querySelectorAll(".recomendacao")

    document.querySelector("#main").innerHTML =
        `
    <div class="d-flex justify-content-center mt-1 px-5 py-2 flex-column conteiner" id="conteiner">
    
    <div class="d-flex justify-content-between align-items-center">
        <button class="btn btn-outline-secondary mt-5 px-3 py-2" onclick="voltarPagina()">Voltar</button>
        <button class="btn btn-dark mt-5 px-3 py-2" onclick="enviarPedido()">Enviar</button>
    </div>

    <div id="recomendacoes">
        <table class="table">

            <thead>
                <tr>
                    <th scope="col" class="text-secondary">Nome</th>
                    <th scope="col" class="text-secondary">Qnt. Disponível</th>
                    <th scope="col" class="text-dark">-</th>
                </tr>
            </thead>


            <tbody>
                <!-- forEach no pedido para acrescentar as rows -->
            </tbody>

        </table>
    </div>
    `;

    todosProdutos.forEach(td => {
        
        tr = td.parentNode
        
        if (tr.hidden) {

            input = td.children[1]
            value = input.value
            input.setAttribute("value", value)

            button = td.children[0]
            button.innerHTML = "Atualizar"

            console.log(td.innerHTML)

            document.getElementsByTagName("tbody")[0].innerHTML += td.parentNode.innerHTML;
        }
    });
}

function voltarPagina() {
    document.querySelector("#main").innerHTML = paginaAnterior
}

async function enviarPedido() {

    let pedidoJSON = JSON.stringify(Object.fromEntries(pedido));
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    const request = new Request("http://localhost:8000/novo-pedido/", {
        headers: { 'X-CSRFToken': csrftoken },
        method: "POST",
        body: pedidoJSON
    });

    const res = await fetch(request);
    console.log(typeof res.status);

    if (res.status == 200) {
        window.location.href = "http://localhost:8000"
    } else {
        alert("Erro ao enviar, tente novamente mais tarde")
    }
}