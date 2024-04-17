# To Run the script

```
make run
```

if you don't have make installed, then run

To build docker container
```
docker build --no-cache -t exchange-app .
```

And to run
```
docker run -it exchange-app
```

# Sample Response

```
price to Buy <quantity> bitcoins: <amount>
price to Sell <quantity> bitcoins: <amount>
```