import datetime, re, os
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.forms import ValidationError
#media/featured_image/%Y/%m/%d/

def validate_filename(name) -> str:
    filename : str = name.strip()[:-4]
    pattern = re.compile(r"^[A-Za-z0-9-]+$")

    if not re.match(pattern, filename):
        raise ValidationError(("Name of the file should only contain alphanumerical characters or hyphens."), code="invalid filename")
    
    if len(filename) > 100:
        raise ValidationError(("Name of the file should be under 101 characters long."), code="too long filename")
    
    encoded_filename : str  = urlsafe_base64_encode(force_bytes(name.strip()[:-4]))
    extension : str = name.strip()[-4:]
    
    return encoded_filename+extension

def save_file(file, slug, existing = False):
    name = file.name
    if existing:
        name = os.path.basename(file.name)
    filename = validate_filename(name)
    today = datetime.datetime.now()
    date = today.strftime("%Y/%m/%d")
    path = f"media/featured_image/{date}/{slug}"
    if not os.path.exists(path):
        os.makedirs(path)
        
    final_path = f"{path}/{filename}"
        
    with open(final_path,"wb+") as image:
        for chunk in file.chunks():
            image.write(chunk)
    
    return final_path

def save_avatar(file, username, existing = False):
    name = file.name
    if existing:
        name = os.path.basename(file.name)
    filename = validate_filename(name)
    path = f"media/avatar/{username}"
    if not os.path.exists(path):
        os.makedirs(path)
        
    final_path = f"{path}/{filename}"
        
    with open(final_path,"wb+") as image:
        for chunk in file.chunks():
            image.write(chunk)
            
    return final_path
