## Usage with ***pip***
1. Go to the project folder
    ```sh
    cd PayersPointsApi
    ```
2. Create a virtual environment
    ```sh
    python -m venv venv
    ```
3. Activate the created virtual environment:
    - `venv\Scripts\activate.bat` - for Windows;
    
    - `source venv/bin/activate` - for Linux & MacOS.
4. Install dependencies
    ```sh
    pip install -r requirements.txt
    ```
5. Go to the folder next to **manage.py***
    ```sh
    cd DjangoApp
    ```
6. Start a local server *Django*
    ```sh
    python manage.py runserver
    ```

## Usage with ***Docker***
1. Go to the project folder
    ```sh
    cd PayersPointsApi
    ```
2. Build an image based on *Dockerfile*
    ```sh
    docker build . -t transactions_api
    ```
3. Launch container
    ```sh
    docker run -p -t 8000:8000 transactions_api
    ```

## Active points

1. /api/transactions/
2. /api/balance/
3. /api/spend-points/
