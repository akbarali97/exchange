build:
	docker build --no-cache -t exchange-app .
run: build
	docker run -it exchange-app