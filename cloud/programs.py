#!/bin/bash
rm -rf data
rm -rf storageData
python3 server.py & python3 findface.py
