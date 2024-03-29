from __future__ import print_function
import boto3
import logging
from botocore.vendored import requests
import json

logger = logging.getLogger()
logger.setLevel(logging.INFO)
ecrClient = boto3.client('ecr')
ecsClient = boto3.client('ecs')
s3 = boto3.resource('s3')

from botocore.vendored import requests
import json

SUCCESS = "SUCCESS"
FAILED = "FAILED"


def send(event, context, responseStatus, responseData, physicalResourceId=None, noEcho=False):
    responseUrl = event['ResponseURL']

    print(responseUrl)

    responseBody = {}
    responseBody['Status'] = responseStatus
    responseBody['Reason'] = 'See the details in CloudWatch Log Stream: ' + context.log_stream_name
    responseBody['PhysicalResourceId'] = physicalResourceId or context.log_stream_name
    responseBody['StackId'] = event['StackId']
    responseBody['RequestId'] = event['RequestId']
    responseBody['LogicalResourceId'] = event['LogicalResourceId']
    responseBody['NoEcho'] = noEcho
    responseBody['Data'] = responseData

    json_responseBody = json.dumps(responseBody)

    print("Response body:\n" + json_responseBody,flush=True)

    headers = {
        'content-type': '',
        'content-length': str(len(json_responseBody))
    }

    try:
        response = requests.put(responseUrl,
                                data=json_responseBody,
                                headers=headers)
        print("Status code: " + response.reason)
    except Exception as e:
        print("send(..) failed executing requests.put(..): " + str(e))

def failfast(event, context, responseStatus, responseData, physicalResourceId=None, noEcho=False):
    print("Goodbye world!", flush=True)
    r = {}
    r['Data'] = responseData
    print(r)
    print("responseData Type: ",type(r),flush=True)
    send(event, context, SUCCESS, r, 'CustomResourcePhysicalID')
    exit(0)

def handler(event, context):
    try:
        CoreServiceEcrRepo = event['ResourceProperties']['CoreServiceRepo']
        LikeServiceEcrRepo = event['ResourceProperties']['LikeServiceRepo']
        EcsClusterName = event['ResourceProperties']['EcsClusterName']
        CfnStackName = event['ResourceProperties']['CfnStackName']
        IsSecondary = event['ResourceProperties']['SecondaryRegion']
        MythicalArtifactBucket = event['ResourceProperties']['MythicalArtifactBucket']
        logger.info('Event: {}'.format(event))
        logger.info('Context: {}'.format(context))
        tempResponse = []
        responseData = {}
        failure = False
        print(event,flush=True)
        logging.info(event)
    except Exception as e:
        logger.warning('failure parsing parameters from event {}'.format(str(e)))
        print('parsing inputs failed',flush=True)
        send(event, context, FAILED, 'unknown failure', 'CustomResourcePhysicalID')
        return()

    # Immediately respond on Delete
    if event['RequestType'] == 'Delete':
        try:
            logger.info('Delete called')
            coreDeleteResponse = ecrClient.delete_repository(
                repositoryName=CoreServiceEcrRepo,
                force=True)
        except Exception as e:
            if "RepositoryNotFoundException" in str(e):
                failure = False
            else:
                failure = True
            tempResponse.append({CoreServiceEcrRepo: str(e)})
        try:
            likeDeleteResponse = ecrClient.delete_repository(
               repositoryName=LikeServiceEcrRepo,
               force=True)
        except Exception as e:
            if "RepositoryNotFoundException" in str(e):
                failure = False
            else:
                failure = True
            tempResponse.append({LikeServiceEcrRepo: str(e)})
        if IsSecondary == 'false':
            try:
                logger.info('deleting bucket {}'.format(MythicalArtifactBucket))
                bucket = s3.Bucket(MythicalArtifactBucket)
                # Delete S3 bucket
                for key in bucket.objects.all():
                    key.delete()
                bucket.delete()
            except Exception as e:
                if "The specified bucket does not exist" in str(e):
                    failure = False
                else:
                    failure = True
                tempResponse.append({MythicalArtifactBucket: str(e)})

            try:
                # List ECS Services and delete services in a specific cluster
                ecsServicesToDelete = ecsClient.list_services(
                   cluster=EcsClusterName
                )
                if ecsServicesToDelete['serviceArns'] != []:
                    for serviceName in ecsServicesToDelete['serviceArns']:
                        ecsDeleteResponse = ecsClient.delete_service(
                            cluster=EcsClusterName,
                            service=serviceName,
                            force=True)
            except Exception as e:
                failure = True
                tempResponse.append({EcsClusterName: str(e)})
            # failfast(event, context, SUCCESS, tempResponse, 'CustomResourcePhysicalID')

        responseData['Data'] = str(tempResponse)
        if failure == False:
            send(event, context, SUCCESS, responseData, 'CustomResourcePhysicalID')
        else:
            send(event, context, FAILED, responseData, 'CustomResourcePhysicalID')   

    if event['RequestType'] == 'Create':
        # Setup the account to enable container insights by default
        try:
            responseData = {}
            logger.info('setting account defaults for ECS')
            ecsClient = boto3.client('ecs')
            response = ecsClient.put_account_setting_default(name='containerInsights',value='enabled')
            responseData['Data'] = str(response)
            send(event, context, SUCCESS, responseData, 'CustomResourcePhysicalID')
        except Exception as e:
            responseData['Data'] = str(e)
            send(event, context, FAILED, responseData, 'CustomResourcePhysicalID')

    if event['RequestType'] == 'Update':
        try:
            responseData = {}
            send(event, context, SUCCESS, responseData, 'CustomResourcePhysicalID')
        except Exception as e:
            send(event, context, FAILED, responseData, 'CustomResourcePhysicalID')

