import boto3
import os
import json

s3_client = boto3.client('s3')
BUCKET_NAME = os.environ['BUCKET_NAME']

def lambda_handler_upload(event, context):
    try: 
        body = json.loads(event.get('body', '{}'))
        file_name = body.get('filename', 'upload_default')
        
        # pre signed URL for PUT
        presigned_url = s3_client.generate_presigned_url(
            'put_object',
            Params={'Bucket': BUCKET_NAME, 'Key': file_name},
            ExpiresIn=300 # 5 minutes
        )
        
        return {
            "statusCode": 200,
            "body": json.dumps({
                "objectKey": file_name,
                "uploadUrl": presigned_url
            })
        }
    except Exception as e:
        print(f"Error: {str(e)}") #  CloudWatch
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Error interno del servidor", "details": str(e)})
        }


def lambda_handler_download(event, context):
    object_key = event['pathParameters']['objectKey']
    
    # pre signed URL for GET
    download_url = s3_client.generate_presigned_url(
        'get_object',
        Params={'Bucket': BUCKET_NAME, 'Key': object_key},
        ExpiresIn=3600 # 1 hour
    )
    
    return {
        "statusCode": 307,
        "headers": {
            "Location": download_url
        }
    }