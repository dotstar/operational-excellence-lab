# Mythical Mysfits: A Micro-services application for Operational Excellence Exploration

## Overview
![mysfits-welcome](/images/mysfits-welcome.png)

**Mythical Mysfits** is a (fictional) pet adoption non-profit dedicated to helping abandoned, and often misunderstood, mythical creatures find a new forever family! Mythical Mysfits believes that all creatures deserve a second chance, even if they spent their first chance hiding under bridges and unapologetically robbing helpless travelers.

Our first adoption agency, founded in Devils Tower National Monument, has helped millions of mythical mysfits find loving homes. Since then, we've deployed expedition teams to far reaching corners of the Earth to seek out more wandering communities of mythical mysfits in need of care and hugs. Initial reports indicate that we'll need to expand our operation globally.

To recap our progress to date, we've modernized our stack to be containerized microservices deployed with AWS Fargate. We manage our resources using infrastructure as code and have a fully automated CI/CD pipeline that deploys our code changes. 

We have two micro-services, almost ready to push into production, however we didn't plan for our operational requirements.  In this lab, we will look at AWS X-Ray as a troubleshooting tool for micro-services and AWS CloudWatch Dashboards to quickly ascertain service health.  This is a small, but important, piece of the _Operational Excellence_ pilar.  We are trying to answer the question: _How do you understand the health of your workload?_

### Note
This is a fork of the excellent workshop [aws-multi-region](https://github.com/aws-samples/aws-multi-region-bc-dr-workshop.git).  This version is for a single region, and we pre-bake some of the tasks associated with instrumenting the application for x-ray.  For a more immersive experience, please take a run through that workshop.

Our focus is to look at a couple of alternatives for instrumentation which are consistent with the Operatonal Excellence and Performance Efficiency pillars of the [AWS Well Architected Framework](https://aws.amazon.com/architecture/well-architected/).
### Requirements

* AWS account - if you're doing this workshop as a part of an AWS event, you will be provided an account through a platform called Event Engine. The workshop administrator will provide instructions. If the event specifies you'll need your own account or if you're doing this workshop on your own, it's easy and free to [create an account](https://aws.amazon.com/) if you do not have one already.
* If using your own AWS account, create and use an IAM account with elevated privileges. Easiest option is to create an IAM user with admin privileges.

Familiarity with AWS, Python, [Docker](https://www.docker.com/), networking, CI/CD, and git is a plus but not required.

### What you'll do

The labs in the workshop are designed to be completed in sequence, and the full set of instructions are documented in each lab. Read and follow the instructions to complete each of the labs. Don't worry if you get stuck, we provide hints along the way.

* **[Lab 0](lab-0-init):** Deploy existing Mythical stack
* **[Lab 1](lab-1-xray):** Improve microservices observability with distributed tracing
* **[Lab 2](lab-2-agg):** Build an operational dashboard

<!-- * **[Bonus Lab](/):** [DOES NOT EXIST YET] Implement automated failover and active-active-->
* **Workshop Cleanup** [Cleanup working environment](#important-workshop-cleanup)

### Conventions

#### 1. Commands

Throughout this workshop, we will provide commands for you to run in a terminal. These commands will look like this:

<pre>
$ ssh -i <b><i>PRIVATE_KEY.PEM</i></b> ec2-user@<b><i>EC2_PUBLIC_DNS_NAME</i></b>
</pre>

The command starts **after** the $.

#### 2. Unique values

If you see ***UPPER_ITALIC_BOLD*** text, that means you need to enter a value unique to your environment. For example, the ***PRIVATE\_KEY.PEM*** above refers to the private key of an SSH key pair that's specific to your account; similarly, the ***EC2_PUBLIC_DNS_NAME*** refers to the DNS name of an EC2 instance in your account.

All unique values required throughout the workshop are captured as outputs from the CloudFormation template you'll launch to set up the workshop environment. You can, of course, also visit the specific service's dashboard in the [AWS management console](https://console.aws.amazon.com).

#### 3. Specific values or text

If you are asked to enter a specific value or text, it will formatted like this - `verbatim`.

#### 4. Hints

Hints are also provided along the way and will look like this:

<details>
<summary>HINT</summary>

**Nice work, you just revealed a hint!**
</details>

*Click on the arrow to show the contents of the hint.*

### IMPORTANT: Workshop Cleanup

If you're attending an AWS event and are provided an account to use, you can ignore this section because we'll destroy the account once the workshop concludes. Feel free to proceed to [Lab-0 to get started](lab-0-init).

**If you are using your own account**, it is **VERY** important you clean up resources created during the workshop. Follow these steps once you're done going through the workshop to delete resources that were created:

1. Delete any manually created assets - for example, Global Accelerator from lab 4 (if you got to that point).
2. Navigate to the [CloudFormation dashboard](https://console.aws.amazon.com/cloudformation/home#/stacks) in the primary region and click on your workshop stack name to load stack details.
3. Click **Delete** to delete the stack.
4. Repeat steps 2-3 for the secondary region.

<details>
<summary>Troubleshooting: Stack delete failed</summary>
There are helper Lambda functions that should clean things up when you delete the main stack. However, if there's a stack deletion failure due to a race condition, follow these steps:

1. In the CloudFormation dashboard, click on the **Events** section, and review the event stream to see what failed to delete
2. Manually delete those resources by visiting the respective service's dashboard in the management console
3. Once you've manually deleted the resources, try to delete the main workshop CloudFormation stack again. Repeat steps 1-3 if you still see deletion failures

</details>

* * *

## Let's Begin!

[Go to Lab-0 to set up your environment](lab-0-init)
