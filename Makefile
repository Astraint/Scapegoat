all: build

build:
	@cd ___python && python3 build.py && cd ..

clean:
	rm -rf __build/