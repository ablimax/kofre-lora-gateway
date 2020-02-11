# Kofre LoRa Gateway

## Introduction

This application populates the MQTT Data to a influxdb database using HTTP. Next step, the Grafana read a influxdb to display the data.  

## How to use

### Running directly using Python 3

### With Docker

### With Docker Compose

```yml
version: '3.4'

services:

  grafana:  
    image: grafana/grafana:5.4.3
    volumes:
      - grafana-storage:/var/lib/grafana
    restart: always
    ports: 
      - 3000:3000
    links:
      - influxdb
      
  influxdb:
    image: influxdb
    volumes:
      - influxdb:/var/lib/influxdb
    restart: always
    ports: 
      - 8086:8086

  mqttbroker:
    image: eclipse-mosquitto
    ports:
      - 1883:1883
      - 9001:9001
  
  gateway:
    image: ablimax/kofre-lora-gateway:arm
    links:
      - influxdb
      - mqttbroker
    configs:
      - source: kofre-lora-gateway.json 
        targed: ./config.json
        
 ```

## Change log

### V1.0
First offcial working version using JSON config file.
