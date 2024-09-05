#!/bin/bash

cp ./hotwalletclaimer.docker.service /etc/systemd/system
systemctl daemon-reload
systemctl enable hotwalletclaimer.docker.service