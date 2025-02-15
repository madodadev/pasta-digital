const res_values = {
    a : "A",
    na: "NA",
    wd: "WD"
}

const TIPOS_AVALIACAO = {
    av : "avaliacao",
    r1: "reavaliacao_1",
    r2: "reavaliacao_2"
}

const resultadosEndPoint = "http://127.0.0.1:8000/resultados/setResultados/"

let selectAvaliacoes = document.querySelectorAll(".select_resultado")
let resultado_btn = document.querySelectorAll(".res_btn")

selectAvaliacoes.forEach((avaliacao) => {
    avaliacao.addEventListener("change", ()=> {
        let res_id = [parseInt(avaliacao.attributes.getNamedItem("resultado").value)]
        let tipoAvaliacao = avaliacao.attributes.getNamedItem("avaliacao").value
        let res_value = avaliacao.value
        console.log(tipoAvaliacao, res_id, res_value)
        postResultado(res_id, tipoAvaliacao, res_value)
        changeSelectClasse(avaliacao)
        if (tipoAvaliacao != TIPOS_AVALIACAO.r2) {
            show_hide_reavalicao(avaliacao)
        }
    })
})

resultado_btn.forEach((res_btn) => {
    res_btn.addEventListener('dblclick', ()=> {
        let res_row = res_btn.closest("tr")
        let avaliacoes = res_row.querySelectorAll(".select_resultado_avaliacao")
        let res_ids = []
        avaliacoes.forEach((avaliacao)=>{res_ids.push(parseInt(avaliacao.attributes.getNamedItem("resultado").value))})

        let tipoAvaliacao = TIPOS_AVALIACAO.av
        res_value = res_btn.attributes.getNamedItem("value").value
        console.log(res_ids, tipoAvaliacao, res_value)
    })
})
function changeSelectClasse(select) {
    const lastClassIndex = select.classList.length - 1;
    selectedValue = select.value
    if (lastClassIndex >= 0) {
        select.classList.remove(select.classList[lastClassIndex]);
        select.classList.add(`select_resultado_${selectedValue}`)
    }
}

function show_hide_reavalicao(select) {
    const selectedValue = select.value
    const nextResultado = select.parentElement.lastElementChild
    if (!selectedValue || selectedValue == res_values.a) {
        nextResultado.className = 'resultado_hide'
    }else {
        nextResultado.className = ''
    }
}

async function postResultado(res_ids, tipoAvaliacao, res_values) {
    const csrftoken = getCookie('csrftoken');
    let headers = new Headers();
    headers.append("X-CSRFToken", csrftoken);
    headers.append("Content-Type", "application/json");

    data = {
        "ids": res_ids,
        "tipo": tipoAvaliacao,
        "value": res_values
    }

    const response = await fetch(resultadosEndPoint, {
        method: "POST",
        body: JSON.stringify(data),
        headers: headers
    });

    console.log(response)
}


function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Check if this cookie string begins with the name we want
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}