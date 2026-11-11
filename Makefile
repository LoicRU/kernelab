.PHONY: lint clean

lint:
	python3 tools/lint.py

clean:
	rm -rf build iso
