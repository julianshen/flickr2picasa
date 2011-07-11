import flickrapi
import config
api_key = config.api_key
api_secret = config.api_secret

flickr = flickrapi.FlickrAPI(api_key, api_secret)
(token, frob) = flickr.get_token_part_one(perms='read')
if not token: raw_input("Press ENTER after you authorized this program")
flickr.get_token_part_two((token, frob))
setList = flickr.photosets_getList()
sets = setList.find('photosets').findall('photoset')

for set in sets:
    id = set.attrib['id']
    title = set.find('title').text
    print id + ":" +title
