# Dashboards and Documentation

In this session we build a dashboard for our prediction API and publish documentation as a website.


## Building the Dashboard

1. **In your Codespace** from the last session:
    - Right-click `DASH.md` and choose *Open Preview* to read this guide in the Codespace.
    - Update the inputs and the `payload` in `dashboard.py` if you changed the model features.

2. **In your Codespace**, add Streamlit and Requests:
    ```bash
    uv add streamlit requests
    ```

3. **In your Codespace**, start the API from the last session:
    ```bash
    uv run uvicorn api:app --reload
    ```

4. **In your Codespace**, open a second terminal and start the dashboard:
    ```bash
    uv run streamlit run dashboard.py
    ```
    - Streamlit asks for an email address the first time. Press `Enter` to skip it.
    - Click *Open in Browser* in the pop-up for port 8501.
    Or open the *Ports* tab and click the globe icon for port 8501.

5. **In the browser**, change the tenure, the monthly charges and the tech support toggle.
    - The dashboard calls the API after every change and shows the new prediction.
    - Stop the API with `Ctrl+C` in the first terminal and change a value again.
    - The dashboard shows an error. Start the API again.


## Connecting to the Azure Function

Skip this part if you deleted your Function App.

1. **In the Azure Portal**, open your Function App and click the name of your function.
    - Click *Get function URL*.
    - Copy the address next to *default (Function key)*.

2. **In your Codespace**, create a file called `.env` in the root of the repository:
    ```text
    PROD_API=<paste the address here>
    ```
    - The address contains your function key. Anyone who has it can call your function.
    - `.env` is listed in `.gitignore`. Git never commits it.

3. **In your Codespace**, stop the dashboard with `Ctrl+C` in the second terminal.
    - Start it again with the `.env` file:
        ```bash
        uv run --env-file .env streamlit run dashboard.py
        ```
    - `dashboard.py` reads the address into `PROD_API`.
    - Nothing changes on screen yet. The dashboard still calls the local API.


## Publishing Documentation

1. **In your Codespace**, stop the API and the dashboard with `Ctrl+C`.
    - Zensical previews the site on port 8000. The API uses the same port.

2. **In your Codespace**, add Zensical and create a site:
    ```bash
    uv add --dev zensical
    uv run zensical new .
    ```
    - This creates `zensical.toml`, a `docs` folder and a workflow in `.github/workflows/docs.yml`.
    - Move `docs.yml` from Canvas into `.github/workflows` and replace the file that Zensical created.

3. **In your Codespace**, preview the site:
    ```bash
    uv run zensical serve
    ```
    - Click *Open in Browser* in the pop-up for port 8000.
    - Change some text in `docs/index.md` and save it. The page reloads.
    - Change `site_name` in `zensical.toml` to a name for your site.

4. **On GitHub**, open the *Settings* of your repository and then *Pages*.
    - Set *Source* to *GitHub Actions*.
    - GitHub Pages needs a public repository on a free account.

5. **In your Codespace**, stop the preview with `Ctrl+C`.
    - Check and format your code:
        ```bash
        uvx ruff check --fix
        uvx ruff format
        ```
    - **Commit and Sync** all your changes!

6. **On GitHub**, open the *Actions* tab and wait for the *Documentation* workflow to finish.
    - Your site is at `https://<your-username>.github.io/<your-repository>/`.


## Exercises

* Change the dashboard to call your Azure Function with `fetch_prediction_from_production`.
The function returns text and not JSON. Show it with `response.text` and remove the `st.json` line.
Some calls take several seconds while Azure starts your function.
* Add a page to your site that explains how to call the `/predict` endpoint.
