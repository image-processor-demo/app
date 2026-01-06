from PIL import Image, ImageFilter
import io

def process_image_bytes(image_bytes: bytes) -> bytes:
    """
    Pure function:
    input  -> raw image bytes
    output -> abstract edge-detected image bytes
    """
    image = Image.open(io.BytesIO(image_bytes))
    
    # Example processing (replace later with ML / AI)
    processed = ( 
        image.convert("RGB") 
            .resize((512, 512)) 
            .filter(ImageFilter.CONTOUR) 
    )
    
    output_buffer = io.BytesIO()
    processed.save(output_buffer, format="JPEG", quality=85)  # Added quality parameter
    output_buffer.seek(0)  # Reset buffer position
    
    result_bytes = output_buffer.getvalue()
    
    # Validate output
    if not result_bytes or len(result_bytes) == 0:
        raise ValueError("Image processing resulted in empty output")
    
    return result_bytes