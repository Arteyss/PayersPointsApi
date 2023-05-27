# Spend points api

When a user spends points, they don't know or care which payer the points come from. But, our accounting team does care how the points are spent. There are two rules for determining what points to "spend" first:
- Oldest points to be spent first (oldest based on transaction timestamp, not the order they’re received)
- No payer's points to go negative.

### Api routes:
- Add transactions for a specific payer and date.
- Spend points using the rules above and return a list of `{ "payer": <string>, "points": <integer> }` for each call.
- Return all payer point balances.

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

## Example
Initial transactions:
- `{ "payer": "DANNON", "points": 1000, "timestamp": "2020-11-02T14:00:00Z" }`
- `{ "payer": "UNILEVER", "points": 200, "timestamp": "2020-10-31T11:00:00Z" }`
- `{ "payer": "DANNON", "points": -200, "timestamp": "2020-10-31T15:00:00Z" }`
- `{ "payer": "MILLER COORS", "points": 10000, "timestamp": "2020-11-01T14:00:00Z" }`
- `{ "payer": "DANNON", "points": 300, "timestamp": "2020-10-31T10:00:00Z" }`

Then you call your spend points route with the following request:

```json
{ "points": 5000 }
```

The expected response from the spend call would be:

```json
[
    { "payer": "DANNON", "points": -100 },
    { "payer": "UNILEVER", "points": -200 },
    { "payer": "MILLER COORS", "points": -4,700 }
]
```
A subsequent call to the points balance route, after the spend, should returns the following results:

```json
{
"DANNON": 1000,
"UNILEVER": 0,
"MILLER COORS": 5300
}
```
