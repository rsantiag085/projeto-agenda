import os
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

#### conexão com o banco de dados ####
DB_USER = os.environ.get('DB_USER', 'postgres')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'password')
DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_NAME = os.environ.get('DB_NAME', 'agenda_db')

DATABASE_URL = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

#### modelo de dados ####
class Contato(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'telefone': self.telefone,
            'email': self.email
        }

#### rotas da API ####
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'ok'}), 200

@app.route('/contatos', methods=['GET'])
def get_contatos():
    try:
        contatos = Contato.query.all()
        lista_contatos = [contato.to_dict() for contato in contatos]
        return jsonify(lista_contatos), 200
    except Exception as e:
        return jsonify({"error": f"Erro ao buscar contatos: {str(e)}"}), 500

@app.route('/contatos', methods=['POST'])
def add_contato():
    try:
        data = request.json
        if not data or 'nome' not in data or 'telefone' not in data or 'email' not in data:
            return jsonify({"error": "Dados 'nome' e 'telefone' são obrigatórios"}), 400

        novo_contato = Contato(
            nome=data['nome'],
            telefone=data['telefone'],
            email=data.get('email', '')
        )
        db.session.add(novo_contato)
        db.session.commit()

        return jsonify({"message": "Contato adicionado com sucesso", "contato": novo_contato.to_dict()}), 201
    except Exception as e:
        return jsonify({"error": f"Erro ao adicionar contato: {str(e)}"}), 500

#### inicialização do banco de dados ####
if __name__ == '__main__':
    with app.app_context():
        print("Criando tabelas no banco de dados, se não existirem...")
        db.create_all()
        print("Tabelas criadas com sucesso.")

    app.run(host='0.0.0.0', port=5000, debug=True)