import datetime, re, os
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.forms import ValidationError
#media/featured_image/%Y/%m/%d/

def validate_filename(name) -> str:
    filename : str  = urlsafe_base64_encode(force_bytes(name.strip()[:-4]))
    extension : str = name.strip()[-4:]
    pattern = re.compile(r"^[A-Za-z0-9-]+$")
    print(filename)
    if not re.match(pattern, filename):
        raise ValidationError(("Name of the file should only contain alphanumerical characters or hyphens."), code="invalid filename")
    
    if len(filename) > 30:
        raise ValidationError(("Name of the file should be under 31 characters long."), code="too long filename")
    
    return filename+extension

def save_file(file):
    filename = validate_filename(file.name)
    today = datetime.datetime.now()
    date = today.strftime("%Y/%m/%d")
    path = f"media/featured_image/{date}"
    if not os.path.exists(path):
        os.makedirs(path)
        
    with open(f"{path}/{filename}","wb+") as image:
        for chunk in file.chunks():
            image.write(chunk)