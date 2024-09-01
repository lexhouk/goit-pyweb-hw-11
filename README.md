# Contacts API

## Deployment

```bash
$ git clone https://github.com/lexhouk/goit-pyweb-hw-11.git
$ cd goit-pyweb-hw-11
$ poetry install
$ alembic upgrade head
```

## Usage

```bash
$ echo 'your database user password' > .secret
$ docker run --name lexhouk-hw-11 -p 5432:5432 -e "POSTGRES_PASSWORD=$(cat .secret)" -d postgres
$ poetry shell
$ python main.py
```

All available endoints can be viewed in [Swagger UI](http://localhost:8000/docs) or [ReDoc](http://localhost:8000/redoc), and can only be tested in the former.
