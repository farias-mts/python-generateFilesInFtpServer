import requests
import random
import json
from ftplib import FTP
import os
import fileinput
import csv
import time

def generate_people(**args):
    data_people = []
    num = 0
    while num!=int(args['number']):
        idade = random.choice(range(15,30))
        payload = {
            'acao':'gerar_pessoa',
            'sexo':'I',
            'idade':idade,
            'cep_estado':None,
            'txt_qtde':1,
            'cep_cidade':None
        }
        response = requests.post('https://www.4devs.com.br/ferramentas_online.php', data=payload)
        data_json = json.loads(response.text)
        first_name = data_json['nome'].split(' ')[0]
        last_name = data_json['nome'].split(' ')[len(data_json['nome'].split(' '))-1]
        idade = data_json['idade']
        cpf = data_json['cpf']
        rg = data_json['rg']
        data_nasc = data_json['data_nasc']
        sexo = data_json['sexo']
        data_people.append([
            '{first} {last}'.format(first=first_name, last=last_name),
            idade,
            cpf,
            rg,
            data_nasc,
            sexo
        ])      
        num+=1
    return data_people

def save(**args):
    fields_name = [
            'name',
            'idade',
            'cpf',
            'rg',
            'data_nasc',
            'sexo'
    ]
    file = open('csv_file_{time}.csv'.format(time=str(time.time())), 'w', newline ='')
    write = csv.writer(file, delimiter=";") 
    write.writerow(fields_name) 
    write.writerows(args['data_people'])
    myfile = open(file.name, 'rb')
    print(myfile)
    print('STOR %s' % file.name, myfile)
    args['ftp'].storlines('STOR '+file.name, myfile)
    print('uploaded')
    args['ftp'].dir()

def connect_ftp_server(**args):
    ftp = FTP()
    ftp.connect(args['host'], int(args['port']))
    ftp.login(args['username'], args['password'])
    ftp.cwd('/Matheus')
    for i in range(1):
        data_people = generate_people(number=3)
        save(data_people=data_people, ftp=ftp)
    ftp.quit()
        

host = '192.168.1.170'
port = '21'
username = 'po75'
password = 'W193410s@'
connect_ftp_server(
    host=host,
    port=port,
    username=username,
    password=password
)




