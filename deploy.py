import os
import zipfile
from ftplib import FTP_TLS

# -------------------------------
# CONFIG
# -------------------------------
folder_to_zip = "src"           # Folder you want to zip
zip_filename = "app.zip"        # Output zip file
ftps_host = "your.ftps.server"  # FTPS server
ftps_port = 21                  # Usually 21 (explicit) or 990 (implicit)
username = "YOUR_USERNAME"
password = "YOUR_PASSWORD"

# -------------------------------
# ZIP THE FOLDER
# -------------------------------
def zip_folder(folder_path, output_path):
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, folder_path)
                zipf.write(file_path, arcname)
    print(f"Folder '{folder_path}' zipped into '{output_path}'")

zip_folder(folder_to_zip, zip_filename)

# -------------------------------
# CONNECT TO FTPS AND UPLOAD
# -------------------------------
ftps = FTP_TLS()
ftps.connect(ftps_host, ftps_port)
ftps.login(username, password)
ftps.prot_p()  # Secure the data connection

# Upload the file
with open(zip_filename, 'rb') as f:
    ftps.storbinary(f'STOR {zip_filename}', f)

ftps.quit()
print(f"File '{zip_filename}' uploaded to {ftps_host} successfully!")
