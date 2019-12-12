import redis
import time
import traceback


def WorkCheck():
    try:

        # HERE SOME INITIAL WORK IS DONE THAT SCRIPTS 1 & 2 NEED TO WAIT FOR
        # IDs SERIAL PORTS
        # SAVE TO db

        r = redis.StrictRedis(host='localhost', port=6379)                # Connect to local Redis instance

        p = r.pubsub()                                                    # See https://github.com/andymccurdy/redis-py/#publish--subscribe

        print("Starting main scripts...")

        r.publish('CanalCEP', '18')                                # PUBLISH START message on startScripts channel

        print("Done")

    except Exception as e:
        print("!!!!!!!!!! EXCEPTION !!!!!!!!!")
        print(str(e))
        print(traceback.format_exc())
WorkCheck()
