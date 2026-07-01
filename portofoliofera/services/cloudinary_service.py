import os
import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv

load_dotenv()

cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key=os.getenv('CLOUDINARY_API_KEY'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET'),
    secure=True
)


def upload_image(file, folder='portfolio'):
    """Upload file ke Cloudinary, return URL."""
    result = cloudinary.uploader.upload(
        file,
        folder=folder,
        resource_type='image',
        transformation=[{'quality': 'auto', 'fetch_format': 'auto'}]
    )
    return result.get('secure_url')


def delete_image(public_id):
    """Hapus gambar dari Cloudinary."""
    cloudinary.uploader.destroy(public_id)


def get_public_id(url):
    """Ambil public_id dari URL Cloudinary."""
    if not url or 'cloudinary' not in url:
        return None
    parts = url.split('/')
    folder_and_file = '/'.join(parts[-2:])
    return folder_and_file.split('.')[0]# cloudinary service
