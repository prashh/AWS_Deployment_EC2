# AWS_Deployment_EC2
Static webpage hosting on AWS EC2 instance.

**Prerequisites :** 
  
  1.  Spin up your favorite Python IDE and create a new project.
  2.  Create your main project file and name it whatever you want — I chose “app.py” for simplicity.
  3.  Next, we need to install Amazon’s SDK "boto3". Open a terminal and type sudo pip3 install boto3.
  4.  Add import boto3 to the top of your Python file.
   
This allows us to use Amazon’s SDK in our Python application
 
 
**Github source :**
  
  1. Create a static webapp and make it public.
  2. Use the clone url(HTTPS) to retrive the code for deployment.


**AWS Credentials :**

Before we can actually use anything on AWS, we need credentials for the AWS account.

  1.  Go to your IAM panel and click “Add user” under the “Users” tab.
  2.  Enter a username and tick the box beside “programmatic access.”
  3.  Click “Next: Permissions” and create a new group, if needed.
  4.  For the purposes of this project, I’ll create a new group with the “AdministratorAccess” policy. This gives us permission to manage everything in our AWS console programmatically.
  5.  Click “Next: Tags” and add any relevant information. This is optional.
  6.  Click “Review,” then “Create User”
  7.  Download your security credentials (the CSV file) and copy it into your project’s root directory.
  
  
**Create key pairs :**
  1.  Head over to your AWS dashboard and go to EC2 -> Network & Security -> Key pairs
  2.  click “Create key pair”.
  3.  Enter a name and hit “Create.”
  
  
To run commands on the server and open it to the Web, we have to create a security group and IAM role on AWS. Go to your dashboard.

**Creating a security group :**

  1.  Navigate to Network & Security -> Security Groups.
  2.  Create a security group, and open ports 22, 80, 443, and 5000. This will allow general access to it from the Web. Allow all IPs to access them.


**Creating an IAM role:**

  1.  Go to your AWS dashboard and navigate to the IAM service.
  2.  Click on the “Roles” tab.
  3.  Click “Create role” and select “EC2.” For the purposes of this project, you’ll want to select “Administrator Access”.
  4.  Click through the rest of the steps to create a role.


**How to run:**

  Run the command : python app.py
  from the directory which contains the file.(It needs to contain the credentials.csv file as well)


**What is running:**

  It creates a EC2 instance on AWS with the given specifications with the web app deployed on the said URL until it is stopped or terminated


**How to cleanup:**

  Launch the console (log in as root) and navigate to the EC2 Dashboard, Search for the instance that you created by the public DNS that you use to test the webapp and right click on it -> Launch State -> Terminate.
						 							
  
 						
					 				
			
		
 
