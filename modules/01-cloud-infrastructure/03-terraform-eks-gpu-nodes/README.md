Terraform module to provision AWS EKS GPU node groups (g5/p4)

Overview
This module demonstrates how to create EKS managed node groups for GPU instances (for training or inference) with taints so that GPU workloads are scheduled explicitly. It also includes autoscaling settings and an example IAM role assumption snippet.

Important notes
- This configuration assumes an EKS cluster already exists (cluster name and kubeconfig).
- Ensure the AWS account has AMIs that support the target instance types. For newer instances (p4), ensure your region supports them.
- Node taints prevent non-GPU pods from being scheduled inadvertently.

Quick usage
1. Set variables in variables.tf or via CLI/environment.
2. terraform init && terraform apply
