import sys
import requests
from bs4 import BeautifulSoup

SUPPORTED_FILE_TYPES = ("pdf","mp4",)
extract_resource_name = lambda link: link.split("/")[-2][:-1]
extract_href = lambda a: f"https://ocw.mit.edu{a["href"]}" if "http" not in a["href"] else a["href"]

def query_selector(url, filter, transform):
	page_source = requests.get(url)
	soup = BeautifulSoup(page_source.text, features="lxml")
	return set(map(transform, soup.select(filter)))

if len(sys.argv) == 1:
    print(f"usage: {sys.argv[0]} https://ocw.mit.edu/courses/...")
    exit(1)

base_url = sys.argv[1]
if not base_url.endswith("/"): base_url += "/"

__import__("pathlib").Path("./work").mkdir(exist_ok=True)
links = query_selector(base_url + "download/", """.resource-list-item-details a[href*="resources"]""", extract_href)
for link in links:
	selector = ",".join(map(lambda file_type: f"""[href*="{file_type}"]""", SUPPORTED_FILE_TYPES))
	resources = query_selector(link, selector, extract_href)
	resource_name = extract_resource_name(link)
	with open(f"./work/{resource_name}.txt", "w+") as f:
		f.write("\n".join(resources))
