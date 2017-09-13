#!/bin/bash
# lancement du proxy a partir de l'environnement virtuel
#zf170911.1139

THEIP=$(/sbin/ifconfig ens18 | /bin/grep "inet ad" | /usr/bin/cut -f2 -d: | /usr/bin/awk '{print $1}')

echo -e "
Afin de garder l'appli permanente, il serait bien de la faire tourner dans un 'screen' avec:
screen -S proxy       pour entrer dans screen
./start.sh            pour lancer le serveur WEB dans screen
CTRL+a,d              pour sortir de screen en laissant tourner le serveur
screen -r proxy       pour revenir dans screen
CTRL+d                pour terminer screen
screen -list          pour lister tous les screen en fonctionement

On utilisera ce petit proxy avec:

$THEIP:8080

"

#read -p "appuyer une touche pour continuer"


virtFold="venvMitmproxy"
source $virtFold/bin/activate

# pour les problèmes de SNI il faut lire
# http://docs.mitmproxy.org/en/stable/features/passthrough.html
 
#mitmdump -v
#mitmdump --insecure
#mitmproxy
#mitmproxy --insecure

#sudo mitmproxy -p 443 -R https://tequila.epfl.ch/ --insecure -s ./code_emule_hello_world_1.py
sudo mitmdump -p 443 -R https://tequila.epfl.ch/ --insecure -s ./code_emule_hello_world_1.py

#!/bin/sh
#python ./tutu.py


deactivate
