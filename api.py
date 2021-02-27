import mysql.connector 
from flask import Flask
import json

app=Flask(__name__)

con = mysql.connector.connect( 
  host="localhost", user="root", 
  password="", database="db") 

cursor = con.cursor() 

@app.route('/<string:audio>', methods=['GET'])
def get_audio(audio):
    try:
        Jsonify=jsonify(cursor.execute('SELECT * FROM ("%s")',audio))
        response = Response("Action is successful", 200)
    except:
        response = Response("The request is invalid", 400)
    return response,Jsonify

@app.route('/<string:audio>/<int:id>', methods=['GET'])
def get_audio_by_id(audio,id):
    try:
        Jsonify= jsonify(cursor.execute('SELECT * FROM ("%s") WHERE ID=("%d")',audio,id))
        response = Response("Action is successful", 200)
    except:
        response = Response("The request is invalid", 400)
    return response,Jsonify

@app.route('/<string:audio>', methods=['POST'])
def add_audio(audio):
    try:
        if audio=='Song':
            request_data = request.get_json()
            query = "select ID from Song"
            cursor.execute(query)
            lst = cursor.fetchall()
            if request_data['ID'] in lst:
                raise Exception('')
            if len(request_data['Name'])>100:
                raise Exception('')
            elif request_data['Duration']<1:
                raise Exception('')
            cursor.execute('INSERT INTO ("%s") VALUES("%d","%s","%d","%s")',audio,request_data['ID'],request_data['Name'],request_data['Duration'],str(datetime.datetime.now()))
        elif audio=='Podcast':
            request_data = request.get_json()
            query = "select ID from Podcast"
            cursor.execute(query)
            lst = cursor.fetchall()
            if request_data['ID'] in lst:
                raise Exception('')
            elif len(request_data['Name'])>100:
                raise Exception('')
            elif request_data['Duration']<1:
                raise Exception('')
            elif len(request_data['Host'])>100:
                raise Exception('')
            elif len(request_data['Participants'])>10:
                for i in request_data['Participants']:
                    if len(i)>100:
                        raise Exception('')
            cursor.execute('INSERT INTO ("%s") VALUES("%d","%s","%s","%s","%s","?")',audio,request_data['ID'],request_data['Name'],request_data['Duration'],str(datetime.datetime.now()),request_data['Host'],[','.join(request_data['Participants'])])
    
        elif audio=='Audiobook':
            request_data = request.get_json()
            query = "select ID from Audiobook"
            cursor.execute(query)
            lst = cursor.fetchall()
            if request_data['ID'] in lst:
                raise Exception('')
            if len(request_data['Title'])>100:
                raise Exception('')
            elif len(request_data['Auther'])>100:
                raise Exception('')
            elif len(request_data['Narrator'])>100:
                raise Exception('')
            elif request_data['Duration']<1:
                raise Exception('')
            cursor.execute('INSERT INTO ("%s") VALUES("%d","%s","%s","%s","%d","%s")',audio,request_data['ID'],request_data['Title'],request_data['Auther'],request_data['Narrator'],request_data['Duration'],str(datetime.datetime.now()))
        response = Response("Action is successful", 200)
    except:
        response = Response("Any error", 500)
    return response


@app.route('/<string:audio>/<int:id>', methods=['PUT'])
def update_audio(audio,id):
    try:
        if audio=='Song':
            request_data = request.get_json()
            cursor.execute('UPDATE ("%s") SET ID=("%d"),NAME=("%s") ,Duration=("%d")',audio,id,request_data['Name'],request_data['Duration'])
        elif audio=='Podcast':
            request_data = request.get_json()
            cursor.execute('UPDATE ("%s") SET ID=("%d"),NAME=("%s") ,Duration=("%d"),Host=("%s"),Participants=("?")',audio,id,request_data['Name'],request_data['Duration'],request_data['Host'],[','.join(request_data['Participants'])])
    
        elif audio=='Audiobook':
            request_data = request.get_json()
            cursor.execute('UPDATE ("%s") SET ID=("%d"),Title=("%s"). Auther=("%s"), Narrator=("%s") ,Duration=("%d")',audio,id,request_data['ID'],request_data['Title'],request_data['Auther'],request_data['Narrator'],request_data['Duration'])
        response = Response("Action is successful", 200)
    except:
        response = Response("Any error", 500)
    return response

# route to delete movie using the DELETE method
@app.route('/<string:audio>/<int:id>', methods=['DELETE'])
def remove_audio(audio,id):
    try:
        cursor.execute('DELETE ("%s") WHERE ID=("%d")',audio,id)
        response = Response("Action is successful", status=200)
    except:
        response = Response("Any error", 500)
    return response


if __name__ == '__main__':
    app.run_server(debug=True)