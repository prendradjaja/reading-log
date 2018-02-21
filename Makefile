.PHONY: run run-diff
run-diff:
	touch out
	mv out prev
	python3 main.py | tee out
	diff -u out prev

run:
	python3 main.py | tee out
