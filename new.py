import asyncio

async def get_weather ():
    await asyncio.sleep (1)
    return {" temp_c ": 42, " city ": " Peshawar "}

async def get_news ():
    await asyncio.sleep (1)
    return {" headline ": "AI Bootcamp Day 10"}

async def run_agent ( query ):
    weather , news = await asyncio.gather (
    get_weather () , get_news ()
    )
    return {" query ": query , " answer ": f"{ weather [' city ']}: { weather [' temp_c ']}C. "f" News : { news [' headline ']}"}

print ( asyncio .run( run_agent (" What 's happening ?")))
