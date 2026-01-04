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
    processed.save(output_buffer, format="JPEG")

    return output_buffer.getvalue()
