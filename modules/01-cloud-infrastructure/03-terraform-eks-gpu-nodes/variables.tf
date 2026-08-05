variable "region" {
  description = "AWS region"
  type        = string
  default     = "us-west-2"
}

variable "cluster_name" {
  description = "EKS cluster name"
  type        = string
}

variable "node_group_name" {
  description = "Name of the GPU node group"
  type        = string
  default     = "eks-gpu-nodes"
}

variable "instance_types" {
  description = "List of instance types for GPU node group"
  type        = list(string)
  default     = ["g5.2xlarge"]
}

variable "min_size" {
  description = "Minimum nodes"
  type        = number
  default     = 0
}

variable "max_size" {
  description = "Maximum nodes"
  type        = number
  default     = 4
}

variable "desired_capacity" {
  description = "Desired capacity"
  type        = number
  default     = 0
}

variable "disk_size" {
  description = "EBS volume size in GB for nodes"
  type        = number
  default     = 100
}

variable "ssh_key_name" {
  description = "Optional SSH key name for nodes"
  type        = string
  default     = ""
}
