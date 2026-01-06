from mangum import Mangum
from app.main import app
import base64
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handler(event, context):
    """
    Custom handler that wraps Mangum and ensures binary responses
    are properly flagged as base64 encoded
    """
    asgi_handler = Mangum(app, lifespan="off")
    response = asgi_handler(event, context)
    
    # Check if this is an image response
    content_type = response.get("headers", {}).get("content-type", "")
    
    if content_type.startswith("image/"):
        body = response.get("body", "")
        
        # Check if body is bytes (binary) - if so, we need to base64 encode it
        if isinstance(body, bytes):
            logger.info(f"Body is bytes, encoding to base64. Size: {len(body)}")
            response["body"] = base64.b64encode(body).decode("utf-8")
            response["isBase64Encoded"] = True
            logger.info(f"Encoded body size: {len(response['body'])}")
        else:
            # Body is already a string, just mark it as base64
            logger.info(f"Body is string, marking as base64. Size: {len(body)}")
            response["isBase64Encoded"] = True
    
    return response