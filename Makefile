default: dev

d:dev
dev:
	hugo serve

b:build
build:
	hugo --gc --minify --cleanDestinationDir --baseURL "https://vonng.com/"

s: sync
sync: build
	@! rg -q '(<link>|href="?|content="?)https?://(localhost|127\.0\.0\.1):[0-9]+' \
		public --glob '*.html' --glob '*.xml'
	rsync -avz public/ jp:/data/web/vonng.com/

.PHONY: default d dev b build s sync
