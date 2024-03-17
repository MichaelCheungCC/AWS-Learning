# make bucket
aws s3 mb s3://dea-sam-1354641568

# package cloudformation
aws cloudformation package --s3-bucket dea-sam-1354641568 --template-file SAM/template.yaml --output-template-file SAM/gen/template-generate.yaml

# deploy
aws cloudformation deploy --template-file SAM/gen/template-generate.yaml --stack-name api-lambda-dynamoDB --capabilities CAPABILITY_IAM