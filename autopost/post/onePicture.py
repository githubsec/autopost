from bs4 import BeautifulSoup
import requests
import linecache
import time
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.compat import xmlrpc_client
from wordpress_xmlrpc.methods import media, posts
from urllib.request import urlopen

url = 'https://unsplash.com/'



client = Client('http://yoursite/xmlrpc.php', 'yourwordpress@email.address', 'password')


def post_picture(image_url):
    fileImg = urlopen(image_url)
    imageName = fileImg.url.split('/')[-1]+'.jpg'
    data = {
        'name': imageName,
        'type': 'image/jpeg',
    }
    data['bits'] = xmlrpc_client.Binary(fileImg.read())

    response = client.call(media.UploadFile(data))
    attachment_id = response['id']
    post = WordPressPost()
    post.title = 'Picture of the Day'
    post.post_status = 'publish'
    post.thumbnail = attachment_id
    post.id = client.call(posts.NewPost(post))


def geturl(latesturl):
    i = 0
    xxxurl = ''
    while latesturl[i] != '"':
        i += 1
    i += 1
    while latesturl[i] != '?':
        xxxurl += latesturl[i]
        i += 1
    xxxurl += '?w=1280'
    return xxxurl


def get_images_url(url, data=None):
    wb_data = requests.get(url)
    ## time.sleep(10)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    images = soup.select('div.y5w1y > a')
    ##print(images[0])
    xxxurl = ''
    theurl = ''
    item = 0
    newurls = open('date', 'w+')
    while item < 20:
        first_img_url = images[item].get('style')
        xxxurl = geturl(first_img_url)
        if item == 0:
            theurl = xxxurl
        newurls.write(xxxurl+'\n')
        item += 1
    post_picture(theurl)

    newurls.close()


def firsturl(url):
    wb_data = requests.get(url)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    images = soup.select('div.y5w1y > a')
    first_img_url = images[0].get('style')
    xxxurl = geturl(first_img_url)
    return xxxurl

first = firsturl(url)
pictures = linecache.getlines('date')
latestfirst = pictures[0]
latestfirst = latestfirst[0:-1]

print(first)
print(latestfirst)
itemfile = open('item', 'r')
item = int(itemfile.read())
itemfile.close()
if first == latestfirst:
    theurl = pictures[item]
    theurl = theurl[0:-1]
    post_picture(theurl)
    item += 1
    print('equal')
else:
    get_images_url(url)
    item = 1

newitem = open('item', 'w+')
newitem.write(str(item))
newitem.close()





