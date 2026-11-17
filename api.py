"""API for making churn predictions using a FastAPI server.

Add fastapi and uvicorn to your environment with:
    uv add fastapi uvicorn

To serve the API, run:
    uv run uvicorn api:app --reload
"""

from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

from prediction import make_prediction


# Field names match those used in the model training
# Aliases are more user-friendly names for the API
class Customer(BaseModel):
    tenure: int
    MonthlyCharges: float = Field(alias="monthly")
    TechSupport_yes: int = Field(alias="techsupport")


app = FastAPI()


@app.get("/", include_in_schema=False)
def home():
    """Serve a page with a churn probability bar."""
    return FileResponse("static/index.html")


@app.post("/predict")
def predict(customer: Customer):
    """Make a churn prediction for a customer."""
    prediction = make_prediction(**customer.model_dump())
    return {"prediction": prediction}


@app.get("/schema")
def predict_schema():
    """Describe the expected fields for /predict."""
    return Customer.model_json_schema()

# Health check endpoint
#@app.get("/health")
#def health_check(request: Request):
#    """Check if the API is running.
#
#    Browsers get a status page, other clients such as curl get JSON.
#    """
#    if "text/html" in request.headers.get("accept", ""):
#        return FileResponse("static/health.html")
#    return {"status": "ok"}

@app.get("/health")
def health_check():
    """ Check health of the API"""
    
    try:
        # Perform a simple prediction to check if the model is working
        test_customer = Customer(tenure=1, monthly=50.0, techsupport=1)
        prediction = make_prediction(**test_customer.model_dump())
        return FileResponse("static/health.html")
    except Exception as e:
        return {"status": "error", "message": str(e)}

