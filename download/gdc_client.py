from Crypto.Hash import MD5
import requests, json

class gdc_client:
    def __init__(self):
        self.data_url = "https://api.gdc.cancer.gov/data"
    
    def download_files(self, uuids: list, md5sums: list):
        len_ids = len(uuids)
        len_sums = len(md5sums)
        if len_ids <= 0:
            raise ValueError("Must provide at least one uuid")
        if  len_ids != len_sums:
            raise ValueError("The number of ids does not match the number of md5 sums provided")
        
        param = json.dumps({
            "ids": uuids
        })

        res = requests.post(
            self.data_url, 
            data=param, 
            headers={
                "Content-Type": "application/json"   
            })
        
        print(res.headers["Content-Disposition"])

