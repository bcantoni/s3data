from botocore.exceptions import ClientError
import os
import pytest
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import s3data  # noqa


@pytest.fixture(scope="module")
def s3_connection():
    s3 = s3data.S3Data(os.environ['AWS_ACCESS_KEY_ID'],
                       os.environ['AWS_SECRET_ACCESS_KEY'],
                       os.environ['S3DATA_BUCKET'])
    return s3


def test_put_get_delete(s3_connection):
    """Test putting the getting back data"""
    key = 'test-qwerty'
    data = {"test": "flag", "version": 1}
    s3_connection.put(key, data)

    data = s3_connection.get(key)
    assert data['test'] == 'flag'
    assert data['version'] == 1

    s3_connection.delete(key)

    data2 = s3_connection.get(key)
    assert not data2


def test_get_non_exist_key(s3_connection):
    """Test fetching a non-existent key is handled correctly (empty return set)"""
    data = s3_connection.get('this-will-not-exist')
    assert not data


def test_invalid_access():
    """Test invalid access key handling"""
    with pytest.raises(ClientError, match=r".*InvalidAccessKeyId.*"):
        s3 = s3data.S3Data('09871304987304897028370',
                           os.environ['AWS_SECRET_ACCESS_KEY'],
                           os.environ['S3DATA_BUCKET'])
        s3.get('invalid-access-key-test')


def test_invalid_secret():
    """Test invalid secret handling"""
    with pytest.raises(ClientError, match=r".*SignatureDoesNotMatch.*"):
        s3 = s3data.S3Data(os.environ['AWS_ACCESS_KEY_ID'],
                           'a;lksdjf;ljsdflkjadslfj;ldasjf;jd;fl',
                           os.environ['S3DATA_BUCKET'])
        s3.get('invalid-secret-test')


def test_invalid_bucket():
    """Test invalid bucket name handling"""
    with pytest.raises(ClientError, match=r".*NoSuchBucket.*"):
        s3 = s3data.S3Data(os.environ['AWS_ACCESS_KEY_ID'],
                           os.environ['AWS_SECRET_ACCESS_KEY'],
                           'bucket-name-not-exist-asdfasdfasdfasdfsadfasdfadf')
        s3.get('invalid-bucket-name-test')
