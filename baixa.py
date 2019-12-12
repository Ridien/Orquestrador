import redis
import time
import traceback
import sys
import os
import signal
import fileinput

def validorder(item, qtd):
    #print item + " item"
    #print qtd + " qtd"
    am = int(qtd)
    sucesso = True

    f= fileinput.input('estoque.txt', inplace=1)
    for line in f:
        if item in line:
            data = line.split()
            qtdestoque = data[1]
            #print (data[0] + "data 0")
            #print (data[1] + "data 1")
            intqtdestoque = int(qtdestoque)
            #print qtdestoque + "amount available"
            if(intqtdestoque-am < 0):
                #print str(am-qtdestoque) + " amount left"
                
            
                sucesso=False
                

        sys.stdout.write(line)

    
    f.close()
    return sucesso

def darbaixa(item, qtd):
    #print item + " item"
    #print qtd + " qtd"
    am = int(qtd)
    sucesso = True

    f= fileinput.input('estoque.txt', inplace=1)
    for line in f:
        if item in line:
            data = line.split()
            qtdestoque = data[1]
            #print (data[0] + "data 0")
            #print (data[1] + "data 1")
            intqtdestoque = int(qtdestoque)
            #print qtdestoque + "amount available"
            if(intqtdestoque-am >= 0):
                #print str(am-qtdestoque) + " amount left"
                line = line.replace(str(data[1]), str(intqtdestoque - am))
            else:
                sucesso=False
                

        sys.stdout.write(line)

    
    f.close()
    return sucesso


def RedisCheck():
    try:
        r = redis.StrictRedis(host='200.235.93.96', port=6379)                          # Connect to local Redis instance

        p = r.pubsub()                                                              # See https://github.com/andymccurdy/redis-py/#publish--subscribe
        p.subscribe('canalBaixa')                                                 # Subscribe to startScripts channel
        PAUSE = True

        while PAUSE:                                                                # Will stay in loop until START message received
            message = p.get_message()                                               # Checks for message
            if message:
                command = message['data']                                       # Get data from message
            
                if command != 1:
                    #print("mensagem recebida" + command)
                    orderlist = str(command).split(",")
                    print orderlist

                    for i in orderlist:
                        checker = i.split()
                        #print checker
                        status = validorder(checker[0], checker[1])
                        if status == False:
                            WorkCheck('Falha')
                            break
                            
                    if status == True:
                        for i in orderlist:
                            checker = i.split()
                            #print checker
                            status = darbaixa(checker[0], checker[1])
                        WorkCheck('Sucesso')        
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

        r = redis.Redis(host='200.235.89.55', port=6379)                # Connect to local Redis instance

        p = r.pubsub()                                                    # See https://github.com/andymccurdy/redis-py/#publish--subscribe
        time.sleep(1)
        r.publish('darBaixaR', responset)                                # PUBLISH START message on startScripts channel
        print ("Respondi", responset)
    except Exception as e:
        print("!!!!!!!!!! EXCEPTION !!!!!!!!!")
        print(str(e))
        print(traceback.format_exc())

RedisCheck()
