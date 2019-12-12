# -*- coding: utf-8 -*-
#coding: utf-8
import redis
import time
import traceback
import fileinput


def RedisCheck():
    try:
        r = redis.StrictRedis(host='localhost', port=6379)                          # Connect to local Redis instance

        p = r.pubsub()                                                              # See https://github.com/andymccurdy/redis-py/#publish--subscribe
        p.subscribe('canalHash')                                                 # Subscribe to startScripts channel
        PAUSE = True

        f = open('hash.txt', 'r')
        lasthash = f.readline()
        lasthash = lasthash.rstrip()

        while PAUSE:                                                                # Will stay in loop until START message received
            message = p.get_message()                                               # Checks for message
            if message:
                command = message['data']                                       # Get data from message
            
                if command != 1:
                    print ('Mensagem recebida', command)
                    newhash = command + "\n" + lasthash             
                    codHash = (hash(newhash))
                    WorkCheck(codHash)
                    #print lasthash + str(codHash)
                    if lasthash != newhash:
                        print "Last block: " + lasthash
                        block = command + "\nLastBlock: " + lasthash +"\nBlockId: " + str(codHash)  
                        arquivo = open('blockchain.txt', 'r')# Abra o arquivo (leitura)
                        conteudo = arquivo.readlines()
                        conteudo.append("\n" + block) # insira seu conteúdo
                        arquivo = open('blockchain.txt', 'w') # Abre novamente o arquivo (escrita)
                        arquivo.writelines(conteudo)   # escreva o conteúdo criado anteriormente nele.
                        print 'block ' + str(codHash) + ' added'   
                        arquivo.writelines("\n")   # escreva o conteúdo criado anteriormente nele.
                        arquivo.close()
                        lasthash = str(codHash)
                    for line in fileinput.input("hash.txt", inplace=1):
                        print line.replace(str(line), str(codHash))

                    

        time.sleep(1)
        

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

        r = redis.Redis(host='localhost', port=6379)                # Connect to local Redis instance

        p = r.pubsub()    
        time.sleep(1)                                                # See https://github.com/andymccurdy/redis-py/#publish--subscribe
        r.publish('hashd', responset)
        print ("Funcao hash", responset)
        
    except Exception as e:
        print("!!!!!!!!!! EXCEPTION !!!!!!!!!")
        print(str(e))
        print(traceback.format_exc())

RedisCheck()
