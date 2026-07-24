#!/data/data/com.termux/files/usr/bin/bash

TOKEN=$(grep access_token ~/.bash_history | tail -1)

echo $TOKEN
