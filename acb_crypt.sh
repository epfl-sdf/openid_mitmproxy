#!/bin/bash
#Cryptage des credentials
#zf170420.1446

ZSECRET="emule_hello_world_1.secrets.json"

gpg2 -c ../$ZSECRET
mv ../$ZSECRET.gpg .
rm -R ../.gnupg
