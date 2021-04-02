import uasyncio as asyncio
from micropython_mqtt_as.mqtt_as import MQTTClient
from micropython_mqtt_as.config import config
from sys import platform


class MQTT:
    def __init__(self, host, user, password, subs_cb, conn_handler, debug=False):
        config['subs_cb'] = subs_cb
        config['connect_coro'] = conn_handler
        config['server'] = host
        config['user'] = user
        config['password'] = password
        if platform == "linux":
            config["client_id"] = "linux"
        MQTTClient.DEBUG = debug  # Optional: print diagnostic messages
        self.client = MQTTClient(**config)  # Using dict to stay compatible to upstream.

    async def connect(self):
        await self.client.connect()


class MqttLog:
    DEBUG = 0
    INFO = 1
    WARNING = 2
    ERROR = 3
    CRITICAL = 4

    def __init__(self, client, log_level=0):
        self._client = client
        self._log_level = log_level

    def info(self, s):
        level = 1
        if self._log_level <= level:
            self._send('log/info', 'INFO')


    def _send(self, topic, msg):
        asyncio.create_task(self._client.publish(topic, msg, qos=0))
