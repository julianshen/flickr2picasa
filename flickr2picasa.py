import flickrapi
import sys
import numbers
import urllib
import os
import shutil
import gdata
import gdata.photos.service
import gdata.media
import gdata.geo

import config
import im

def init():
    global gd_client
    global flickr
    api_key = config.api_key
    api_secret = config.api_secret
    gd_client = gdata.photos.service.PhotosService()
    gd_client.email = config.email
    gd_client.password = config.password
    gd_client.source = 'myuploader'
    gd_client.ProgrammaticLogin()
    flickr = flickrapi.FlickrAPI(api_key, api_secret)
    (token, frob) = flickr.get_token_part_one(perms='read')
    if not token: raw_input("Press ENTER after you authorized this program")
    flickr.get_token_part_two((token, frob))

def create_picasa_album(album_name):
    album = gd_client.InsertAlbum(title=album_name, summary='') 
    return album
   
def mv_photos(set_id):
    if set_id.isdigit():
        resp = flickr.photosets_getPhotos(photoset_id=set_id)
        photos = resp.find('photoset').findall('photo')
        resp = flickr.photosets_getInfo(photoset_id=set_id)
        title = resp.find('photoset').find('title').text
        album = create_picasa_album(title);
        picasa_album_url = '/data/feed/api/user/%s/albumid/%s' % ('default', album.gphoto_id.text)
        if not os.path.exists(set_id):
            os.makedirs(set_id)
        
        for photo in photos:
            pid = photo.attrib['id']
            resp = flickr.photos_getInfo(photo_id=pid)
            p = resp.find('photo')
            farm = p.attrib['farm']
            secret = p.attrib['secret']
            server = p.attrib['server']
            originalsecret = p.attrib['originalsecret']
            originalformat = p.attrib['originalformat']
            photo_title = p.find('title').text
            photo_desc = p.find('description').text
            if not photo_title:
                photo_title = 'photo'
            else:
                photo_desc = "%s\n\n%s" % (photo_title,photo_desc)
            url = "http://farm{0}.static.flickr.com/{1}/{2}_{3}_o.{4}".format(farm,server,pid,originalsecret,originalformat)
            filename = "{0}/{1}_{2}_o.{3}".format(set_id, pid,originalsecret,originalformat)
            urllib.urlretrieve(url,filename)
            im.resizeImg(filename)
            photo = gd_client.InsertPhotoSimple(picasa_album_url, photo_title, photo_desc, filename, content_type='image/%s'%(originalformat))
        shutil.rmtree(set_id)


init()
for arg in sys.argv:
    mv_photos(arg)
