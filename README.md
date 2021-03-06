# Digitize

This project began as the SCU COEN 315 - Web Architecture and Protocols final project. Not surprisingly, it was abandoned the day after it was submitted for a grade. It has since turned into an exercise in converting a serverful web app into its serverless equivalent using AWS managed services.

This repository holds the backend of the site.

### External links:
- [Website](https://digitize.aleonard.dev)
- [Frontend repository](https://github.com/leonardishere/DigitizeFrontend)

### Technologies used:
- Python 3.7
- AWS API Gateway
- AWS Lambda
- AWS DynamoDB
- AWS CodePipeline
- AWS CloudFormation
- WebSockets

### Architecture
Below is a high-level architecture diagram for Digitize.
This repository includes the API Gateway, Lambda functions, DynamoDB tables, and the Route 53 DNS entries to access the API. Infrastructure and code are continuously integrated and deployed with CodeStar.

![Architecture](images/Digitize_Architecture.svg)

### Todo list:
- [x] Create CI/CD Pipeline
- [x] Migrate from EC2 LAMP instance to API Gateway, Lambda, DynamoDB
- [x] Create resources
  - [x] Students
    - [x] Students Table
    - [x] GET
    - [x] POST
    - [x] GET /cardid/
    - [x] GET /studentid/
  - [x] Checkins
    - [x] POST /checkins/
    - [x] Active Checkins
      - [x] Active Checkins Table
      - [x] GET /checkins/active/
      - [x] GET /checkins/active/cardid/
      - [x] GET /checkins/active/cardreaderid/
    - [x] Inactive Checkins
      - [x] Inactive Checkins Table
      - [x] Get /checkins/inactive/
  - [x] Checkout
    - [x] POST /checkout/
- [x] Create WebSocket API
- [x] Add architecture diagram to the README
- [ ] Migrate API to Swagger
- [ ] Test
- [ ] Create API documentation

### Future work:
- More than one classroom/school
- More detailed attendance analysis
- Automated attendance grading
- Connect to SCU Students database
- Staff login
