TAG = fuji_uploader

run: build
	docker run \
		--detach \
		--rm \
		-p 8888:8888 \
		-v /media/cympfh/HDCZ-UT/MyPictures/x100f/:/vol/ \
		-e FUJI_ROOT=/vol/ \
		-e FUJI_PORT=8888 \
		$(TAG)

build:
	docker build -t $(TAG) .
