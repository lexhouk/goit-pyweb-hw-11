# Contacts API

## Deployment

```bash
$ git clone https://github.com/lexhouk/goit-pyweb-hw-11.git
$ cd goit-pyweb-hw-11
$ poetry install
```

## Usage

```bash
$ poetry shell
$ uvicorn main:app --host localhost --port 8000 --reload
```

All available endoints can be viewed in [Swagger UI](http://localhost:8000/docs) or [ReDoc](http://localhost:8000/redoc), and can only be tested in the former.
