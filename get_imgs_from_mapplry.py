import requests
import json
import os
import sys

def get_images():
    saved_img_keys = set()
    list_of_locations = ['30.219444,48.75'] # Uman, Ukraine. Longtitude and lattitude are inversed
    client_id = 'TG1sUUxGQlBiYWx2V05NM0pQNUVMQTo2NTU3NTBiNTk1NzM1Y2U2'
    radius = 100000
    resolution = 2048 # 256, 512, 1024, 2048
    angle_interval = (0, 50)

    # iterate over all specified locations
    for location in list_of_locations:
        # GET request to mapillary
        next_page_link = f"https://a.mapillary.com/v3/images/?closeto={location}&radius={radius}&per_page=100&client_id={client_id}"

        # iterate over next pages
        page = 0
        while True:
            page += 1
            print(f'PAGE {page}')

            # GET
            r = requests.get(next_page_link)
            # frome bytestring to unicode
            req_str = r.content.decode('utf-8')
            # parse from json to python dict
            data = json.loads(req_str)

            # iterate over all entries on page
            for i in range(len(data['features'])):
                # extract info about image
                img_descr = data['features'][i]
                ca = img_descr['properties']['ca']
                print(f'ca = {ca}')
                # filter camera angles
                if ca >= angle_interval[0] and ca <= angle_interval[1]:
                    key = img_descr['properties']['key']
                    # if image is not already saved
                    if key not in saved_img_keys:
                        # download & rename image
                        os.system(f'wget https://d1cuyjsrcm0gby.cloudfront.net/{key}/thumb-{resolution}.jpg')
                        os.system(f'mv thumb-{resolution}.jpg thumb-{resolution}_{key}.jpg')
                        saved_img_keys.add(key)
                    print(f'PAGE {page} entry {i}')

            # check if not the last page
            if len(r.headers['Link'].split('<')) >= 3:
                next_page_link = r.headers['Link'].split('<')[2][:-13]
            else: # last page
                break

get_images()

#r = requests.get("https://a.mapillary.com/v3/images/?radius=100&client_id=TG1sUUxGQlBiYWx2V05NM0pQNUVMQTo2NTU3NTBiNTk1NzM1Y2U2&closeto=13.0006076843%2C55.6089295863&per_page=3&_next_page_token=eyJhZnRlciI6WzE0LjQ4NTYyNDMzMDYzMzUyNCwxNDA3MDUzODM2MDAwLDk4MTQzNDFdfQ%3D%3D")
# print info about request
#print(r.status_code)
#print(r.headers)
#print(r.headers['Link'])
#print(r.content)

# nice output
#print(json.dumps(data, indent=4, sort_keys=True))











