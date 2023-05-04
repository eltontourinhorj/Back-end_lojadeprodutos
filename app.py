from flask import Flask, jsonify, request
import psycopg2

app = Flask(__name__)

# Conexão com o banco de dados
conn = psycopg2.connect(
    host="localhost",
    database="productdb",
    user="postgres",
    password="root"
)
cur = conn.cursor()


@app.route('/cadastrar_produto', methods=['POST'])
def cadastrar_produto():
    data = request.get_json()
    nome = data['nome']
    descricao = data['descricao']
    preco = data['preco']
    cur.execute("INSERT INTO produtos (nome, descricao, preco) VALUES (%s, %s, %s)",
                (nome, descricao, preco))
    conn.commit()
    return jsonify({'message': 'Produto cadastrado com sucesso!'})


@app.route('/buscar_produto/<int:produto_id>', methods=['GET'])
def buscar_produto(produto_id):
    cur.execute(
        "SELECT nome, descricao, preco FROM produtos WHERE id=%s", (produto_id,))
    produto = cur.fetchone()
    if produto is None:
        return jsonify({'message': 'Produto não encontrado!'}), 404
    return jsonify({'nome': produto[0], 'descricao': produto[1], 'preco': produto[2]})


@app.route('/buscar_produtos/', methods=['GET'])
def buscar_produtos():
    cur.execute(
        "SELECT * FROM produtos ")
    produto = cur.fetchall()
    produtos = []
    for row in produto:
        produto = {
            'id': row[0],
            'nome': row[1],
            'descricao': row[2],
            'preco': row[3]

        }
        produtos.append(produto)
    return jsonify(produtos)


@app.route('/deletar_produto/<int:produto_id>', methods=['DELETE'])
def deletar_produto(produto_id):
    try:
        cur.execute("DELETE FROM produtos WHERE id=%s", (produto_id))
        return '', 204
    except:
        return jsonify({"mensagem": "Erro ao excluir produto."}), 500
    finally:
        cur.close()


if __name__ == '__main__':
    app.run(debug=True)
