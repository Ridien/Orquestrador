# -*- coding: utf-8 -*-
#coding: utf-8
import redis
import time
import traceback


def RedisCheck():
    try:
        r = redis.StrictRedis(host='localhost', port=6379)                          # Connect to local Redis instance

        p = r.pubsub()                                                              # See https://github.com/andymccurdy/redis-py/#publish--subscribe
        p.subscribe('canalPessoas')                                                 # Subscribe to startScripts channel
        PAUSE = True

        while PAUSE:                                                                # Will stay in loop until START message received
            message = p.get_message()                                               # Checks for message
            if message:
                command = message['data']                                       # Get data from message
            
                if command != 1:
                    #new code start
                    hasAccount = False
                    arquivo = open('nomes.txt', 'r')
                    for line in arquivo:
                        line=line.strip()
                        if command in line.split("\n"):
                            #print command + line
                            hasAccount = True
                            WorkCheck("O perfil ja existe, faca login")
                            print ('Dados recebidos:', command)
                            print ('O perfil ja existe, faça login')
                            break



                    # Checks for START message
                    if hasAccount == False:	 #new code end       
                        arquivo = open('nomes.txt', 'r')# Abra o arquivo (leitura)
                        conteudo = arquivo.readlines()
                        conteudo.append(command) # insira seu conteúdo
                        arquivo = open('nomes.txt', 'w') # Abre novamente o arquivo (escrita)
                        arquivo.writelines(conteudo)   # escreva o conteúdo criado anteriormente nele.
                        WorkCheck("Perfil Cadastrado")
                        arquivo.writelines("\n")   # escreva o conteúdo criado anteriormente nele.
                        arquivo.close()
                        print ('Dados recebidos:', command)
                        print ('Enviado: Perfil cadastrado')
	    time.sleep(1)


        print("Permission to start...")        

    except Exception as e:
        print("!!!!!!!!!! EXCEPTION !!!!!!!!!")
        print(str(e))
        print(traceback.format_exc())

def WorkCheck(responset):
    try:
        responset = str(responset)
        # HERE SOME INITIAL WORK IS DONE THAT SCRIPTS 1 & 2 NEED TO WAIT FOR
        # IDs SERIAL PORTS
        # SAVE TO db

        r = redis.StrictRedis(host='localhost', port=6379)                # Connect to local Redis instance

        p = r.pubsub()                                          # See https://github.com/andymccurdy/redis-py/#publish--subscribe
        
        r.publish('respostaPessoa', responset)                                # PUBLISH START message on startScripts channel
        #print (responset)
    except Exception as e:
        print("!!!!!!!!!! EXCEPTION !!!!!!!!!")
        print(str(e))
        print(traceback.format_exc())

RedisCheck()
