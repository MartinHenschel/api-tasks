from flask import request, jsonify
from models import db, User, Task
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity


def init_routes(app):

    # 🔹 Registrar usuário
    @app.route('/register', methods=['POST'])
    def register():
        data = request.json

        if not data or 'username' not in data or 'password' not in data:
            return jsonify({"msg": "Dados inválidos"}), 400

        user = User(
            username=data['username'],
            password=data['password']
        )

        db.session.add(user)
        db.session.commit()

        return jsonify({"msg": "Usuário criado"}), 201


    # 🔹 Login
    @app.route('/login', methods=['POST'])
    def login():
        data = request.json

        if not data:
            return jsonify({"msg": "JSON inválido"}), 400

        user = User.query.filter_by(username=data['username']).first()

        if not user or user.password != data['password']:
            return jsonify({"msg": "Credenciais inválidas"}), 401

        token = create_access_token(identity=str(user.id))

        return jsonify(access_token=token)


    # 🔹 Criar tarefa
    @app.route('/tasks', methods=['POST'])
    @jwt_required()
    def create_task():
        user_id = get_jwt_identity()
        data = request.json

        if not data or 'title' not in data:
            return jsonify({"msg": "Título obrigatório"}), 400

        task = Task(title=data['title'], user_id=user_id)
        db.session.add(task)
        db.session.commit()

        return jsonify({"msg": "Tarefa criada"})


    # 🔹 Listar tarefas
    @app.route('/tasks', methods=['GET'])
    @jwt_required()
    def get_tasks():
        user_id = get_jwt_identity()

        tasks = Task.query.filter_by(user_id=user_id).all()

        return jsonify([{"id": t.id, "title": t.title} for t in tasks])


    # 🔹 Atualizar tarefa (PUT)
    @app.route('/tasks/<int:id>', methods=['PUT'])
    @jwt_required()
    def update_task(id):
        user_id = get_jwt_identity()
        data = request.json

        if not data or 'title' not in data:
            return jsonify({"msg": "Título obrigatório"}), 400

        task = Task.query.filter_by(id=id, user_id=user_id).first()

        if not task:
            return jsonify({"msg": "Tarefa não encontrada"}), 404

        task.title = data['title']
        db.session.commit()

        return jsonify({"msg": "Tarefa atualizada com sucesso"})


    # 🔹 Deletar tarefa
    @app.route('/tasks/<int:id>', methods=['DELETE'])
    @jwt_required()
    def delete_task(id):
        user_id = get_jwt_identity()

        task = Task.query.filter_by(id=id, user_id=user_id).first()

        if not task:
            return jsonify({"msg": "Tarefa não encontrada"}), 404

        db.session.delete(task)
        db.session.commit()

        return jsonify({"msg": "Tarefa deletada com sucesso"})


    # 🔹 Rota de teste
    @app.route('/teste', methods=['GET'])
    def teste():
        return jsonify({"msg": "Rota funcionando!"})