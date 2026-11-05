import json

from flask import Flask, Response, jsonify, render_template, request

app = Flask(__name__)
app.json.ensure_ascii = False

municipios_nordeste_dataset = {
    "metadados": {
        "regiao": "Nordeste",
        "pais": "Brasil",
        "total_municipios": 30,
        "fonte_dados_populacao": "IBGE",
    },
    "municipios": {
        "Fortaleza": {"id_ibge": 2304400, "estado": "Ceará", "sigla_uf": "CE", "capital": True, "populacao_estimada": 2582360},
        "Salvador": {"id_ibge": 2927408, "estado": "Bahia", "sigla_uf": "BA", "capital": True, "populacao_estimada": 2559945},
        "São Luís": {"id_ibge": 2111300, "estado": "Maranhão", "sigla_uf": "MA", "capital": True, "populacao_estimada": 1037775},
        "Teresina": {"id_ibge": 2211001, "estado": "Piauí", "sigla_uf": "PI", "capital": True, "populacao_estimada": 866300},
        "Natal": {"id_ibge": 2408102, "estado": "Rio Grande do Norte", "sigla_uf": "RN", "capital": True, "populacao_estimada": 751300},
        "João Pessoa": {"id_ibge": 2507507, "estado": "Paraíba", "sigla_uf": "PB", "capital": True, "populacao_estimada": 833932},
        "Recife": {"id_ibge": 2611606, "estado": "Pernambuco", "sigla_uf": "PE", "capital": True, "populacao_estimada": 1488920},
        "Maceió": {"id_ibge": 2704302, "estado": "Alagoas", "sigla_uf": "AL", "capital": True, "populacao_estimada": 957916},
        "Aracaju": {"id_ibge": 2800308, "estado": "Sergipe", "sigla_uf": "SE", "capital": True, "populacao_estimada": 602757},
        "Feira de Santana": {"id_ibge": 2910800, "estado": "Bahia", "sigla_uf": "BA", "capital": False, "populacao_estimada": 616272},
        "Vitória da Conquista": {"id_ibge": 2933307, "estado": "Bahia", "sigla_uf": "BA", "capital": False, "populacao_estimada": 370879},
        "Camaçari": {"id_ibge": 2905701, "estado": "Bahia", "sigla_uf": "BA", "capital": False, "populacao_estimada": 300372},
        "Juazeiro": {"id_ibge": 2918407, "estado": "Bahia", "sigla_uf": "BA", "capital": False, "populacao_estimada": 237000},
        "Juazeiro do Norte": {"id_ibge": 2307304, "estado": "Ceará", "sigla_uf": "CE", "capital": False, "populacao_estimada": 286000},
        "Caucaia": {"id_ibge": 2303709, "estado": "Ceará", "sigla_uf": "CE", "capital": False, "populacao_estimada": 355679},
        "Sobral": {"id_ibge": 2312908, "estado": "Ceará", "sigla_uf": "CE", "capital": False, "populacao_estimada": 203023},
        "Maracanaú": {"id_ibge": 2307650, "estado": "Ceará", "sigla_uf": "CE", "capital": False, "populacao_estimada": 234392},
        "Imperatriz": {"id_ibge": 2105302, "estado": "Maranhão", "sigla_uf": "MA", "capital": False, "populacao_estimada": 273110},
        "Caxias": {"id_ibge": 2103000, "estado": "Maranhão", "sigla_uf": "MA", "capital": False, "populacao_estimada": 156973},
        "Timon": {"id_ibge": 2112209, "estado": "Maranhão", "sigla_uf": "MA", "capital": False, "populacao_estimada": 174000},
        "Parnaíba": {"id_ibge": 2207702, "estado": "Piauí", "sigla_uf": "PI", "capital": False, "populacao_estimada": 162159},
        "Mossoró": {"id_ibge": 2408003, "estado": "Rio Grande do Norte", "sigla_uf": "RN", "capital": False, "populacao_estimada": 264577},
        "Parnamirim": {"id_ibge": 2403251, "estado": "Rio Grande do Norte", "sigla_uf": "RN", "capital": False, "populacao_estimada": 252716},
        "Campina Grande": {"id_ibge": 2504009, "estado": "Paraíba", "sigla_uf": "PB", "capital": False, "populacao_estimada": 419379},
        "Olinda": {"id_ibge": 2609600, "estado": "Pernambuco", "sigla_uf": "PE", "capital": False, "populacao_estimada": 349976},
        "Jaboatão dos Guararapes": {"id_ibge": 2607901, "estado": "Pernambuco", "sigla_uf": "PE", "capital": False, "populacao_estimada": 643000},
        "Caruaru": {"id_ibge": 2604106, "estado": "Pernambuco", "sigla_uf": "PE", "capital": False, "populacao_estimada": 378000},
        "Petrolina": {"id_ibge": 2611101, "estado": "Pernambuco", "sigla_uf": "PE", "capital": False, "populacao_estimada": 386000},
        "Arapiraca": {"id_ibge": 2700300, "estado": "Alagoas", "sigla_uf": "AL", "capital": False, "populacao_estimada": 234185},
        "Nossa Senhora do Socorro": {"id_ibge": 2804805, "estado": "Sergipe", "sigla_uf": "SE", "capital": False, "populacao_estimada": 192000},
    },
}

CAMPOS_OBRIGATORIOS = ["id_ibge", "estado", "sigla_uf", "populacao_estimada"]


