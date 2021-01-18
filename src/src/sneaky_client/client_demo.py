from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.tl.types import Channel

from sneaky_client.client import get_telegram_client


def get_query(client):
    async def query():
        channel: Channel = await client.get_entity("GreatAwakeningChannel")
        result = await client(
            JoinChannelRequest(await client.get_entity("GreatAwakeningChannel"))
        )
        print(result)

    return query


def main():
    with get_telegram_client() as client:

        # Run the client until Ctrl+C is pressed, or the client disconnects
        print("(Press Ctrl+C to stop this)")
        client.loop.run_until_complete(get_query(client)())


if __name__ == "__main__":
    main()
