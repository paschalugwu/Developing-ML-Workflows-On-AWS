# Scones Unlimited Image Classification Project

## Project Introduction
This project aims to build an image classification model for Scones Unlimited, a logistics company specializing in scone delivery. The model will classify images of vehicles used by delivery drivers (bicycles vs. motorcycles) to optimize routing and loading bay assignments, enhancing operational efficiency.

## Background
Image classifiers are crucial in computer vision, finding applications in autonomous vehicles, augmented reality, eCommerce, and diagnostic medicine. For Scones Unlimited, such a model can improve various operational aspects, including video feed analysis, social media engagement, and quality control.

## Project Steps Overview
1. **Data Staging**
2. **Model Training and Deployment**
3. **Lambdas and Step Function Workflow**
4. **Testing and Evaluation**
5. **Optional Challenge**
6. **Cleanup Cloud Resources**

## Project Environment

### Workspace Instructions
Complete the project within the AWS lab provided through the Udacity classroom.

### Sagemaker Studio
Ensure you have the SageMaker Studio User created:
1. Open the AWS console from the AWS Gateway.
2. Navigate to Amazon SageMaker and open SageMaker Studio.
3. If no user exists, add a user with an execution role that has full SageMaker access.

### Lambda Functions
You need the Lambda service:
1. Open the AWS console from the AWS Gateway.
2. Navigate to Amazon Lambda.
3. Create and test a Lambda function.

### Step Function Visual Editor
Access the Step Function Visual Editor:
1. Open the AWS console from the AWS Gateway.
2. Navigate to Step Function.
3. Create a state machine and design your workflow visually.

### Role Creation Instructions
1. Open SageMaker service page and start configuring your environment.
2. Select the Quick Start option and create a new IAM role.
3. Complete the configuration and wait for SageMaker to provision the environment.

## Project: Build a ML Workflow For Scones Unlimited On Amazon SageMaker

### Train and Deploy a Machine Learning Model
- **Setup SageMaker Studio:** Set up SageMaker studio and a kernel to run this project.
- **Data Preparation for ML:** Complete the ETL (extract, transform, load) section of the starter code.
- **Train ML Model:** Successfully complete the model training section up to “Getting ready to deploy”.
- **Deploy Model and Construct API Endpoint:** Deploy the trained ML model, print the unique model endpoint name, and make predictions using a sample image.

### Build a Full Machine Learning Workflow

#### Author Lambda Functions
- **First Lambda Function:** Returns image data to Step Function as an event.
- **Second Lambda Function:** Performs image classification.
- **Third Lambda Function:** Filters low-confidence inferences.
- Save the Lambda function code in a Python script.

#### Author Step Function
- Compose the Lambda functions into a Step Function.
- Provide a JSON export defining the Step Function and a screenshot of the working Step Function.

### Monitor the Model for Errors
- **Extract Monitoring Data from S3:** Load Model Monitor data into the notebook.
- **Visualize Model Monitor Data:** Create visualizations of the Model Monitor data outputs.

---

By following these steps, you will build and deploy a robust image classification model using AWS services, ensuring it scales effectively and includes safeguards for performance monitoring.
