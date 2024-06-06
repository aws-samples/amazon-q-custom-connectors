# AWS custom connector workshop for Amazon Q Business

This folder holds artifacts used in the workshop titled "Connect Amazon Q Business to a custom data source"
* `cdk/` - contains a deploy script that creates an ECR repo, builds the custom data source container image, deploys the custom data source as a load-balanced ECS Fargate service and creates a base connector lambda function.
* `connector/` - custom connector application files for the workshop
* `datasource/` - custom data source dockerfile and requirements 

Visit the workshop here: [Link](https://aws.amazon.com/)