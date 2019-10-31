# s3data

Simple persistent object storage for AWS S3

![](https://github.com/bcantoni/s3data/workflows/Python%20package/badge.svg)

This is a simple wrapper for a specific use case of S3 using the [Amazon AWS SDK for Python Boto3](https://aws.amazon.com/sdk-for-python/). The use case is to create a persistent object store for a simple data dictionary. It could be used for anything, but in my case I'm using it to store data between test runs for CI systems like GitHub Actions.

## Prerequisites

Only Python 3.6 and up are tested. Virtual environment is recommended to make your life easier.

This package is not installed to PyPI but instead can be directly installed from Github:

    pip install -e git://github.com/bcantoni/s3data.git#egg=s3data

In AWS S3, create a new bucket and an IAM user (with access key and secret) which only has access to that specific bucket. Note: if you have an existing S3 bucket that will also work, but I intentionally wanted to isolate this one out of caution.

Set all of the above values into environment variables:

* AWS_ACCESS_KEY_ID
* AWS_SECRET_ACCESS_KEY
* S3DATA_BUCKET

## Usage example

    #!/usr/bin/env python
    import os
    import s3data


    s3 = s3data.S3Data(os.environ['AWS_ACCESS_KEY_ID'],
                    os.environ['AWS_SECRET_ACCESS_KEY'],
                    os.environ['S3DATA_BUCKET'])

    key = 'testy-tester'
    data = {"test": "alpha", "version": 1}
    s3.put(key, data)

    data2 = s3.get(key)
    print(data2)
    assert data2['test'] == 'alpha'
    assert data2['version'] == 1

    s3.delete(key)
