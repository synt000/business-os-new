#!/bin/bash

TOKEN="မင်းရဲ့ JWT Token"

curl \
-H "Authorization: Bearer $TOKEN" \
http://127.0.0.1:8000/dashboard/summary
