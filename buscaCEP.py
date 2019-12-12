import redis
import time
import traceback

def pesquisar_registro( arq, txt ):
    cep = ""
    registro = ""
    with open( arq, 'r' ) as a:
        for linha in a:
            
            linha = linha.strip()
            if cep == "":
                #print (linha, txt)
                if txt in linha.split("\n"):
                    cep = linha
                    #print cep
            else:
                registro = linha
                return registro
                break
                
    return "CEP inexistente";


def RedisCheck():
    try:
        r = redis.StrictRedis(host='200.235.93.96', port=6379)                          # Connect to local Redis instance

        p = r.pubsub()                                                              # See https://github.com/andymccurdy/redis-py/#publish--subscribe
        p.subscribe('CanalCEP')                                                 # Subscribe to startScripts channel
        PAUSE = True

        while PAUSE:                                                                # Will stay in loop until START message received
            #print("Waiting For redisStarter...")
            message = p.get_message()                                               # Checks for message
            if message:
                command = message['data']                                       # Get data from message
            
                if command != 1:                                      				# Checks for START message
                    response = pesquisar_registro('cep.txt', command)
                    WorkCheck(response)
                    print ('CEP recebido: ', command)
                    print pesquisar_registro("cep.txt", command)
                    

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

        r = redis.StrictRedis(host='200.235.89.55', port=6379)                # Connect to local Redis instance

        p = r.pubsub()                                                    # See https://github.com/andymccurdy/redis-py/#publish--subscribe
        
        r.publish('cepr', responset)                                # PUBLISH START message on startScripts channel
        #print (responset)
    except Exception as e:
        print("!!!!!!!!!! EXCEPTION !!!!!!!!!")
        print(str(e))
        print(traceback.format_exc())

RedisCheck()