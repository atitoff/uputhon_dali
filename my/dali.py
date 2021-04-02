import uasyncio as asyncio
import time


class Dali:
    def __init__(self, port_in: int, port_out: int):
        self._port_in = port_in
        self._port_out = port_out
        self.mqtt_client = None  # MQTT client
        self._receive_list = []
        self._receive_queue = asyncio.Event()
        DaliCommand.dali = self



    async def run(self, mqtt_client):
        self.mqtt_client = mqtt_client
        await self.mqtt_client.subscribe('dali/#', 1)
        asyncio.create_task(self._run())


    async def _run(self):
        while True:
            await self._receive_queue.wait()
            d = self._receive_list.pop(0)
            if len(self._receive_list) < 1:
                self._receive_queue.clear()
            print(time.time())
            print('awaited receive', d, '|  len', len(self._receive_list))
            await asyncio.sleep(2)


    def receive_from_mqtt(self, topic, msg):
        if len(self._receive_list) > 20:
            pass
        else:
            self._receive_list.append([topic, msg])
            self._receive_queue.set()


    def _byte_to_rmt(self, b):
        b = bytes(b)
        for i in range(16):
            if b[i // 8] & 1 << i % 8 != 0:
                self._dali_send_buffer[i * 2 + 2] = 1
                self._dali_send_buffer[i * 2 + 3] = 0
            else:
                self._dali_send_buffer[i * 2 + 2] = 0
                self._dali_send_buffer[i * 2 + 3] = 1

        print(self._dali_send_buffer)

        rmt = []

        compared = False
        for i in range(34):
            try:
                if compared:
                    compared = False
                    continue

                if self._dali_send_buffer[i] == self._dali_send_buffer[i+1]:
                    rmt.append(260)
                    compared = True
                else:
                    rmt.append(130)
            except:
                if i % 2:
                    rmt.append(130 * 5)
                else:
                    rmt.append(130)
                    rmt.append(130 * 4)
                pass
        return rmt



        rmt_show = []
        for i, _ in enumerate(rmt):
            if i % 2:
                rmt_show.append('0')
            else:
                rmt_show.append('1')

        print(rmt)
        print(rmt_show)


    async def receive(self):
        pass

    async def send_with_answer(self, command):
        # async def self.send(command)
        await asyncio.sleep_ms(17)
        return await self.receive()

    async def send_without_answer(self, command):
        # async def self.send(command)
        await asyncio.sleep_ms(17)
        return await self.receive()


class DaliCommand:
    dali: Dali

    @classmethod
    async def parse(cls, msg):
        try:
            topic = msg[0].split('/')
            if topic[1] == 'set_level':
                level =  int(topic[2])
                if 0 <= level < 64:
                    await cls.set_level(level)
            elif topic[1] == 'set_level_grp':
                grp = int(topic[2])
                if 0 <= grp < 64:
                    await cls.set_level(grp)
        except Exceptions:
            pass

    @classmethod
    async def set_level(cls, level):
        await cls.dali.send_without_answer(level)




class DaliFindNewModule:
    _f_address = 0
    _dali: Dali

    @classmethod
    async def start(cls, dali: Dali, short_address):
        cls._f_address = 0
        cls._dali = dali
        await cls._find(0xFFFFFF, 0x800000)
        # check
        if await cls._is_small(cls._f_address):
            cls._f_address -= 1
        if cls._f_address > 0:
            print('find: ', hex(cls._f_address))
            pass
            # todo write short_address

    @classmethod
    async def _is_small(cls, address):
        c = 0xFCFF00
        await asyncio.sleep_ms(10)
        return c < address

    @classmethod
    async def _find(cls, address, delta):
        if address == 0xFFFFFF and await cls._is_small(address) is False:
            return
        else:
            if delta < 1:
                cls._f_address = address
                return
            if await cls._is_small(address):
                await cls._find(address - delta, delta >> 1)
            else:
                await cls._find(address + delta, delta >> 1)


async def main():
    dali = Dali('', 1, 2)
    await DaliFindNewModule.start(dali, 16)
    # d._byte_to_rmt(b"\x00\xFF")
    # asyncio.create_task(dali.run())
    # while True:
    #     await asyncio.sleep(1)
    #     dali._receive_s.set()


if __name__ == '__main__':
    asyncio.run(main())



