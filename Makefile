venv/bin/activate:
	virtualenv -p python3.6 venv
	. venv/bin/activate; pip install -r requirements.txt

.PHONY: clean
clean:
	$(RM) -r venv __pycache__