def atualizar_total():
    municipios_nordeste_dataset["metadados"]["total_municipios"] = len(
        municipios_nordeste_dataset["municipios"]
    )


def validar_campos(dados, parcial=False):
    limpo = {}

    if not parcial:
        faltando = [c for c in CAMPOS_OBRIGATORIOS if c not in dados]
        if faltando:
            return None, "Campos obrigatórios ausentes: " + ", ".join(faltando)

    if "id_ibge" in dados:
        try:
            limpo["id_ibge"] = int(dados["id_ibge"])
        except (TypeError, ValueError):
            return None, "id_ibge deve ser um número inteiro."
        if limpo["id_ibge"] <= 0:
            return None, "id_ibge deve ser positivo."

    if "estado" in dados:
        estado = str(dados["estado"]).strip()
        if not estado:
            return None, "estado não pode ser vazio."
        limpo["estado"] = estado

    if "sigla_uf" in dados:
        sigla = str(dados["sigla_uf"]).strip().upper()
        if len(sigla) != 2:
            return None, "sigla_uf deve ter exatamente 2 letras."
        limpo["sigla_uf"] = sigla

    if "populacao_estimada" in dados:
        try:
            limpo["populacao_estimada"] = int(dados["populacao_estimada"])
        except (TypeError, ValueError):
            return None, "populacao_estimada deve ser um número inteiro."
        if limpo["populacao_estimada"] < 0:
            return None, "populacao_estimada não pode ser negativa."

    if "capital" in dados:
        valor = dados["capital"]
        if isinstance(valor, bool):
            limpo["capital"] = valor
        elif isinstance(valor, str) and valor.strip().lower() in ("true", "1", "sim"):
            limpo["capital"] = True
        elif isinstance(valor, str) and valor.strip().lower() in ("false", "0", "nao", "não"):
            limpo["capital"] = False
        else:
            return None, "capital deve ser verdadeiro ou falso."
    elif not parcial:
        limpo["capital"] = False

    return limpo, None


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/metadados", methods=["GET"])
def obter_metadados():
    atualizar_total()
    return jsonify(municipios_nordeste_dataset["metadados"]), 200


@app.route("/municipios", methods=["GET"])
def listar_municipios():
    uf = request.args.get("uf")

    if uf:
        uf = uf.strip().upper()
        filtrados = {}
        for nome, dados in municipios_nordeste_dataset["municipios"].items():
            if dados["sigla_uf"] == uf:
                filtrados[nome] = dados
        return jsonify(filtrados), 200

    return jsonify(municipios_nordeste_dataset["municipios"]), 200


@app.route("/municipios/<nome>", methods=["GET"])
def consultar_municipio(nome):
    municipio = municipios_nordeste_dataset["municipios"].get(nome)
    if municipio is None:
        return jsonify({"erro": f"Município '{nome}' não encontrado."}), 404
    return jsonify({nome: municipio}), 200


@app.route("/municipios", methods=["POST"])
def cadastrar_municipio():
    dados = request.get_json(silent=True)
    if not dados:
        return jsonify({"erro": "Envie os dados do município em formato JSON."}), 400

    nome = str(dados.get("nome", "")).strip()
    if not nome:
        return jsonify({"erro": "O campo 'nome' é obrigatório."}), 400

    if nome in municipios_nordeste_dataset["municipios"]:
        return jsonify({"erro": f"O município '{nome}' já está cadastrado."}), 409

    limpo, erro = validar_campos(dados, parcial=False)
    if erro:
        return jsonify({"erro": erro}), 400

    municipios_nordeste_dataset["municipios"][nome] = limpo
    atualizar_total()

    return jsonify({
        "mensagem": f"Município '{nome}' cadastrado com sucesso.",
        "municipio": {nome: limpo},
    }), 201


@app.route("/municipios/<nome>", methods=["PATCH"])
def atualizar_municipio(nome):
    municipio = municipios_nordeste_dataset["municipios"].get(nome)
    if municipio is None:
        return jsonify({"erro": f"Município '{nome}' não encontrado."}), 404

    dados = request.get_json(silent=True)
    if not dados:
        return jsonify({"erro": "Envie os dados a atualizar em formato JSON."}), 400

    limpo, erro = validar_campos(dados, parcial=True)
    if erro:
        return jsonify({"erro": erro}), 400

    if not limpo:
        return jsonify({"erro": "Nenhum campo válido foi informado para atualização."}), 400

    municipio.update(limpo)

    return jsonify({
        "mensagem": f"Município '{nome}' atualizado com sucesso.",
        "municipio": {nome: municipio},
    }), 200


@app.route("/municipios/<nome>", methods=["DELETE"])
def excluir_municipio(nome):
    if nome not in municipios_nordeste_dataset["municipios"]:
        return jsonify({"erro": f"Município '{nome}' não encontrado."}), 404

    del municipios_nordeste_dataset["municipios"][nome]
    atualizar_total()

    return jsonify({"mensagem": f"Município '{nome}' removido com sucesso."}), 200


@app.route("/download/municipios.json", methods=["GET"])
def baixar_json():
    atualizar_total()
    conteudo = json.dumps(municipios_nordeste_dataset, ensure_ascii=False, indent=2)
    return Response(
        conteudo,
        mimetype="application/json",
        headers={"Content-Disposition": "attachment; filename=municipios_nordeste.json"},
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)