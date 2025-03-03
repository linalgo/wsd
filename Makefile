.PHONY: npm-build mesop

npm-build:
	cd wsd/annotate/lit && npm run build

mesop: npm-build
	mesop wsd/annotate/app.py