if __name__ == "__main__":
    mockevent = {
		'RequestType': 'Delete',
		'ServiceToken': 'arn:aws:lambda:us-east-2:428505257828:function:l1-CleanDeletionLambdaFunction-1I8XLIN9Q0RS4',
		'ResponseURL': 'https://cloudformation-custom-resource-response-useast2.s3.us-east-2.amazonaws.com/arn%3Aaws%3Acloudformation%3Aus-east-2%3A428505257828%3Astack/l1/897739d0-227d-11ea-ba13-0ad7a569cb8c%7CCleanDeletionCustomResource%7Cb1587f31-65b4-4a29-8723-aef7d0f6d839?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20191219T163659Z&X-Amz-SignedHeaders=host&X-Amz-Expires=7200&X-Amz-Credential=AKIAVRFIPK6PMQZL3WHJ%2F20191219%2Fus-east-2%2Fs3%2Faws4_request&X-Amz-Signature=4feba47f210737c2155d1cb3147624f663d64926662cef9e088cf605b7175bb5',
		'StackId': 'arn:aws:cloudformation:us-east-2:428505257828:stack/l1/897739d0-227d-11ea-ba13-0ad7a569cb8c',
		'RequestId': 'b1587f31-65b4-4a29-8723-aef7d0f6d839',
		'LogicalResourceId': 'CleanDeletionCustomResource',
		'ResourceType': 'Custom::CleanDelete',
		'ResourceProperties': {
			'ServiceToken': 'arn:aws:lambda:us-east-2:428505257828:function:l1-CleanDeletionLambdaFunction-1I8XLIN9Q0RS4',
			'CfnStackName': 'l1',
			'CoreServiceRepo': 'l1-coreserv-i4pjp3re04r7',
			'SecondaryRegion': 'false',
			'Region': 'us-east-2',
			'MythicalArtifactBucket': 'l1-mythicalartifactbucket-nnwkchumi48x',
			'EcsClusterName': 'foo',
			'LikeServiceRepo': 'l1-likeserv-1dtsq9dl51m7z'
		}
	}

    handler(event=mockevent,context={})
