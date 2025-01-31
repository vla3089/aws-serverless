#!/bin/zsh

aws s3api put-bucket-encryption \
    --cli-input-json file://encryption-config.json
