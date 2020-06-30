# ------- importing secret keys ----------------
from k3y5 import COS_API_KEY_ID, COS_AUTH_ENDPOINT, COS_ENDPOINT, COS_RESOURCE_CRN, COS_SERVICE_CRN
# ----------------------------------------------
# ------- import boto --------------------------
import ibm_boto3
from ibm_botocore.client import Config, ClientError
# ----------------------------------------------

# get list of buckets in cloud object storage
def get_buckets():
    cos = ibm_boto3.resource("s3",
        ibm_api_key_id=COS_API_KEY_ID,
        ibm_service_instance_id=COS_RESOURCE_CRN,
        ibm_auth_endpoint=COS_AUTH_ENDPOINT,
        config=Config(signature_version="oauth"),
        endpoint_url=COS_ENDPOINT
    )
    print("Retrieving list of buckets")
    try:
        buckets = cos.buckets.all()
        for bucket in buckets:
            print("Bucket Name: {0}".format(bucket.name))
    except ClientError as be:
        print("CLIENT ERROR: {0}\n".format(be))
    except Exception as e:
        print("Unable to retrieve list buckets: {0}".format(e))


# get list of contents in given bucket name
def get_bucket_contents(bucket_name="darwin-resume-vault"):
    cos = ibm_boto3.resource("s3",
        ibm_api_key_id=COS_API_KEY_ID,
        ibm_service_instance_id=COS_RESOURCE_CRN,
        ibm_auth_endpoint=COS_AUTH_ENDPOINT,
        config=Config(signature_version="oauth"),
        endpoint_url=COS_ENDPOINT
    )
    print("Retrieving bucket contents from: {0}".format(bucket_name))
    try:
        files = cos.Bucket(bucket_name).objects.all()
        for file in files:
            print("Item: {0} ({1} bytes).".format(file.key, file.size))
    except ClientError as be:
        print("CLIENT ERROR: {0}\n".format(be))
    except Exception as e:
        print("Unable to retrieve bucket contents: {0}".format(e))

# retrieve specfic item from given bucket
def get_item(bucket_name, item_name="darwin-resume-vault"):
    cos = ibm_boto3.resource("s3",
        ibm_api_key_id=COS_API_KEY_ID,
        ibm_service_instance_id=COS_RESOURCE_CRN,
        ibm_auth_endpoint=COS_AUTH_ENDPOINT,
        config=Config(signature_version="oauth"),
        endpoint_url=COS_ENDPOINT
    )
    print("Retrieving item from bucket: {0}, key: {1}".format(bucket_name, item_name))
    try:
        file = cos.Object(bucket_name, item_name).get()
        print("File Contents: {0}".format(file["Body"].read()))
    except ClientError as be:
        print("CLIENT ERROR: {0}\n".format(be))
    except Exception as e:
        print("Unable to retrieve file contents: {0}".format(e))

# upload item to particular bucket
def upload_item(item_key, up_from, bucket_name="darwin-resume-vault"):
    cos = ibm_boto3.client("s3",
        ibm_api_key_id=COS_API_KEY_ID,
        ibm_service_instance_id=COS_SERVICE_CRN,
        config=Config(signature_version="oauth"),
        endpoint_url=COS_ENDPOINT
    )
    print("Uploading {0} to {1}".format(up_from, bucket_name))
    try:
        cos.upload_file(Filename=up_from, Bucket=bucket_name, Key=item_key)
        print("Uploaded {0} to {1}".format(up_from, bucket_name))
        return True
    except ClientError as be:
        print("CLIENT ERROR: {0}\n".format(be))
    except Exception as e:
        print("Unable to Upload to Bucket: {0}".format(e))
    return False

# download specific item from given bucket
def download_item (item_key, save_to, bucket_name="darwin-resume-vault"):
    cos = ibm_boto3.client("s3",
        ibm_api_key_id=COS_API_KEY_ID,
        ibm_service_instance_id=COS_SERVICE_CRN,
        config=Config(signature_version="oauth"),
        endpoint_url=COS_ENDPOINT
    )
    print("Downloading {0} from {1}".format(item_key, bucket_name))
    try:
        res=cos.download_file(Bucket=bucket_name, Key=item_key, Filename=save_to)
        print("Downloaded {0} to {1}".format(item_key, save_to))
        return True
    except ClientError as be:
        print("CLIENT ERROR: {0}\n".format(be))
    except Exception as e:
        print("Unable to Download from Bucket: {0}".format(e))
    return False


# ---- test functions -------------------------------------
# get_buckets ()
# get_bucket_contents ("darwin-resume-vault")
# get_item ("darwin-resume-vault", "mihir_singh")
# upload_item("darwin-resume-vault", "siddhant_thakur", "data_src\\resume\\sid_resume.pdf")
# download_item ("darwin-resume-vault", "siddhant_thakur", "siddhant_thakur.pdf")
# ---------------------------------------------------------