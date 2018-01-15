all: install compile run benchmark

install:
	pip3 install -r requirements.txt
	go get -d ./src/...
	mkdir -p ./build

compile:
	# go
	go build -o build/godistance.so -buildmode=c-shared src/distance.go
	# rust unoptimized
	rustc --crate-type dylib -o build/rustdistance_default.so src/distance.rs
	# rust optimized
	rustc --crate-type dylib -o build/rustdistance_optimized.so -O src/distance.rs

run:
	python3 src/distance.py

benchmark:
	pytest src/test_distance.py

clean:
	rm -rf build
