TAG = fuji_uploader

run: build
	docker run --rm -p 8888:8888 $(TAG)

build:
	docker build -t $(TAG) .
