import time
import asyncio
import os


async def k():
    cmd = [
        "curl",
        "-X",
        "POST",
        (os.environ.get("PUBLIC_URL"))
    ]
    while True:
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        time.sleep(1800)
        await process.communicate()


loop = asyncio.get_event_loop()
loop.run_until_complete(k())
