import asyncio
import aio_pika


async def main(loop):
    connection = await aio_pika.connect_robust("amqp://rabbit/", loop=loop)

    routing_key = "test_queue"

    channel = await connection.channel()  # type: aio_pika.Channel

    await channel.default_exchange.publish(
        aio_pika.Message(body="Hello {}".format(routing_key).encode()),
        routing_key=routing_key,
    )
    print("Howdy!")

    await connection.close()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
    loop.close()
