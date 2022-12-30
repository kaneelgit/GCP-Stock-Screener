provider "google" {

    project = local.project
    region = local.region

}

data "google_billing_account" "account" {

    display_name = var.billing_account_name

}

resource "google_project" "project" {

    name = local.project_name
    project_id = local.project
    billing_account = data.google_billing_account.account.id

}

resource "google_project_iam_member" "project_owner" {

    role = "roles/owner"
    member = "user:${var.user}"
    project = local.project_name

    depends_on = [
        google_project.project
    ]

}

resource "google_storage_bucket" "storage_csv_bucket" {

    name = local.csv_output_bucket
    location = "US"
    force_destroy = true
    
    depends_on = [
        google_project_iam_member.project_owner
    ]

}

resource "google_storage_bucket" "storage_pdf_bucket" {

    name = local.pdf_output_bucket
    location = "US"
    force_destroy = true

    depends_on = [
        google_project_iam_member.project_owner
    ]

}

resource "google_project_service" "cloud_registry_service" {

  service = "containerregistry.googleapis.com"
  disable_dependent_services = true

  depends_on = [
    google_project.project,
  ]

}

resource "google_project_service" "cloud_build_service" {

  service = "cloudbuild.googleapis.com"
  disable_dependent_services = true

  depends_on = [
    google_project.project,
    google_project_iam_member.project_owner
  ]

}


resource "google_project_service" "cloud_run_service" {

  service = "run.googleapis.com"
  disable_dependent_services = true

  depends_on = [
    google_project.project,
  ]

}


resource "google_project_service" "iam_api" {

  service = "iam.googleapis.com"
  disable_dependent_services = true
  
  depends_on = [
    google_project.project,
  ]
}



resource "google_project_service" "scheduler_api" {

  service = "cloudscheduler.googleapis.com"
  disable_dependent_services = true
  depends_on = [
    google_project.project,
  ]
}

#create cloud run service using the image
resource "google_cloud_run_service" "default" {
  
  project = local.project_name
  name     = local.cloud_app_name 
  location = local.region

  template {
    spec {
      containers {
        image = local.image_uri 

      }
    }
  }
  traffic {
    percent         = 100
    latest_revision = true
  }
  depends_on = [
    google_project.project,
    google_project_service.cloud_run_service, 
  ]
}



resource "null_resource" "app_container" {

    provisioner "local-exec" {
        command = "cd ../screener_app && gcloud config set project ${local.project} && gcloud builds submit --tag ${local.image_uri}"
    }

    depends_on = [
        google_project.project,
        google_project_service.cloud_build_service,
        google_project_iam_member.project_owner
    ]
}



resource "google_service_account" "default" {
  account_id   = "scheduler-sa"
  description  = "Cloud Scheduler service account; used to trigger scheduled Cloud Run jobs."
  display_name = "scheduler-sa"

  # Use an explicit depends_on clause to wait until API is enabled
  depends_on = [
    google_project_service.iam_api,
    google_project.project,
  ]
}


resource "google_cloud_scheduler_job" "default" {
  name             = "scheduled-cloud-run-job"
  description      = "Invoke a Cloud Run container on a schedule."
  schedule         = "30 22 * * *"
  time_zone        = "America/New_York"
  attempt_deadline = "320s"

  retry_config {
    retry_count = 3
  }

  http_target {
    http_method = "POST"
    uri         = google_cloud_run_service.default.status[0].url

    oidc_token {
      service_account_email = google_service_account.default.email
    }
  }

  # Use an explicit depends_on clause to wait until API is enabled
  depends_on = [
    google_project_service.scheduler_api,
    google_project.project,
  ]
}

resource "google_cloud_run_service_iam_member" "default" {

  location = google_cloud_run_service.default.location
  service  = google_cloud_run_service.default.name
  role     = "roles/run.invoker"
  member   = "serviceAccount:${google_service_account.default.email}"

  depends_on = [
    google_project.project,
    google_cloud_run_service.default,
  ]

}
