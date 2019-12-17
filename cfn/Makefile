stackName=mm3
bucket=daveaws/cloudformation/mm
all: core

push:
	aws s3 cp core.yml s3://${bucket}/core.yml
	aws s3 cp cwdashboard.yml s3://${bucket}/cwdashboard.yml
	aws s3 cp cicd.yml s3://${bucket}/cicd.yml
	aws s3 cp parameters_primary.json s3://${bucket}/parameters_primary.json

update: push
	aws cloudformation update-stack \
	  --stack-name ${stackName} \
	  --template-url https://s3.amazonaws.com/${bucket}/core.yml \
	  --capabilities CAPABILITY_NAMED_IAM CAPABILITY_IAM --region us-east-2
	  
core: push
	aws cloudformation create-stack \
	  --stack-name ${stackName} \
	  --template-url https://s3.amazonaws.com/${bucket}/core.yml \
	  --capabilities CAPABILITY_NAMED_IAM CAPABILITY_IAM --region us-east-2

delete:
	aws cloudformation delete-stack --stack-name ${stackName}
