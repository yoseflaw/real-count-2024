import os
import json
import requests

from pathlib import Path

BASE_URL = "https://sirekap-obj-data.kpu.go.id/"
PPWP_WILAYAH = "wilayah/pemilu/ppwp"
PPWP_RECAP = "pemilu/hhcw/ppwp"
PDPR_RECAP = "pemilu/hhcw/pdpr"
PDPRD_RECAP = "pemilu/hhcw/pdprdp"
PDPD_RECAP = "pemilu/hhcw/pdpd"
PDPRDK_RECAP = "pemilu/hhcd/pdprdk"  # min tingkat = 2

def download_data(url):
    print(f"downloading: {url}")
    response = requests.get(url)
    content = response.content
    content_json = json.loads(content)
    
    output_file = "data/raw/" + url.replace(BASE_URL, "")
    output_parent_folder = os.path.join(*output_file.split("/")[:-1])
    Path(output_parent_folder).mkdir(parents=True, exist_ok=True)
    with open(output_file, "w") as f_out:
        json.dump(
            content_json, 
            f_out,
            indent=2
        )
    return content_json


def download_wilayah(
        wilayah_dict, 
        url_root, 
        min_tingkat_recap=1, 
        wilayah_url=None,
        rekap_url=None
        ):
    url_root_next = url_root[:-7] if wilayah_dict["tingkat"] == 1 else url_root[:-5]
    next_url = f"{url_root_next}/{wilayah_dict['kode']}.json"
    # download recap
    download_data(next_url.replace(PPWP_WILAYAH, PPWP_RECAP))
    download_data(next_url.replace(PPWP_WILAYAH, PDPR_RECAP))
    download_data(next_url.replace(PPWP_WILAYAH, PDPRD_RECAP))
    download_data(next_url.replace(PPWP_WILAYAH, PDPRD_RECAP))
    if wilayah_dict["tingkat"] >= 2:
        download_data(next_url.replace(wilayah_url, PDPD_RECAP))
    if wilayah_dict["tingkat"] < 5:
        next_wilayah = download_data(next_url)
        for wilayah in next_wilayah:
            download_wilayah(
                wilayah, 
                next_url,
                min_tingkat_recap=min_tingkat_recap,
                wilayah_url=wilayah_url,
                rekap_url=rekap_url
            )



if __name__=='__main__':
    # PPWP
    ## Download candidate names
    download_data("https://sirekap-obj-data.kpu.go.id/pemilu/ppwp.json")

    ## Download wilayah and all wilayah data
    url_wilayah_root = "https://sirekap-obj-data.kpu.go.id/wilayah/pemilu/ppwp/0.json"
    download_data("https://sirekap-obj-data.kpu.go.id/pemilu/hhcw/ppwp.json")
    ppwp_wilayah_root = download_data(url_wilayah_root)
    for wilayah in ppwp_wilayah_root:
        download_wilayah(
            wilayah,
            url_wilayah_root,
            wilayah_url=PPWP_WILAYAH,
            rekap_url=PPWP_RECAP
        )
    download_data("https://sirekap-obj-data.kpu.go.id/wilayah/pemilu/ppwp/11/1105/110507/1105072002/1105072002001.json")
        
    # DPR
    ## Download partai
    download_data("https://sirekap-obj-data.kpu.go.id/pemilu/partai.json")
    ## Download recap national
    download_data("https://sirekap-obj-data.kpu.go.id/pemilu/hhcd/pdpr/0.json")
    url_dapil_root = "https://sirekap-obj-data.kpu.go.id/wilayah/pemilu/pdpr/dapil_dpr.json"
    pdpr_dapil_root = download_data(url_dapil_root)
    for dapil in pdpr_dapil_root:
        dapil_code = dapil["kode"]
        # recap
        download_data(f"https://sirekap-obj-data.kpu.go.id/pemilu/hhcd/pdpr/{dapil_code}.json")
        # caleg
        download_data(f"https://sirekap-obj-data.kpu.go.id/pemilu/caleg/partai/{dapil_code}.json")

    # DPRD Prov & Kab
    url_dapil_root = "https://sirekap-obj-data.kpu.go.id/wilayah/pemilu/pdprdp/0.json"
    pdprd_dapil_root = download_data(url_dapil_root)
    for wilayah in pdprd_dapil_root:
        # Prv
        kode_wilayah = wilayah["kode"]
        dapil_list = download_data(f"https://sirekap-obj-data.kpu.go.id/wilayah/pemilu/pdprdp/{kode_wilayah}.json")
        for dapil in dapil_list:
            kode_dapil = dapil["kode_dapil"]
            download_data(f"https://sirekap-obj-data.kpu.go.id/pemilu/hhcd/pdprdp/{kode_wilayah}/{kode_dapil}.json")
            download_data(f"https://sirekap-obj-data.kpu.go.id/pemilu/caleg/partai/{kode_dapil}.json")
        # Kab
        kab_list = download_data(f"https://sirekap-obj-data.kpu.go.id/wilayah/pemilu/ppwp/{kode_wilayah}.json")
        for kab in kab_list:
            kode_kab = kab["kode"]
            dapil_list = download_data(f"https://sirekap-obj-data.kpu.go.id/wilayah/pemilu/pdprdk/{kode_wilayah}/{kode_kab}.json")
            for dapil in dapil_list:
                kode_dapil = dapil["kode_dapil"]
                download_data(f"https://sirekap-obj-data.kpu.go.id/wilayah/pemilu/pdprdk/{kode_wilayah}/{kode_kab}/{kode_dapil}.json")
                download_data(f"https://sirekap-obj-data.kpu.go.id/pemilu/hhcd/pdprdk/{kode_wilayah}/{kode_kab}/{kode_dapil}.json")
                download_data(f"https://sirekap-obj-data.kpu.go.id/pemilu/caleg/partai/{kode_dapil}.json")
