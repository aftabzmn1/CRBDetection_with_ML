#!/bin/sh

# This script starts restarts the server

systemctl restart nginx
supervisorctl reload