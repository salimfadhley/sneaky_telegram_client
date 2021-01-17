Sneaky Telegram Client
----------------------

A tool for monitoring Telegram groups.

Setup
-----

Create a config file at `~/.config/simpleclient/config.yaml`. It should have the following content:

```yaml
app_api_id: <replace with your app telegram id>
app_api_hash: "<replace with your telegram app hash>"
phone_number: "<replace with your phone number>"
encryption_key: "<a random string>"
```

Build everything
```shell
docker-compose pull
docker-compose build
```

Run the app interactively:
```shell
docker-comose run client
```
Provide any login credentials necessary, and then quit the app by pressing CTRL-C

Run the app normally:
```shell
docker-compose up
```
