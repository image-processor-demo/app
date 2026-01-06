from mangum import Mangum
from app.main import app
import json

def handler(event, context):
    """
    Custom handler that wraps Mangum and ensures binary responses
    are properly flagged as base64 encoded
    """
    # Create Mangum handler
    asgi_handler = Mangum(app, lifespan="off")
    
    # Get response from Mangum
    response = asgi_handler(event, context)
    
    # If response is an image, ensure it's marked as base64 encoded
    if response.get("headers", {}).get("content-type", "").startswith("image/"):
        response["isBase64Encoded"] = True
    
    return response