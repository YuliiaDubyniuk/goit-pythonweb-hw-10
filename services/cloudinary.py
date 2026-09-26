import os
import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv


load_dotenv()


cloudinary.config(
    cloud_name=os.environ.get("CLOUDINARY_NAME"),
    api_key=os.environ.get("CLOUDINARY_API_KEY"),
    api_secret=os.environ.get("CLOUDINARY_API_SECRET"),
    secure=True,
)


def upload_avatar(file, username: str) -> str:
    public_id = f"RestApp/{username}"

    result = cloudinary.uploader.upload(
        file.file,
        public_id=public_id,
        overwrite=True,
    )

    src_url = cloudinary.CloudinaryImage(
        public_id
    ).build_url(
        width=250,
        height=250,
        crop="fill",
        version=result.get("version"),
    )

    return src_url