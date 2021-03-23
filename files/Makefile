.PHONY: test
all: extract transform load

extract:
	echo "Extracting concepts..."
	python3 ./extract_concepts.py -o ./tmp/

transform:
	echo "Filtering concepts...."
	python3 -u ./transform_concepts.py -o ./tmp/

delete:
	echo "Deleting concepts...."
	python3 ./delete_concepts.py -o ./tmp/

clean:
	rm ./tmp/*.json
