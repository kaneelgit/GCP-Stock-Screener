variable "billing_account_name" {
    default = "" #enter billing account name here
}

variable "user" {
    default = "" #enter user email address here
}

locals {

    project_name = "stock-screener-${random_id.id.hex}" #enter your project name
    project = "${local.project_name}"
    region = "us-east1"

    #storage bucket names
    csv_output_bucket = "screener_csv_bucket" #enter your unique csv bucket name. Also change the csv bucket name in the screener_app/app.py file
    pdf_output_bucket = "screener_pdf_bucket" #enter your unique pdf bucket name. Also change the pdf bucket name in the screener_app/app.py file
    
    #container image info
    container_image_name = "screener-image" #enter your container image name
    image_name = "gcr.io/${local.project}/${local.container_image_name}"
    image_tag = "latest"
    image_uri = "${local.image_name}:${local.image_tag}" #substitute with the app image uri

    #cloud run app name
    cloud_app_name = "screener-cloudrun"

}


resource "random_id" "id" {

    byte_length = 2

}