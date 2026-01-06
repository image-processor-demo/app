from mangum import Mangum
from app.main import app

# Configure Mangum to base64 encode binary responses for API Gateway
handler = Mangum(
    app, 
    lifespan="off",
    api_gateway_base_path="/",
)