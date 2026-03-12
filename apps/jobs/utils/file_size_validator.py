def validate_image(file):
    max_size = 5 * 1024 * 1024  # 5MB

    if file.size > max_size:
        raise ValueError("Image size must be less than 5MB")

    allowed_types = ["image/jpeg", "image/png", "image/webp"]

    if file.content_type not in allowed_types:
        raise ValueError("Unsupported image format")