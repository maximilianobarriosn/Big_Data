variable "project" {
  type = string
}

variable "region" {
  type = string
}

variable "taxonomy_display_name" {
  type = string
}

variable "taxonomy_description" {
    type = string
}

variable "taxonomy_activated_policy_types" {
    type = string
}

variable "parent_policy_high_display_name" {
  type = string
}

variable "parent_policy_medium_display_name" {
    type = string
}

variable "parent_policy_high_description" {
  type = string
}

variable "parent_policy_medium_description" {
    type = string
}

variable "child_policy_restricted_display_name" {
  type = string
}

variable "child_policy_confidential_display_name" {
    type = string
}

variable "child_policy_restricted_description" {
  type = string
}

variable "child_policy_confidential_description" {
    type = string
}

variable "dev_bucket" {
    type = string
}

