if [[ $# -ne 2 ]]; then
	echo "Usage: run.sh [NGROK_AUTHTOKEN] [NGROK_BASIC_AUTH]"
	echo
	echo "NGROK_BASIC_AUTH - username:password"
	echo
	exit 1
fi

DOMAIN="JTjkRajnVdExwo.glioblastoma"
# mount the hardrive
source hardrive_mount.sh

# run the flask process
python3 app.py

# run the ngrok instance
sudo docker run  --net=host -it -e NGROK_AUTHTOKEN=$1 ngrok/ngrok:alpine http --region=au --hostname=jtjkrajnvdexwo.glioblastoma.au.ngrok.io --basic-auth=$2 5000
