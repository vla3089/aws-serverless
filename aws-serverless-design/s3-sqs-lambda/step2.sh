#!/bin/zsh

aws lambda create-event-source-mapping \
    --function-name cmtr-7e60a31c-s3-snlt-lambda \
    --event-source-arn arn:aws:sqs:eu-central-1:905418349556:cmtr-7e60a31c-s3-snlt-queue \
    --enabled