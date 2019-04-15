import os

dest = "../kbengine/assets"

def update(**kwargs):
	# os.system("wget  --reject=bat,pyc -r -L -np {}".format(url))
	url = str(kwargs["url"])

	os.system("wget --reject=bat,pyc -c -r -k -np -L -p {}".format(url))
	if not os.path.exists(dest):
		os.system("mkdir -p {}".format(dest))
	os.system("cp -rf ./{}/. {}".format(url, dest))
	os.system("rm -rf ./{}".format(url))

if __name__ == "__main__":
	# parse args
	import argparse

	parser = argparse.ArgumentParser(description='build')
	parser.add_argument("--url")
	args = parser.parse_args()

	args.url = args.url or '192.168.1.11:8088'

	update(url= args.url)