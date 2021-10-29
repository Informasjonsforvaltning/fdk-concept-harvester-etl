.PHONY: test
all: extract transform load

extract:
	echo "Extracting concepts..."
	python3 ./extract_concepts.py -o ./tmp/

transform:
    echo "Transforming concepts..."
    python3 -u ./transform_concepts.py -o ./tmp/

load:
    echo "Loading new/deleting old concepts..."
    python3 -u ./load_concepts.py -o ./tmp/

clean:
	rm ./tmp/*.json
