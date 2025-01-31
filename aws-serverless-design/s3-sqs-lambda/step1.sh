#!/bin/zsh

aws s3api put-bucket-notification-configuration \
    --bucket cmtr-7e60a31c-s3-snlt-bucket-882992 \
    --notification-configuration file://s3-notification-config.json