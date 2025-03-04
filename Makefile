.PHONY: npm-build mesop

install:
	pip install -e .
	git lfs fetch --all
	cd wsd/annotate/lit && npm install

npm-build:
	cd wsd/annotate/lit && npm run build

annotate: npm-build
	mesop wsd/annotate/app.py
