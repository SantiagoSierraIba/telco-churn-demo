# Serving Predictions with FastAPI

In this session we look at the RESTful approach to APIs.


## Serving the Model

1. **In your Codespace** from the last session, add the API code:
    - Download `api.py` and `GUIDE.md` from the *10-12 Additional Materials* page on Canvas.
    - Drag both into the root of the repository next to `prediction.py`.
    - Right-click `GUIDE.md` and choose *Open Preview* to read this guide in the Codespace.
    - Update the fields in the `Customer` class if you changed the model features last session.

2. **In your Codespace**, add FastAPI and Uvicorn:
    ```bash
    uv add fastapi uvicorn
    ```

3. **In your Codespace**, start the API:
    ```bash
    uv run uvicorn api:app --reload
    ```
    - Click *Open in Browser* in the pop-up for port 8000.
    Or open the *Ports* tab and click the globe icon for port 8000.
    - The page shows `{"detail":"Not Found"}`. There is nothing at the root of the API.

4. **In the browser**, add `/docs` to the end of the address.
    - Click `POST /predict` and then *Try it out*.
    - Use this as the *Request body* and click *Execute*:
        ```json
        {"tenure": 12, "monthly": 70.5, "techsupport": 0}
        ```
    - Check the response code (`200`) and the churn probability in the response body.
    - Change `12` to `"twelve"` and click *Execute* again.
    - Check the response code (`422`) and the error message.

5. **In the browser**, replace `/docs` with `/schema` to see the fields the API expects.

6. **In your Codespace**, open a second terminal and call the API with `curl`:
    ```bash
    curl -X POST http://127.0.0.1:8000/predict \
      -H "Content-Type: application/json" \
      -d '{"tenure": 12, "monthly": 70.5, "techsupport": 0}'
    ```

7. **In your Codespace**, stop the API with `Ctrl+C` in the first terminal.
    - Check and format your code:
        ```bash
        uvx ruff check --fix
        uvx ruff format
        ```
    - **Commit and Sync** all your changes!
    - Pushing also runs your Azure deployment workflow. It fails if you deleted your Function App.


## Exercise

* Add a `GET /health` endpoint that returns `{"status": "ok"}`.
