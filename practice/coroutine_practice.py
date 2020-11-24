import asyncio, time

async def say_after(delay, what):
    await asyncio.sleep(delay)
    print(what)

async def main():
    print(f"started at {time.strftime('%X')}") #format을 이렇게 쓰기도 한다.
    await say_after(1, 'hello')
    await say_after(2, 'world1')
    await say_after(3, 'world2')
    await say_after(4, 'world3')
    await say_after(5, 'world4')
    print(f"finished at {time.strftime('%X')}")

asyncio.run(main())