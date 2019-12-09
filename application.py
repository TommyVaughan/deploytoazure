from flask import Flask, jsonify, request, abort
from filmDAO import filmDAO

app = Flask(__name__, static_url_path='', static_folder='.')


#curl "http://127.0.0.1:5000/films"
@app.route('/films')
def getAll():
    #print("in getall")
    results = filmDAO.getAll()
    return jsonify(results)

#curl "http://127.0.0.1:5000/films/2"
@app.route('/films/<int:id>')
def findById(id):
    foundFilm = filmDAO.findByID(id)

    return jsonify(foundFilm)

#curl  -i -H "Content-Type:application/json" -X POST -d "{\"title\":\"hello\",\"director\":\"someone\",\"released\":2010}" http://127.0.0.1:5000/films
@app.route('/films', methods=['POST'])
def create():
    
    if not request.json:
        abort(400)
    
    film = {
        'title': request.json['title'],
        'director': request.json['director'],
        'released': request.json['released'],
    }
    values = (film['title'],film['director'],film['released'])
    newId = filmDAO.create(values)
    film['id'] = newId
    return jsonify(film)

#curl  -i -H "Content-Type:application/json" -X PUT -d "{\"title\":\"hello\",\"director\":\"someone\",\"released\":2010}" http://127.0.0.1:5000/films/3
@app.route('/films/<int:id>', methods=['PUT'])
def update(id):
    foundFilm = filmDAO.findByID(id)
    if not foundFilm:
        abort(404)
    
    if not request.json:
        abort(400)
    reqJson = request.json
    if 'released' in reqJson and type(reqJson['released']) is not int:
        abort(400)

    if 'title' in reqJson:
        foundFilm['title'] = reqJson['title']
    if 'director' in reqJson:
        foundFilm['director'] = reqJson['director']
    if 'released' in reqJson:
        foundFilm['released'] = reqJson['released']
    values = (foundFilm['title'],foundFilm['director'],foundFilm['released'],foundFilm['id'])
    filmDAO.update(values)
    return jsonify(foundFilm)
        

    

@app.route('/films/<int:id>' , methods=['DELETE'])
def delete(id):
    filmDAO.delete(id)
    return jsonify({"done":True})




if __name__ == '__main__' :
    app.run(debug= True)
