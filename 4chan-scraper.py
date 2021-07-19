import os
import re
import requests
import sys
import time

from requests_html import HTMLSession

def get_image_links(user_input):
    session = HTMLSession()
    x = session.get(user_input)
    links = x.html.links

    print(links)

    return links

def get_web_content(file_extension, links, image_counter):
    x = re.compile(".*" + file_extension)
    links = list(filter(x.match, links))

    for link in links:
        image_counter = int(image_counter) + 1

        while (os.path.isfile(str(image_counter) + "." + file_extension)):
            image_counter = int(image_counter) + 1

        try:
            req = requests.get(link)
        except requests.exceptions.MissingSchema:
            req = requests.get("http:" + link)
        except requests.exceptions.InvalidURL:
            continue

        f = open(str(image_counter) + "." + file_extension, 'wb')
        f.write(req.content)
        f.close()

def main():
    # Check length of argument list.
    if (len(sys.argv) <= 1):
        print(":: No arguments given.")
        print(":: Ensure you've provided arguments, then rerun " + sys.argv[0] + ".")

        quit(1)

    file_extensions = ["png", "gif", "jpg", "jpeg", "webm"]
    image_counter = 0

    # Remove filename from list.
    sys.argv.pop(0)

    for sub_url in sys.argv:
        print("Generating file list from " + sub_url)

        links = get_image_links(sub_url)

        for extension in file_extensions:
            get_web_content(extension, links, image_counter)

    print("Downloaded from \"" + str(len(sys.argv)) + "\" URLs")
    quit(0)

main()
