#!/bin/bash
#Décryptage des credentials
#zf170420.1446

ZSECRET="emule_hello_world_1.secrets.json"

gpg2 $ZSECRET.gpg
mv $ZSECRET ../.
rm -R ../.gnupg
