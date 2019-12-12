import redis
import time
import traceback
import sys
import os
import signal
from multiprocessing import Process, Queue


def handler(signum, frame):
    raise Exception("Process is cancelled due to a timeout")

def baixaR():
    try:
        r = redis.StrictRedis(host='200.235.89.55', port=6379)                          # Connect to local Redis instance

        p = r.pubsub()                                                              # See https://github.com/andymccurdy/redis-py/#publish--subscribe
        p.subscribe('darBaixaR')                                                 # Subscribe to startScripts channel
        PAUSE = True

        while PAUSE:   
            #print("a")                                                             # Will stay in loop until START message received
            message = p.get_message()                                               # Checks for message
            if message:
                command = message['data']  
                if command != 1:                                         # Get data from message
                    print("recebi a mensagem" + command)
                    return command
            time.sleep(1)
    except Exception as e:
        print("!!!!!!!!!! EXCEPTION !!!!!!!!!")
        print(str(e))
        print(traceback.format_exc())

def PessoaR():
    try:
        r = redis.StrictRedis(host='200.235.89.55', port=6379)                          # Connect to local Redis instance

        p = r.pubsub()                                                              # See https://github.com/andymccurdy/redis-py/#publish--subscribe
        p.subscribe('respostaPessoa')                                                 # Subscribe to startScripts channel
        PAUSE = True

        while PAUSE:   
            #print("a")                                                             # Will stay in loop until START message received
            message = p.get_message()                                               # Checks for message
            if message:
                command = message['data']  
                if command != 1:                                         # Get data from message
                    print(command)
                    return command
            time.sleep(1)
    except Exception as e:
        print("!!!!!!!!!! EXCEPTION !!!!!!!!!")
        print(str(e))
        print(traceback.format_exc())

#essa funcao requisita o hash
def HashR():
    try:
        r = redis.StrictRedis(host='200.235.89.55', port=6379)                          # Connect to local Redis instance

        p = r.pubsub()                                                              # See https://github.com/andymccurdy/redis-py/#publish--subscribe
        p.subscribe('hashd')                                                 # Subscribe to startScripts channel
        PAUSE = True

        while PAUSE:   
            #print("a")                                                             # Will stay in loop until START message received
            message = p.get_message()                                               # Checks for message
            if message:
                command = message['data']  
                if command != 1:                                         # Get data from message
                    print("recebi a mensagem" + command)
                    return command
    except Exception as e:
        print("!!!!!!!!!! EXCEPTION !!!!!!!!!")
        print(str(e))
        print(traceback.format_exc())


def CepR():
    try:
        r = redis.StrictRedis(host='200.235.89.55', port=6379)                          # Connect to local Redis instance

        p = r.pubsub()                                                              # See https://github.com/andymccurdy/redis-py/#publish--subscribe
        p.subscribe('cepr')                                                 # Subscribe to startScripts channel
        PAUSE = True

        while PAUSE:   
            #print("a")                                                             # Will stay in loop until START message received
            message = p.get_message()                                               # Checks for message
            if message:
                command = message['data']  
                if command != 1:
                    print("recebi a mensagem" + command)                                         # Get data from message
                    # prints the retrieved data print(command)
                    return command
            time.sleep(1)
    except Exception as e:
        print("!!!!!!!!!! EXCEPTION !!!!!!!!!")
        print(str(e))
        print(traceback.format_exc())


def sendBaixa(line, r):
    print "esperando processo: " + str(os.getpid())
    signal.signal(signal.SIGALRM, handler)
    signal.alarm(10)
    try:
        message = line.strip("$order$")
        message = message.strip()
        #publica a mensagem no canal
        r.publish('canalBaixa', message)
        #espera a resposta do servidor
        
        var = baixaR()
        #coloca a resposta na fila
        if var:
            return var
        else:
            return "$TIMEOUT"
        
    except Exception, exc:
        print exc



def send(queue, line, r):
    #print line + "<<<<<<<"
    print "iniciando processo: " + str(os.getpid())


    #envia requisicao cep
    if "$cep$" in line:
        print "esperando processo: " + str(os.getpid())
        signal.signal(signal.SIGALRM, handler)
        signal.alarm(10)
        try:
            message = line.strip("$cep$")
            message = message.strip()
            #publica a mensagem no canal
            r.publish('CanalCEP', message)
            #espera a resposta do servidor
            
            var = CepR()
            #coloca a resposta na fila
            if var:
                queue.put("$cep$" + var)
            else:
                queue.put("$cep$TIMEOUT")
            return
        except Exception, exc:
            print exc

    #envia requisicao hash
    if "$order$" in line:
        print "esperando processo: " + str(os.getpid())
        signal.signal(signal.SIGALRM, handler)
        signal.alarm(20)
        try:
            message = line.strip("$order$")
            message = message.strip()
            #publica a mensagem no canal
            r.publish('canalHash', message)
            #espera a resposta do servidor
            
            var = HashR()
            #coloca a resposta na fila
            if var:
                queue.put("$hash$" + var)
            else:
                queue.put("$hash$TIMEOUT")
            return
        except Exception, exc:
            print exc

    if "$perfil$" in line:
        print "esperando processo: " + str(os.getpid())
        signal.signal(signal.SIGALRM, handler)
        signal.alarm(10)
        try:
            message = line.strip("$perfil$")
            message = message.strip()
            #publica a mensagem no canal
            r.publish('canalPessoas', message)
            #espera a resposta do servidor
            
            var = PessoaR()
            #coloca a resposta na fila
            if var:
                queue.put("$perfil$" + var)
            else:
                queue.put("$perfil$TIMEOUT")
            return
        except Exception, exc:
            print exc

            
    
    queue.put("$unknowndata$")






def WorkCheck():
    try:
        # HERE SOME INITIAL WORK IS DONE THAT SCRIPTS 1 & 2 NEED TO WAIT FOR
        # IDs SERIAL PORTS
        # SAVE TO db
        requisicao = "requisicao.dat"

        r = redis.Redis(host='200.235.93.96', port=6379)                # Connect to local Redis instance

        p = r.pubsub()   
        
        q = Queue()
        with open(requisicao, 'rb') as f:
            for line in f:
                if "$order$" in line:
                    status = sendBaixa(line, r)

        if status == "Sucesso":
            #creating processes
            processlist=[]
            rets=[]
            with open(requisicao, 'rb') as f:
                for line in f:
                    worker = Process(target=send, args=(q, line, r,))
                    worker.start()
                    processlist.append(worker)

            for p in processlist:
                ret = q.get()
                rets.append(ret)
            for p in processlist:
                p.join()

            print(rets)
            #cep = ""
            #for p in rets:
            #    if "$cep$" in p:
            #        cep = p.strip("$cep$")
            #        cep = cep.strip()

            #retrying for timeouts
            #retrylist = []
            #if "TIMEOUT" in cep:
            #    print "Retrying for CEP..."
            #    with open(requisicao, 'rb') as retry:
            #        for line in retry:
            #            if "$cep$" in line:
            #                worker = Process(target=send, args=(q, line, r,))
            #                worker.start()
            #                retrylist.append(worker)
                        
                
            #for p in retrylist:
            #    ret = q.get()
            #    for i in rets:
            #        if "$cep$" in i and "$cep$" in ret:
            #            rets.remove(i)
            #            rets.append(ret)
            #for p in retrylist:
            #    p.join()

            #print(rets)
        else:
            print status

        #results after the retries




        print("Done")
        
        


    except Exception as e:
        print("!!!!!!!!!! EXCEPTION !!!!!!!!!")
        print(str(e))
        print(traceback.format_exc())

WorkCheck()