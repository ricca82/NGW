#mi import fastapi per creare il backend in python
from fastapi import FastAPI
#per richieste standardizzate
from pydantic import BaseModel
#per connessione
import mysql.connector


#per evitare errori di CORS
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

#sempre per cors
# Middleware per gestire le intestazioni CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#file di configurazione per connessione
config = {
    "host" : "127.0.0.1",
    "port" : "3306", #standard
    "user" : "root",
    "database" : "instagram_users"
}

class user_register(BaseModel):
    username: str
    nome: str
    cognome: str
    password: str

#la rotta di registrazione
@app.post("/api/register")
def registrazione(user : user_register):
    conn = mysql.connector.connect(**config) # host = config#host
    cursor  = conn.cursor()
    cursor.execute("INSERT INTO users (username, nome, cognome, password) VALUES (%s,%s,%s,%s)" 
                , (user.username, user.nome, user.cognome, user.password))
    conn.commit()
    conn.close()
    return {
        "msg" : "utente inserito con successo"
    }
    
#la rotta di stampa di tutti gli utenti
@app.get("/api/allusers")
def all_users():
    conn = mysql.connector.connect(**config) # host = config#host
    cursor  = conn.cursor(dictionary=True)
    cursor.execute("SELECT * from users")
    #fetchall restituisce una lista degli oggetti utenti trovati
    users = cursor.fetchall()
    conn.close()
    return users
    
#la rotta che stampa i dati di un dato username specifico
@app.get("/api/user/{username}")
def user(username : str):
    conn = mysql.connector.connect(**config) # host = config#host
    cursor  = conn.cursor(dictionary=True)
    cursor.execute(f"SELECT * from users WHERE username = '{username}' ")
    
    #fetchone restituisce la prima riga che ha trovato
    #   noi sappiamo che la riga sarà prima ma anche unica
    user = cursor.fetchone()
    conn.close()
    if user :
        return user
    else : 
        return {
            "msg" : "utente not found"
        }
    
        
# La parte due : 
#voglio creare la rotta di creazione post e di stampa tutti i post
class post(BaseModel):
    caption: str
    image_url: str
    
#rotta di creazione post tramite metodo post
@app.post("/api/create_post/{username}")
def create_post(username:str, post: post):
    conn = mysql.connector.connect(**config) # host = config#host
    cursor  = conn.cursor(dictionary=True)
    cursor.execute("INSERT INTO posts(username, caption, image_url) VALUES (%s,%s,%s)", 
                    (username, post.caption, post.image_url))
    conn.commit()
    conn.close()
    return {
        "msg" : "tutto andato a buon fine"
    }
    
#creiamo la rotta di stampa post
@app.get("/api/home")
def all_post():
    conn = mysql.connector.connect(**config) # host = config#host
    cursor  = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM posts")
    posts = cursor.fetchall()
    #fetchall restituisce una lista degli oggetti post trovati
    conn.close()
    return posts
class message(BaseModel):
    receiver : str
    message_text: str
@app.post("api/send_message/{sender}")
def send_message(sender:str,message:message):
    conn = mysql.connector.connect(**config) # host = config#host
    cursor  = conn.cursor(dictionary=True)
    cursor.execute("insert into messages(sender,receiver,message_text) VALUES (%s,%s,%s)",
                    (sender,message.receiver,message.message_text))
    conn.commit()
    conn.close()
    return{
        "msg":"messaggio creato"
    }
@app.get("/api/read_message{username}")
def read_message(username:str):
    conn = mysql.connector.connect(**config) # host = config#host
    cursor  = conn.cursor(dictionary=True)
    cursor.execute("select * from messages where receiver=%s") ,(username),
    #restituisce la lista dei messaggi trovati
    posts=cursor.fetchall()
    conn.close()
    return{
        "msg":"messaggio creato"
    }