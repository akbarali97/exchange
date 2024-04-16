build:
	docker build --no-cache -t exchange-app .
run: build
	docker run exchange-app python main.py