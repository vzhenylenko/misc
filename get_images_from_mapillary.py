import requests
import json
import os

def get_images(list_of_locations, client_id, radius, angle_interval, resolution=2048):
    '''Download all mapillary images that are in the specified radius to any location of list of locations.
    Filter by angle to download only side looking pictures.

    Args:
        list_of_locations (list of strings): List of 'longitude,lattitude' strings for locations
        cliend_id (string):                  Developer API id for Mapillary
        radius (int):                        Radius from locations (round shape) in meters
        angle_interval (tuple(int, int)):    Interval of angles for downloading (download only if angle is in interval)
        resolution (int):                    Resolution of images for downloading (could be 256, 512, 1024, 2048)

    Raises:
        Error:                               Problems with GET requests to Mapillary

    Returns:
        None
    '''

    saved_img_keys = set()

    # iterate over all specified locations
    for location in list_of_locations:
        # GET request to mapillary
        next_page_link = \
            f"https://a.mapillary.com/v3/images/?closeto={location}&radius={radius}&per_page=100&client_id={client_id}"

        # iterate over next pages
        page = 0
        try:
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

        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)
            raise


if __name__ == '__main__':

    LIST_OF_LOCATIONS= ['30.219444,48.75', '34.98333,48.45']  # ['Uman,Ukraine', 'Dnipro,Ukraine]
    CLIENT_ID = 'TG1sUUxGQlBiYWx2V05NM0pQNUVMQTo2NTU3NTBiNTk1NzM1Y2U2'
    RADIUS = 100000
    RESOLUTION = 2048
    ANGLE_INTERVAL = (0, 50)

    get_images(LIST_OF_LOCATIONS, CLIENT_ID, RADIUS, ANGLE_INTERVAL, RESOLUTION)
