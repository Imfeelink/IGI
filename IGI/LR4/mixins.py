from zipfile import ZipFile, ZIP_DEFLATED

#1
class LogMixin:
    def log(self, message: str):
        print(f"[LOG]: {message}")

class ZipArchieverMixin:
    #user defines archieve name
    def pack_to_zip(self, file_to_pack: str, archieve_name: str):
        with ZipFile(archieve_name, 'w', compression=ZIP_DEFLATED, compresslevel=3) as myzip:
            myzip.write(file_to_pack)

    def print_zip_info(self, archieve_name: str):
        with ZipFile(archieve_name, 'r') as myzip:
            print(myzip.infolist())