# Flask: Framework de microestrutura (microframework) para construir aplicações web.
from flask import Flask, request, jsonify
import psycopg2

# Cria a instância da aplicação.
app = Flask(__name__)

# Configurando o BD.
db_conn = psycopg2.connect(
    dbname="userdb",
    user="postgres",
    password="root",
    host="localhost"
)


# Função que retorna todos os usuários cadastrados.
@app.route('/listarUsuarios', methods=['GET'])
def get_listarUsuarios():
    try:
        cursor = db_conn.cursor()
        cursor.execute('SELECT * FROM tusuario')
        # Fetchall recupera todas as linhas de resultados da consulta.
        listaUsuarios = cursor.fetchall()
        cursor.close()
        return jsonify(listaUsuarios)
    except Exception as e:
        return jsonify({"Erro ao executar a função 'listarUsuarios'": str(e)})


# Função que busca um usuário específico por seu ID.
@app.route('/buscarPorCodigo/<int:codigo>', methods=['GET'])
def get_buscarPorCodigo(codigo):
    try:
        cursor = db_conn.cursor()
        cursor.execute('SELECT * FROM tusuario WHERE codigo = %s', [codigo])
        # Fetchone recupera uma única linha da consulta.
        usuarioEncontrado = cursor.fetchone()
        cursor.close()
        return jsonify(usuarioEncontrado)
    except Exception as e:
        return jsonify({"Erro ao executar a função 'buscarPorCodigo'"})

@app.route('/cadastrarUsuario', methods=['POST'])
def add_cadastrarUsuario():
    try:
        data = request.json # Assume que você está enviando dados JSON no corpo da solicitação
        nome = data.get('nome')
        email = data.get('email')
        senha = data.get('senha')

        cursor = db_conn.cursor()
        cursor.execute('INSERT INTO tusuario(nome, email, senha) VALUES (%s, %s, %s) RETURNING codigo', (nome, email, senha))
        db_conn.commit()
        novoUsuario = cursor.fetchone()[0]
        cursor.close()

        return jsonify({"message": "Usuário adicionado com sucesso!", "Código do Usuário": novoUsuario})
    except Exception as e:
        db_conn.rollback() # Desfaz as alterações no BD.
        return jsonify({"Erro ao executar a função 'cadastrarUsuario'":str(e)})

@app.route('/deletarPorCodigo/<int:codigo>', methods=['DELETE'])
def delete_deletarPorCodigo(codigo):
    try:
        cursor = db_conn.cursor()
        cursor.execute('DELETE FROM tusuario WHERE codigo = %s', [codigo])
        db_conn.commit()
        cursor.close()
        return jsonify({"message": "Usuário deletado com sucesso!"})
    except Exception as e:
        db_conn.rollback() # Desfaz as alterações no BD.
        return jsonify({"Erro ao executar a função 'deletarPorCodigo'":str(e)})


if __name__ == '__main__':
    app.run(debug=True)
