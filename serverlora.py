import time
import paho.mqtt.client as paho
import json
from influxdb import InfluxDBClient

broker="10.11.108.10"
port=1883

#define index db
def index(value, unidade, dispositivo):
    
    json_body = [       #json pattern to populate the database
        {
            "measurement": "XXX",
            "tags": {
                "host": "xxx",
                "region": "Kf"
            },            
            "fields": {
                "value":0.0
            }
        }
    ]

    json_body[0]["fields"]["value"] = value         #update the field
    json_body[0]["tags"]["host"] = dispositivo
    json_body[0]["measurement"] = unidade


    client = InfluxDBClient(broker, 8086, 'root', 'root', 'lora')          #setting my DB
    client.create_database('lora')                                              #name of my DB
    client.write_points(json_body)                                              #popuate my Db

    

#define callback
def on_message(client, userdata, message):
    time.sleep(1)
    msg = str(message.payload.decode("utf-8"))
    topicoG = ('F8033201CC5F')
    topicoE = ('4B686F6D70113574') 
    print("received message =",msg)
    print()
    jsonData = json.loads(msg)

    
    if jsonData[0]["bn"] == topicoG:     #gateway
        flag = 1
    if jsonData[0]["bn"] == topicoE:     #end-point
        flag = 0
    

    if flag == 0:       #it's a end-point

        if (jsonData[2]["n"] == ('C1'))or(jsonData[2]["n"] == ('C2')):      #it's a interruption (door)

            value = str(jsonData[2]["vb"])      #porta aberta ou fechada
            disp = str(jsonData[1]["vs"])       #quem sou eu
            unidade = str('porta_ped')          #qual medida estou mandando
           
            if value == 'True':
                value = 1                                
            if value == 'False':
                value = 0 

            index(value, unidade, disp)         #populando o banco
        
        if jsonData[2]["n"] == ('rssi'):                                    #medidas comuns
            
            value = float(jsonData[3]["v"])     #valor da temperatura
            disp = str(jsonData[1]["vs"])       #quem sou eu           
            unidade = 'temperatura_bi'          #temperatura built-in

            index(value, unidade, disp)

            value = float(jsonData[4]["v"])     #valor da umidade relativa
            unidade = '%rh_bi'                  #sensor built-in
                                                 
            index(value, unidade, disp)

            value = float(jsonData[5]["v"])     #valor da temperatura
            unidade = 'temperatura_sonda'       #temperatura sonda

            index(value, unidade, disp)
                
            
    if flag == 1:       #é um gateway

        if jsonData[1]["n"] == ('C1'or'C2'):      #é uma interrupção(porta)

            value = jsonData[1]["vb"]                       
            unidade = str('porta_bancada')
            disp = str(jsonData[0]["vs"])            
            
            if value == True:
                value = 1                
            if value == False:
                value = 0 

            index(value, unidade, disp)            
           
        else: 

            value = jsonData[1]["v"]
            unidade = str('Cel')
            disp = str(jsonData[0]["vs"])             
                                     
            index(value, unidade, disp)            


client1= paho.Client("client-001") #create client object client1.on_publish = $
#assign function to callback 
client1.connect(broker,port) 
#establish connection 
client1.publish("itg200","on")

######Bind function to callback

client1.on_message = on_message

#####

print("Connecting to broker ",broker)
client1.connect(broker) #connect
client1.loop_start() #start loop to process received messages
print("Subscribing ")
client1.subscribe("itg200") #subscribe


time.sleep(2)
while True:
    time.sleep(1)
    print(".")
