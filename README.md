# Telco Churn Predictions

This repository contains code to build and deploy a machine learning
model that predicts customer churn for a telecommunications company
using the Marimo framework. The model is trained on the well known
IBM Telco Customer Churn dataset.


## The Model

The model is a simple logistic regression model built using `scikit-learn`.

The model currently uses the following features:
- `tenure`: Number of months the customer has stayed with the company.
- `MonthlyCharges`: The amount charged to the customer monthly.
- `TechSupport_yes`: Binary indicator of whether the customer has tech support.

We recommend looking into additional features and engineering new ones to
improve model performance. There are other possible issues to explore, including
model choice, leakage, and others.

The model is built and trained using `notebooks/telco_marimo.py`. The model is
saved in the `models/` directory, with the scaler and model bundled together
using `joblib`.

An example prediction can be found in `prediction.py`.

## CI Pipeline

There is a CI pipeline set up using GitHub Actions that runs tests
on every push and pull request. The tests are located in the `tests/`
directory and can be run locally using `pytest`.

## Deploying to Serverless

The saved model can be deployed to an Azure Function with the following
steps:


1. **In your Codespace**, install the Azure Functions extension:
    - Open the Extensions view in the left sidebar.
    - Search for "Azure Functions" and install the extension by Microsoft.

2. **In your Codespace**, create the function:
    - Open the Command Palette (`Ctrl+Shift+P`).
    - Type and select *Azure Functions: Create Function*
         - Do not select the "...in Azure..." command
    - Select the root folder of the project (should be the default).
    - Select *Python* as the language.
    - Select *HTTP trigger* as the template.
    - Provide a name (without spaces or special characters) e.g. predict.
    - Select *FUNCTION* as the authorization level.
    - **Do not** *overwrite* the `.gitignore` file.

3. **In your Codespace**, wait some time for the function to be created. Then:
    - Add azure.functions to your env and update the `requirements.txt` file for Azure.
    Azure installs packages from `requirements.txt` with `pip`. It doesn't read `uv.lock`.
        ```bash
        uv add azure-functions
        uv pip freeze > requirements.txt
        ```
    - Edit the `function_app.py` file
        - Add an import: `from prediction import make_prediction`
        - Replace the line `name = req.params.get('name')`,
        using the same approach to get input data for prediction.
            - You'll need tenure, monthly bill and tech support status.
            - It is up to you how you name these but simple names are best.
            - The variable name (on the left) is internal to the function,
            while the string name (on the right) is what the user will need to provide.
                ```python
                tenure = req.params.get("tenure")
                monthly = req.params.get("monthly")
                techsupport = req.params.get("techsupport")
                ```
        - Remove the entire `if not name:` block. We aren't supporting JSON input here.
        - Change `if name:` to `if tenure and monthly and techsupport:`
        - Inside that `if` block, call the `make_prediction` function, passing tenure, monthly and techsupport
        as keyword arguments following the column names used by the model.
        Query parameters arrive as text, so convert each one with `float()`:
            ```python
            prediction = make_prediction(
                tenure=float(tenure),
                MonthlyCharges=float(monthly),
                TechSupport_yes=float(techsupport),
            )
            ```
        - Change the `f""` response to return the prediction result instead of a name.
        `{prediction:.1%}` shows it as a percentage.
        - Change the message in the `else` block to ask for tenure, monthly and techsupport.
    - Check and format your code:
        ```bash
        uvx ruff check --fix
        uvx ruff format
        ```
    - Your `function_app.py` should now look like this, with the name you chose in step 2 instead of `predict`:
        ```python
        import logging

        import azure.functions as func

        from prediction import make_prediction

        app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)


        @app.route(route="predict")
        def predict(req: func.HttpRequest) -> func.HttpResponse:
            logging.info("Python HTTP trigger function processed a request.")

            tenure = req.params.get("tenure")
            monthly = req.params.get("monthly")
            techsupport = req.params.get("techsupport")

            if tenure and monthly and techsupport:
                prediction = make_prediction(
                    tenure=float(tenure),
                    MonthlyCharges=float(monthly),
                    TechSupport_yes=float(techsupport),
                )
                return func.HttpResponse(f"Churn probability: {prediction:.1%}")
            else:
                return func.HttpResponse(
                    "This HTTP triggered function executed successfully. Pass tenure, monthly and techsupport in the query string for a churn prediction.",
                    status_code=200,
                )
        ```
    - **Commit and Sync** all your changes!

4. **In the Azure Portal**, create an Azure Function App.
    - Choose *Flex Consumption*.
    - Select your existing **Resource Group** (the one you created earlier in this session).
    - Choose a unique **name** for your Function App.
    - Set the **Region** to a supported student region (e.g. *Switzerland North*).
    Azure for Students only allows about five regions. They differ from person to person.
    To see yours, search for *Policy* in the portal and open *Assignments*.
    Then open *Allowed resource deployment regions* and look at *Allowed locations*.
    - Choose *Python* *3.12* as the **runtime** stack and **version** (the same as this Codespace).
    - Choose the smallest **instance size** (e.g. *512MB*).
    - If given the option, *disable* **Zone Redundancy**.
    - Use an existing **Storage Account** or create a new one.
    - *Configure* **diagnostic settings** *later*.
    - Leave the *defaults* for OpenAI (disable)
    - Leave the *defaults* for Networking (public enabled, virtual disabled).
    - Leave the *defaults* for Monitoring (enable in a supported region).
    - Leave the *defaults* for Durable Functions (unticked).
    - Enable **Continuous Deployment** and point to your repo, signing in to GitHub.
    - Leave **Basic authentication** disabled (the default). GitHub Actions signs in to Azure with an identity instead.
    - Leave the *defaults* for Authentication (secrets) and tags (none).
    - Wait until the deployment completes.

5. **In the Codespace**, in **Source Control**, click on the *Pull* icon,
or choose it through the `...` menu.
    - Ensure you have the latest changes from GitHub (a new workflow file)
        - If not, click *Pull* again until you do.
    - Edit the **newly** created workflow file in `.github/workflows/`
    i.e. not the existing `quality.yaml`. It is named after your Function App, e.g. `main_<your-app-name>.yml`.
        - Find the `Install dependencies` step and add `-t .` to the command:
        
            ```yaml
            run: pip install -r requirements.txt -t .
            ```
    - **Commit and Sync** all your changes!

6. **On your repository on GitHub**, go to the *Actions* tab.
    - Wait for the *Build and deploy Python project to Azure Function App* workflow to complete successfully.
    The *Code Quality* workflow runs as well.
    - Azure started a first run when it created your app. That run doesn't have the `-t .` change,
    so your function only appears after the run from your own push.

7. **In the Azure Portal**, navigate to your Function App.
    - Select your function from the list.
    - Test the function using the *Test/Run* option in the Function
        - Under *Query*, provide the required parameters: tenure, monthly and techsupport (1 for yes, 0 for no).
        - Run the test and check the output for the prediction result, e.g. `Churn probability: 12.3%`.

