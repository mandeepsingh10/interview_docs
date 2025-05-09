# OTT Platform on AWS: System Architecture & Design Decisions


## 1. Introduction

**Core Pillars:**
* **Application:** EKS microservices, API Gateway, Cognito.
* **Video:** Elemental Link (live ingest), MediaConnect (optional routing), MediaLive (transcoding), MediaPackage (packaging), MediaConvert (VOD).
* **Storage:** S3 (video, logs, events), Aurora/RDS (catalog, subscriptions), DynamoDB (profiles, recommendations), ElastiCache.
* **Delivery:** CloudFront (API, video).
* **Recommendations/Analytics:** Kinesis suite (event ingest), SageMaker (ML), EMR (analytics).


## 2. Scaling Strategy

* **EKS Microservices:** Horizontal Pod Autoscaler (HPA) for pods, Karpenter for nodes.
* **Managed Services (API Gateway, Lambda, Kinesis, S3, CloudFront, Elemental Services, SageMaker, DynamoDB):** Scale automatically or offer configurable scaling.
* **Databases (Aurora/RDS, ElastiCache):** Vertical and horizontal (read replicas, sharding/clustering) scaling. Aurora Serverless v2 for auto-scaling.

## 3. Fault Tolerance and High Availability (HA)

* **Multi-AZ by Default/Configuration:**
    * **Live Ingest:** Redundant Elemental Link devices feed MediaLive "Standard" channels (dual-pipeline across AZs) or redundant MediaConnect flows.
    * **Compute/Data:** EKS, RDS/Aurora, Kinesis, S3, ElastiCache, Load Balancers deployed/configured across multiple AZs. For EKS, make sure the spread of microservice pods are even across AZs.
    * **Media Services:** MediaLive (Standard channels), MediaPackage, MediaConnect are designed for HA.

## 4. Security

* **Network:** VPCs, Security Groups, NACLs, AWS WAF (with CloudFront/API Gateway), AWS Shield (DDoS protection).
* **Identity:** IAM (least privilege for services/users), Cognito (end-user authentication/authorization).
* **Data Protection:**
    * **In-Transit:** TLS/SSL (HTTPS) for all external communication. Secure protocols for Elemental Link.
    * **At-Rest:** Encryption for S3, EBS, RDS/Aurora, DynamoDB, ElastiCache, EMRFS using AWS KMS.
* **API:** API Gateway for request validation, throttling, authorization.
* **Containers:** ECR vulnerability scanning, EKS network policies.

## 5. Monitoring, Alerting, and Logging

* **Amazon CloudWatch:**
    * **Metrics:** Centralized collection for AWS managed services (Elemental Link status, Kinesis, SageMaker, EMR, S3, Databases, etc.).
    * **Logs:** Centralized via CloudWatch Logs for AWS service logs (Firehose, SageMaker, VPC Flow Logs, etc.) and can receive EKS control plane logs.
* **Prometheus & Grafana (for EKS & Application Monitoring):**
    * **Prometheus:** Deployed within the EKS cluster (e.g., via AWS Managed Service for Prometheus or self-managed) to scrape detailed metrics from Kubernetes components (nodes, pods, containers) and custom application metrics exposed by microservices.
    * **Grafana:** Used for advanced visualization and dashboarding of metrics collected by Prometheus and potentially CloudWatch (via Grafana's CloudWatch data source). Provides customizable dashboards for deep dives into EKS and application performance.
    * **Alertmanager (with Prometheus):** Handles alerting based on metrics collected by Prometheus, complementing CloudWatch Alarms. Configured to send critical alerts to designated **Slack channels** for immediate team notification.
* **Logging (EKS Applications):**
    * Application logs from EKS pods are typically collected using Fluent Bit or Fluentd and can be routed to **Amazon CloudWatch Logs** for centralized storage and basic analysis, or to **Amazon OpenSearch Service** for more advanced querying and visualization within Grafana or OpenSearch Dashboards.
* **AWS CloudTrail:** API call auditing for all AWS services.

## 6. CI/CD Pipeline

* **Source Control:** GitHub (application code, Kubernetes manifests, IaC, ML code).
* **CI/CD (Microservices/Infra):** GitHub Actions (build, test, deploy IaC - Terraform).
* **GitOps (EKS):** ArgoCD for automated synchronization of Kubernetes applications from Git. ArgoCD is configured to send deployment status updates (e.g., successful sync, health degradation) to a dedicated **Slack channel** for team visibility.

## 7. Disaster Recovery (DR) Plan

* **Strategy:** Warm Standby in a DR AWS Region.
* **Data Replication:**
    * **S3:** CRR for VOD, logs, S3 User Interaction Events Data Lake, SageMaker model artifacts.
    * **Databases:** Snapshots and/or continuous replication (Aurora Global Database, DynamoDB Global Tables/backups) for catalog, user profiles, recommendations store.
    * **ECR:** Container image replication.
* **EKS Disaster Recovery:**
    * Use AWS Global Accelerator and Amazon Route 53 to distribute traffic to Kubernetes-hosted applications that run in two AWS Regions, a primary region that actively serves traffic and a second region that acts as failover.

## 8. Design Decisions (Why Specific Services Were Chosen)

* **Amazon EKS:** For managed Kubernetes, enabling scalable and resilient microservice orchestration with deep AWS integration.
* **API Gateway:** For a centralized, secure, and scalable entry point for all backend APIs, handling routing, auth, and traffic management.
* **Cognito:** For offloading user identity management, including authentication, authorization, and user federation.
* **AWS Elemental Link:** For simplified, reliable, and secure live video contribution directly into AWS Media Services from event sites.
* **AWS Elemental Media Services (MediaLive, MediaPackage, MediaConvert):** For broadcast-grade, scalable video processing: MediaLive for live ABR transcoding; MediaPackage for JIT packaging and DRM; MediaConvert for file-based VOD transcoding.
* **Amazon S3:** For highly durable, scalable, and cost-effective object storage for video assets, logs, event data, and static content.
* **Aurora/RDS:** For relational data requiring strong consistency, complex queries, and ACID properties, such as the master content catalog and subscription data.
* **DynamoDB:** For high-velocity, flexible-schema data needing low-latency key-value access at scale, like user profiles, watch history, and precomputed recommendations.
* **ElastiCache:** For in-memory caching to reduce latency and database load for frequently accessed data.
* **CloudFront:** For global, low-latency content delivery (video, APIs, static assets) via its extensive edge network.
* **Kinesis Suite (Data Streams, Data Firehose):** For a scalable, real-time event ingestion pipeline for user interactions, ensuring durable and reliable data delivery to S3.
* **SageMaker:** For its comprehensive ML capabilities, including SageMaker Pipelines, to build, train, and deploy recommendation models.
* **EMR:** For large-scale batch processing and analytics on user interaction data in S3
* **OpenSearch Service:** For robust content search functionality and for ingesting, analyzing, and visualizing application logs and usage analytics.
* **GitHub & GitHub Actions:** For version control and CI/CD automation
* **ArgoCD:** For GitOps-based continuous delivery to EKS

