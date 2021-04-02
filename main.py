import uasyncio as asyncio
from my.mqtt import MQTT, MqttLog
from my.dali import Dali
import time

dali = Dali(1, 2, topic_index=b'ha')



def mqtt_callback(topic, msg, retained):
    if topic.startswith(b'dali/'):
        dali.receive_from_mqtt(topic, msg)
    print(topic, msg, retained)


async def mqtt_conn_handler(client):
    await client.subscribe('dali/#', 1)

mqtt = MQTT(host='192.168.1.197', user='alex', password='bh0020', subs_cb=mqtt_callback, conn_handler=mqtt_conn_handler, debug=True)
# mqtt = MQTT(host='192.168.1.72', user='alex', password='bh0020', subs_cb=mqtt_callback, conn_handler=mqtt_conn_handler, debug=True)

log = MqttLog(mqtt.client)

async def main():
    await mqtt.connect()
    await dali.run(mqtt.client)
    await asyncio.sleep(1)

    while True:
        t = time.time()
        await mqtt.client.publish('dali/ha/set_level/32', b'\23', qos=0)
        print(t)
        await asyncio.sleep(2)



try:
    asyncio.run(main())
finally:
    mqtt.client.close()  # Prevent LmacRxBlk:1 errors
