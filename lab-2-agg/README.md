# Mythical Mysfits: A Micro-services application for Operational Excellence Exploration

![mysfits-welcome](../images/mysfits-welcome.png)

## Workshop progress
✅ [Lab 0: Workshop Initialization](../lab-0-init)

✅ [Lab 1: Instrument Observability - Distributed Tracing with AWS X-Ray](../lab-1-xray)

**Lab 2: Operationalize Observability - Aggregate Metrics**
* [Explore pre-configured CloudWatch dashboard](#1-explore-pre-configured-cloudwatch-dashboard)
* [Add newly instrumented error and fault metrics from X-Ray](#2-add-newly-instrumented-error-and-fault-metrics-from-x-ray)

[Lab 3: Preparing for Multi-Region Deployments](../lab-3-mr-prep)

[Lab 4: Implement Traffic Management - Global Accelerator](../lab-4-globalacc)

[Lab 5: Load Test and Failover your multi-region application](../lab-5-loadtest)

## LAB 2 - Operationalize Observability - Aggregate Metrics

In this lab, you will start the process of aggregating metrics to understand the health of your application so you can make informed decisions about when to fail over to a different region. We will use an Amazon CloudWatch Dashboard for this.

Our CloudWatch dashboard should include metrics from the key components of our system and application. In this case, the metrics we should display on a dashboard are the following:

* Fargate task capacity (CPU / Mem)
* ALB requests per minute
* ALB HTTP 200, 400 and 500 responses
* Application faults and errors reported by AWS X-Ray

Here's a reference image showing what your CloudWatch dashboard may look like when complete -
![image](https://user-images.githubusercontent.com/23423809/69607429-14888580-0fda-11ea-9ec1-bd6ffa16b2b0.png)

Luckily, the previous engineer already started the task of creating the dashboard for you, adding some basic metrics regarding Load Balancer health and the Core and Like service metrics from the ECS Tasks. There are still some additional metrics to add, however. The dashboard can be located by navigating to the CloudWatch service and selecting <stackname>-Dashboard.

Here's what you'll be doing:

* Open up the pre-configured CloudWatch dashboard
* Add metrics to the dashboard X-Ray Errors
* Save the dashboard

### Instructions

### [1] Explore pre-configured CloudWatch dashboard

1. Navigate to the Amazon [CloudWatch service](https://console.aws.amazon.com/cloudwatch/) from the Management Console
2. Select **Dashboards** from the menu on the left
3. Select the CloudWatch dashboard that contains the name **Dashboard**

### [2] Add newly instrumented error and fault metrics from X-Ray

In the previous Lab, you instrumented the Like service with AWS X-Ray which provides greater visibility into individual requests passing through the Like service. You also created a Trace Group that will filter out the faults and errors that X-Ray has captured from the application. Create a widget on the CloudWatch dashboard to show the number of errors and faults that X-Ray has observed from the trace information. X-Ray pushes these metrics to CloudWatch so that we can display them on the dashboard. Use the step by step instructions below if required.

Reminder: [What is an AWS X-Ray trace?](https://docs.aws.amazon.com/xray/latest/devguide/xray-concepts.html#xray-concepts-traces)

<details>
<summary>Step by step instructions:</summary>

1. Click on the **Add Widget** button in the CloudWatch dashboard
  ![image](https://user-images.githubusercontent.com/23423809/69609253-e9a03080-0fdd-11ea-9090-40568a536874.png)

2. Select **Stacked area** and press **Configure**

3. Give the widget a name, then select **X-Ray** followed by **Group Metrics** and select the Group created in the X-Ray lab previously (like-service-errors-faults).
![image](https://user-images.githubusercontent.com/23423809/69609559-a8f4e700-0fde-11ea-89aa-9375ce0db044.png)

4. Select the tab marked **Graphed metrics** and change the Statistic to **Sum**. Press **Create widget**
![image](https://user-images.githubusercontent.com/23423809/69609745-1acd3080-0fdf-11ea-9958-70416f6408f0.png)

5. Move the widget to anywhere on the dashboard
6. Save the dashboard by pressing **Save dashboard**

</details>

### [3] Create a CloudWatch Canary

Amazon CloudWatch Synthetics enables you to create canaries to monitor your endpoints and APIs. Canaries are configurable scripts that follow the same routes and perform the same actions as a customer. This enables the outside-in view of your customers’ experiences, and your service’s availability from their point of view. 

1. Navigate to the Amazon [CloudWatch service](https://console.aws.amazon.com/cloudwatch/) from the Management Console
2. Select **Canaries** from the menu on the left, near the bottom
3. Click "**Create Canary**"
4. _Use a **blueprint**_
5. _API canary_
6. Name "mythical_core_api"
7. Method: GET
8. recall the URL of your Mysfits core service
   ```
    jq < ~/environment/operational-excellence-lab/cfn-output.json -er '.LoadBalancerDNS'                                                                                          
   ```
9. Add the Service endpoint URL to the URL for Canary, for example: http://alb-mm8-626376333.us-east-2.elb.amazonaws.com

10. Click "Create Canary" at bottom of the page.

   After several minutes, the Canary will begin to poll the API endpoint, and log the response time.

11. Time permitting, add the Canary results to your CloudWatch Dashboard.  Hint - the value you are looking for is in All -> CloudWatchSynthetics -> mythical-core-api -> Duration.

AWS announced CloudWatch Synthetics at re:Invent 2019.  The service preview is available in Ohio, Virginia, and Ireland.




# Lab Complete

Excellent, you've completed building out the operational CloudWatch dashboard by adding a widget that graphs X-Ray trace data collected from the Like service; specifically you're using the faults and errors filter expression group to isolate 4xx/5xx status codes to be displayed.

You also added a canary, to baseline service response time from outside your VPC.

