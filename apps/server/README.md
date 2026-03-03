# My FastAPI Server

This project is a FastAPI application designed for easy file import and data management. Below are the details on how to set up and run the application.

## Project Structure

```
server
├── Dockerfile
├── .dockerignore
├── requirements.txt
├── .env
├── docker-compose.yml
├── README.md
├── app
│   ├── __pycache__
│   ├── image
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   ├── database.py
│   ├── routes
│   │   └── __init__.py
│   └── utils
│       └── __init__.py
│   
│── scripts
│   └── start.sh
│── tests
│   └── test_main.py
```

## Requirements

Make sure to install the required dependencies listed in `requirements.txt`. You can do this by running:

```
pip install -r requirements.txt
```

## Docker Setup

To build and run the application using Docker, follow these steps:

1. Build the Docker image:

   ```
   docker build -t server .
   ```

2. Run the Docker container:

   ```
   docker run -d -p 8000:8000 server
   ```

Alternatively, you can use Docker Compose to manage the application:

```
docker-compose up --build
```

## Environment Variables

Create a `.env` file in the root directory to store your environment variables, such as database connection strings and other sensitive information.

## Running Tests

To run the tests, execute the following command:

```
pytest app/tests/test_main.py
```

## Usage

Once the application is running, you can access the API at `http://localhost:8000`. You can use tools like Postman or curl to interact with the endpoints.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.