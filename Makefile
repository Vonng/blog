default: dev

d:dev
dev:
	hugo serve

b:build
build:
	hugo build --minify

s: sync
sync:
	rsync -avz public/ cc:/www/vonng.com/

.PHONY: default d dev b build s sync
