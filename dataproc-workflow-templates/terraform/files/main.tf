terraform {
  backend "gcs" {
    bucket  = "gcs-dataproc-workflow-templates"
    prefix  = "terraform/state"
  }
}

resource "google_data_catalog_taxonomy" "my_taxonomy" {
  provider = google-beta
  region = var.region
  display_name =  var.taxonomy_display_name
  description = var.taxonomy_description
  activated_policy_types = [var.taxonomy_activated_policy_types]
  project = var.project
}

resource "google_data_catalog_policy_tag" "parent_policy_high" {
  provider = google-beta
  taxonomy = google_data_catalog_taxonomy.my_taxonomy.id
  display_name = var.parent_policy_high_display_name
  description = var.parent_policy_high_description
  depends_on = [google_data_catalog_taxonomy.my_taxonomy]
}

resource "google_data_catalog_policy_tag" "parent_policy_medium" {
  provider = google-beta
  taxonomy = google_data_catalog_taxonomy.my_taxonomy.id
  display_name = var.parent_policy_medium_display_name
  description = var.parent_policy_medium_description
  depends_on = [google_data_catalog_taxonomy.my_taxonomy]
}

resource "google_data_catalog_policy_tag" "child_policy_restricted" {
  provider = google-beta
  taxonomy = google_data_catalog_taxonomy.my_taxonomy.id
  display_name = var.child_policy_restricted_display_name
  description = var.child_policy_restricted_description
  parent_policy_tag = google_data_catalog_policy_tag.parent_policy_high.id
  depends_on = [google_data_catalog_policy_tag.parent_policy_high]
}

resource "google_data_catalog_policy_tag" "child_policy_confidential" {
  provider = google-beta
  taxonomy = google_data_catalog_taxonomy.my_taxonomy.id
  display_name = var.child_policy_confidential_display_name
  description = var.child_policy_confidential_description
  parent_policy_tag = google_data_catalog_policy_tag.parent_policy_medium.id
  depends_on = [google_data_catalog_policy_tag.parent_policy_medium]
}

