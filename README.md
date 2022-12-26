# GIF API

This is a simple API for working with GIFs. You can add, delete and view information on GIFs.
You can also add GIFs to trends, and get trends for a specific date.

This service does not provide storage for GIFs, but simply stores information about them.

The full documentation on the project API can be viewed in the [openapi.yaml](openapi.yaml) file.

# Setting up the development environment

1. Create `.env` file:
```
make env
```
2. Launch the database container:
```
make db
```
3. Apply the latest migrations:
```
make migrate
```
4. Install dependencies and activate virtual environment:
```
poetry install
poetry shell
```
5. Now you can work on the project:
```
make run
```

# Project launch

1. Create `.env` file:
```
make env
```
2. Create and launch service containers:
```
make up
```