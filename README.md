Dotcoin
-----

In this assignment, you will build a small ledger-based blockchain similar to Bitcoin. The original Bitcoin [whitepaper](https://Bitcoin.org/Bitcoin.pdf) is an excellent resource however the tutorial [Naivecoin: a tutorial for building a cryptocurrency](https://lhartikk.github.io/) provides a simpler but yet comprehensive overview of the most important Bitcoin concepts.

You are tasked to implement a Python version of Naivecoin called *Dotcoin*. The goal is not solely to translate this code into python but rather understand in details the Bitcoin mechanics. You code must work but your grade will also depend on your understanding of the concepts. You will likely be asked to explain your code during during a live meeting with the instructor. 

The blockchain will run within a [Docker container](https://thierrysans.me/CSCD27/doc/docker/) and use [Python Flask](https://palletsprojects.com/p/flask/) for the HTTP server (instead of Node Express in the tutorial) and the [Python Libsodium Library (PyNaCl)](https://pynacl.readthedocs.io/en/latest/) for the cryptography primitives.

Build the docker image (first time only)

```
docker build -t dotcoin .
```

To run your code in debug mode (the server will automatically reload when the source files change)

```
docker run --rm -p 5000:5000 -v $(pwd)/src:/shared dotcoin flask --app dotcoin.py --debug run
```

```
docker run --rm -p 5000:5000 -v $(pwd)/src:/shared dotcoin flask --app dotcoin.py --debug run --host=0.0.0.0
```

Type `ctrl-c` to stop the server. 





##### React as frontend + Flask as backend, all serve through Flask

your url+port is also repersenting the backend url+port since I chosed to compile the react frontend and serve it throught flask, the reason is:

- everything will still in docker container (requirement)
- each docker instance will only output one ip 
- each ip repersent one node