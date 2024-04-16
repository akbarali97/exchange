build:
	docker build --no-cache -t exchange-app .
run-all: build
	docker run exchange-app python main.py --show-log --exchanges a,b,c
run: build
	docker run exchange-app python main.py
run-log: build
	docker run exchange-app python main.py --show-log