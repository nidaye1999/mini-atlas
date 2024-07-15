import httplib2, argparse, os
from bs4 import BeautifulSoup, SoupStrainer

parser = argparse.ArgumentParser(description="Description for arguments")
parser.add_argument("--url", required=True, dest="url")
parser.add_argument("--out", required=True, dest="out")
args = parser.parse_args()
# python3.10 code/download.py --url https://data.nemoarchive.org/biccn/grant/u19_zeng/zeng/transcriptome/sncell/10x_v3/mouse/processed/analysis/10X_nuclei_v3_Broad/ --out data/raw/allen/yao2020/10X_nuclei_v3_Broad

args.url += "/" if args.url[-1] != "/" else ""
args.out += "/" if args.out[-1] != "/" else ""

folder = [args.url]
while len(folder) != 0:
	parent = folder[0]
	del folder[0]
	status, response = httplib2.Http().request(parent)
	for link in BeautifulSoup(response, features="html.parser", parse_only=SoupStrainer("a")):
		if link.has_attr("href") and link["href"] == link.contents[0] and link["href"][-1] == "/":
			folder.append(parent + link["href"])
		elif link.has_attr("href") and link["href"] == link.contents[0] and link["href"][-1] != "/":
			print(args.out + parent.replace(args.url, "") + link["href"])
			os.system("curl " + parent + link["href"] + " --create-dirs -o " + args.out + parent.replace(args.url, "") + link["href"])
