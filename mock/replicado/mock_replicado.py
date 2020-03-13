from flask import Flask, jsonify

app = Flask(__name__)

def make_data():
    data =  [
                {
                    "nome": "Capistrano",
                    "cargo": "Aluno graduação",
                    "email": "capis@usp.com",
                    "phone": "1112233",
                    "doc": "usp",
                    "doc_num": "456666",
                    "answerable": "Shista",
                    "departament": "ACA"
                },
                {
                    "nome": "Tentaculous",
                    "cargo": "Aluno graduação",
                    "email": "tents@usp.com",
                    "phone": "187632433",
                    "doc": "usp",
                    "doc_num": "9823456",
                    "answerable": "sheba",
                    "deoartament": "ACA"
                },
                {
                    "nome": "Zibauwe",
                    "cargo": "Aluno graduação",
                    "email": "zin@usp.com",
                    "phone": "1879999433",
                    "doc": "usp",
                    "doc_num": "9823333",
                    "answerable": "sheba",
                    "departament": "AGG"
                }
            ]
    return data

@app.route('/replicado/alunos')
def alunos():
    data = make_data()
    return jsonify(data)


@app.route('/replicado/alunos/name/Capistrano')
def alunos_by_name():
    data =  [{"nome": "Capistrano", "cargo": "Aluno graduação", "email": "capis@usp.com",\
                    "phone": "1112233", "doc": "usp", "doc_num": "456666", "answerable": "Shista",\
                    "departament": "ACA" }]

    return jsonify(data)
