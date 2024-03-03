import json
import requests

"""
URLS
Presiden/WP: https://sirekap-obj-data.kpu.go.id/pemilu/ppwp.json
Rekap: 
 - sample: https://sirekap-obj-data.kpu.go.id/pemilu/hhcw/ppwp/11/1105/110507.json
 including image:
 - https://sirekap-obj-data.kpu.go.id/pemilu/hhcw/ppwp/11/1105/110507/1105072002/1105072002001.json

 
 Wilayah: 
 - https://sirekap-obj-data.kpu.go.id/wilayah/pemilu/ppwp/{id wilayah by /}.json
 - https://sirekap-obj-data.kpu.go.id/wilayah/pemilu/ppwp/11/1105.json

 
Gambar:
https://sirekap-obj-formc.kpu.go.id/2e38/pemilu/ppwp/11/05/07/20/02/1105072002001-20240215-022619--f005fee9-5a36-4a4e-89c4-8c7776de09fd.jpg


DPR
https://sirekap-obj-data.kpu.go.id/pemilu/hhcd/pdpr/0.json


DPRD Provinsi
https://sirekap-obj-data.kpu.go.id/wilayah/pemilu/pdprdp/0.json
https://sirekap-obj-data.kpu.go.id/pemilu/partai.json
https://sirekap-obj-data.kpu.go.id/pemilu/hhcd/pdprdp/11.json


DPRD KAB/KOTA
https://sirekap-obj-data.kpu.go.id/pemilu/hhcd/pdprdk/51/5108.json

DPD
https://sirekap-obj-data.kpu.go.id/pemilu/caleg/dpd/11.json
https://sirekap-obj-data.kpu.go.id/pemilu/hhcw/pdpd/11.json


"""

if __name__=='__main__':
    url = "https://sirekap-obj-data.kpu.go.id/pemilu/hhcw/ppwp/11/1105/110507.json"
    response = requests.get(url)
    content = json.loads(response.content)
    print(content)