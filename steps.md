# STEP 1

Create new lambda function in AWS.

# Step 2 

Paste the required lambda code in code soure from vs code.

# Step 3

Deploy the code. 

# step 3

 Create API Gateway

 Create new api 

 # step 4
 Create new resource
 select cros
 Create method 
 select get/post/put ect.
 * Select integration type- Lambda Function.
 * Select lambda function. 
 Deploy API
 create stage

 * After deploying the api invoke url can be found in api gateway page -> stages 

# Step 5
Create new Bucket in S3 

now go to lambda funtion service page.
then go to configurations -> Environment variables -> edit/ add bucket key-value.

# step 6 
Go to IAM page then -> roles -> select your lambda -> add permissions -> s3 full access add.

# 5 Services Are
1. Lambda Function
2. S3 bucket
3. API Gateway
4. IAM
5. CloudWatch