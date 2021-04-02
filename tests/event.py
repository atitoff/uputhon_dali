import uasyncio as asyncio

event = asyncio.Event()

async def waiter():
    print('waiting for it ...')
    await event.wait()
    print('... got it!')

async def main():
    # Create an Event object.


    # Spawn a Task to wait until 'event' is set.
    asyncio.create_task(waiter())

    # Sleep for 1 second and set the event.
    await asyncio.sleep(1)
    event.set()
    await asyncio.sleep(1)


asyncio.run(main())
