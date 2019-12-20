stackName=l8
bucket=daveaws/cloudformation/mm
all: core

test:
	zip CleanDeletionLambdaFunction.zip CleanDeletionLambdaFunction.py
	aws s3 cp CleanDeletionLambdaFunction.zip s3://${bucket}/CleanDeletionLambdaFunction.zip
	aws s3 cp lambdatest.yml  s3://${bucket}/lambdatest.yml
	aws cloudformation create-stack \
	  --stack-name ${stackName} \
	  --template-url https://s3.amazonaws.com/${bucket}/lambdatest.yml \
  	  --timeout-in-minutes 5 \
	  --capabilities CAPABILITY_NAMED_IAM CAPABILITY_IAM --region us-east-2

push:
	aws s3 cp core.yml s3://${bucket}/core.yml
	aws s3 cp cwdashboard.yml s3://${bucket}/cwdashboard.yml
	aws s3 cp cicd.yml s3://${bucket}/cicd.yml
	aws s3 cp parameters_primary.json s3://${bucket}/parameters_primary.json
	zip CleanDeletionLambdaFunction.zip CleanDeletionLambdaFunction.py
	aws s3 cp CleanDeletionLambdaFunction.zip s3://${bucket}/CleanDeletionLambdaFunction.zip


update: push
	aws cloudformation update-stack \
	  --stack-name ${stackName} \
	  --template-url https://s3.amazonaws.com/${bucket}/core.yml \
	  --capabilities CAPABILITY_NAMED_IAM CAPABILITY_IAM --region us-east-2
	  
core: push
	aws cloudformation create-stack \
	  --stack-name ${stackName} \
	  --template-url https://s3.amazonaws.com/${bucket}/core.yml \
	  --timeout-in-minutes 5 \
	  --capabilities CAPABILITY_NAMED_IAM CAPABILITY_IAM --region us-east-2

delete:
	aws cloudformation delete-stack --stack-name ${stackName}
	
lambda2ee:
	echo "copying assets to event engine"
	zip CleanDeletionLambdaFunction.zip CleanDeletionLambdaFunction.py
	aws s3 cp cwdashboard.yml s3://ee-assets-prod-us-east-1/modules/034436f43dc3453ea9ac68007666b8c6/v1/cwdashboard.yml
	aws s3 cp CleanDeletionLambdaFunction.zip s3://ee-assets-prod-us-east-1/modules/034436f43dc3453ea9ac68007666b8c6/v1/CleanDeletionLambdaFunction.zip
	aws s3 cp cicd.yml s3://ee-assets-prod-us-east-1/modules/034436f43dc3453ea9ac68007666b8c6/v1/cicd.yml
	
	
