# ---------- Lambda Function ------------- #

# Template file
data "template_file" "wget" {
  template = file("./src/third_party_lib/wget.py")
}

data "template_file" "imdb_data_injection_lambda" {
  template = file("./src/aws_lambda/imdb_data_injection_lambda.py")
}

data "template_file" "movie_lens_data_injection_lambda" {
  template = file("./src/aws_lambda/movie_lens_data_injection_lambda.py")
}

data "template_file" "data_analysis_lambda" {
  template = file("./src/aws_lambda/data_analysis_lambda.py")
}

data "template_file" "data_analysis_imdb_query" {
  template = file("./src/aws_lambda/data_analysis_imdb_query.py")
}

data "template_file" "data_analysis_movie_lens_query" {
  template = file("./src/aws_lambda/data_analysis_movie_lens_query.py")
}

# Archive file
data "archive_file" "imdb_data_injection_lambda_file" {
  type        = "zip"
  output_path = "./src/aws_lambda/imdb_data_injection_lambda.zip"

  source {
    content  = data.template_file.wget.rendered
    filename = "wget.py"
  }

  source {
    content  = data.template_file.imdb_data_injection_lambda.rendered
    filename = "imdb_data_injection_lambda.py"
  }
}

data "archive_file" "movie_lens_data_injection_lambda_file" {
  type        = "zip"
  output_path = "./src/aws_lambda/movie_lens_data_injection_lambda.zip"

  source {
    content  = data.template_file.wget.rendered
    filename = "wget.py"
  }

  source {
    content  = data.template_file.movie_lens_data_injection_lambda.rendered
    filename = "movie_lens_data_injection_lambda.py"
  }
}

data "archive_file" "data_analysis_lambda_file" {
  type        = "zip"
  output_path = "./src/aws_lambda/data_analysis_lambda.zip"

  source {
    content  = data.template_file.data_analysis_lambda.rendered
    filename = "data_analysis_lambda.py"
  }

  source {
    content  = data.template_file.data_analysis_imdb_query.rendered
    filename = "data_analysis_imdb_query.py"
  }

  source {
    content  = data.template_file.data_analysis_movie_lens_query.rendered
    filename = "data_analysis_movie_lens_query.py"
  }
}

# ---------- Glue ------------- #
resource "aws_s3_bucket_object" "imdb_data_cleansing_glue_script" {
  key    = "script/glue/imdb_data_cleansing_glue.py"
  bucket = aws_s3_bucket.main.id
  source = "./src/aws_glue/imdb_data_cleansing_glue.py"
  etag   = filemd5("./src/aws_glue/imdb_data_cleansing_glue.py")
  tags   = var.tags
}

resource "aws_s3_bucket_object" "movie_lens_data_cleansing_glue_script" {
  key    = "script/glue/movie_lens_data_cleansing_glue.py"
  bucket = aws_s3_bucket.main.id
  source = "./src/aws_glue/movie_lens_data_cleansing_glue.py"
  etag   = filemd5("./src/aws_glue/movie_lens_data_cleansing_glue.py")
  tags   = var.tags
}

resource "aws_s3_bucket_object" "data_transformation_glue_script" {
  key    = "script/glue/data_transformation_glue.py"
  bucket = aws_s3_bucket.main.id
  source = "./src/aws_glue/data_transformation_glue.py"
  etag   = filemd5("./src/aws_glue/data_transformation_glue.py")
  tags   = var.tags
}

# -------------------------------------------------------------- #
# --------------------------- Web ------------------------------ #
# -------------------------------------------------------------- #

# ---------- Lambda Function ------------- #
# Template file
data "template_file" "data_service_lambda" {
  template = file("./src/aws_lambda/data_service_lambda.js")
}

# Archive file
data "archive_file" "data_service_lambda_file" {
  type        = "zip"
  output_path = "./src/aws_lambda/data_service_lambda.zip"

  source {
    content  = data.template_file.data_service_lambda.rendered
    filename = "data_service_lambda.js"
  }
}

# ---------- Web bucket ------------- #
resource "aws_s3_bucket" "mpd_web_bucket" {
  bucket = "moviedataplatform.com"
  acl    = "public-read"
  force_destroy = true

  website {
    index_document = "index.html"
    error_document = "index.html"
  }

  tags   = var.tags
}

output "website_domain" {
  value = "${aws_s3_bucket.mpd_web_bucket.website_domain}"
}

output "website_endpoint" {
  value = "${aws_s3_bucket.mpd_web_bucket.website_endpoint}"
}

resource "aws_s3_bucket_policy" "bucket_policy" {
  bucket = aws_s3_bucket.mpd_web_bucket.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid       = "PublicReadGetObject"
        Effect    = "Allow"
        Principal = "*"
        Action    = "s3:GetObject"
        Resource  = "${aws_s3_bucket.mpd_web_bucket.arn}/*"
      },
    ]
  })
}

# ---------- S3 Bucket Object ------------- #
resource "aws_s3_bucket_object" "mpd_web_bucket_object" {
  for_each = fileset("src/web/build/", "**/*")

  bucket = aws_s3_bucket.mpd_web_bucket.id
  key    = each.value
  source = "src/web/build/${each.value}"
  etag   = filemd5("src/web/build/${each.value}")

  content_type  = lookup(local.content_type_map, regex("\\.(?P<extension>[A-Za-z0-9]+)$", each.value).extension, "application/octet-stream")
}

# MIME type mapping
locals {
  src_dir      = "src/web/build"
  content_type_map = {
    html        = "text/html",
    txt         = "text/plain",
    js          = "application/javascript",
    css         = "text/css",
    svg         = "image/svg+xml",
    jpg         = "image/jpeg",
    ico         = "image/x-icon",
    png         = "image/png",
    gif         = "image/gif",
    map         = "application/json",
    pdf         = "application/pdf"
  }
}


# ---------- IAM Policy Data ------------- #
data "template_file" "mdp_user_policy_data" {
  template = file("aws_policy/mdp_user_policy.json")
  vars = {
    s3_bucket_arn = aws_s3_bucket.main.arn
  }
}

data "template_file" "mdp_lambda_policy_data" {
  template = file("aws_policy/mdp_lambda_policy.json")
  vars = {
    s3_bucket_arn = aws_s3_bucket.main.arn
  }
}

data "template_file" "mdp_glue_policy_data" {
  template = file("aws_policy/mdp_glue_policy.json")
  vars = {
    s3_bucket_arn = aws_s3_bucket.main.arn
  }
}
