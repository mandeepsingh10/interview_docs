# SolarWinds Senior DevOps/SRE Interview – Interviewer Questions

## Kubernetes & Cluster Management

1. What is the difference between Deployment, DaemonSet, and StatefulSet in Kubernetes? When would you prefer one over the other?
2. How do clients connect to StatefulSets, and why would they prefer them over Deployments?
3. How do you ensure that traffic is not sent to pods before they're ready, and how do pods recover from runtime issues?
4. What’s the difference between readiness and liveness probes? What happens if each of them fails?
5. How do you define CPU and memory resources for pods? What are requests and limits?
6. What happens when a pod breaches its CPU or memory limits?
7. What are some good security practices to run a pod securely in a Kubernetes cluster?
8. Have you tried any approaches to secure pod-to-pod communication in your clusters?
9. How do you ensure high availability (HA) for your applications running on Kubernetes?
10. Will pod anti-affinity alone ensure pods are spread across different AZs?
11. What is the function of `maxSkew` in pod scheduling?
12. How can you fetch a core dump file from a pod that crashes (e.g., Java OOM)?
13. Drain and cordon commands? Explain drain and cordon commands and what do they do.
14. How do you manage ingress and egress on your clusters?
15. What problems were you trying to solve when you implemented Karpenter?

## AWS Infrastructure & Networking

16. What are the main AWS services that you have interacted with?
17. You have to deploy a new infrastructure in AWS. How will you plan this out, starting from the VPC design? What all things will you consider and how will you set up your subnets?
18. How do you differentiate between private and public subnet?
19. How do you turn on the internet access for a public subnet?
20. How do you turn on the internet access for a private subnet?

## CI/CD & Automation

21. How do you manage CD part of your cluster?
22. Do you have experience automating Terraform-based workloads?
23. What are the benefits you’ve observed from using Terragrunt instead of Terraform?
24. How would you import a manually created RDS instance into Terraform?
25. Can you force Terraform to "forget" about a resource and manage it manually without interfering with others?

## EKS Specific

26. Have you done any EKS upgrades recently? How do you plan and execute them?

## Observability & Monitoring

27. What is the difference between Gauge, Counter, and Histogram in Prometheus?
28. How would you monitor a Java-based application deployed in Kubernetes? What kind of alerts would you set up?
29. Have you been involved in setting up SLOs or SLIs?
30. What indicators would you use to define SLOs and SLIs for a Java-based API service?
31. Is CPU usage a good SLI? What other indicators would be better?

## Database Management

32. What is your experience with databases?
33. How do you manage creation of new schemas on a database?
34. How do you monitor databases and what kind of metrics will you monitor for databases?
35. What will be the best practices to set up databases in the cloud to ensure HA?
36. In case of multiple read replicas, could there be a case where we get old data because of replication delay? Read-after-write consistency. What could be a workaround for this?

## Security & Access Control

37. Is there a better way of giving S3 access to a pod without granting it to the entire node?
38. How would you configure a service account in a pod to access S3? Does this require node-level changes?

## Incident Management

39. Have you participated in on-call rotations?
40. Have you handled any major production incidents? Can you describe your role and the incident management process?
41. What were the major changes you made after a production incident?
