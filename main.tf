# ---------- CloudWatch EventBridge ------------- #
resource "aws_cloudwatch_event_rule" "data_injection_event_rule" {
  name                = "data_injection_event_rule"
  schedule_expression = "cron(0 1 1 4 ? *)"
}

resource "aws_cloudwatch_event_target" "imdb_data_injection_event_target" {
  arn  = aws_lambda_function.imdb_data_injection_lambda.arn
  rule = aws_cloudwatch_event_rule.data_injection_event_rule.id
}

resource "aws_cloudwatch_event_target" "movie_lens_data_injection_event_target" {
  arn  = aws_lambda_function.movie_lens_data_injection_lambda.arn
  rule = aws_cloudwatch_event_rule.data_injection_event_rule.id
}

# ---------- Lambda Function ------------- #
resource "aws_lambda_function" "imdb_data_injection_lambda" {
  function_name    = "imdb_data_injection_lambda"
  filename         = "./src/aws_lambda/imdb_data_injection_lambda.zip"
  source_code_hash = data.archive_file.imdb_data_injection_lambda_file.output_base64sha256
  handler          = "imdb_data_injection_lambda.lambda_handler"
  runtime          = "python3.8"
  timeout          = 300
  memory_size      = 4096
  role             = aws_iam_role.mdp_lambda_role.arn
  tags             = var.tags
}
resource "aws_lambda_function" "movie_lens_data_injection_lambda" {
  function_name    = "movie_lens_data_injection_lambda"
  filename         = "./src/aws_lambda/movie_lens_data_injection_lambda.zip"
  source_code_hash = data.archive_file.movie_lens_data_injection_lambda_file.output_base64sha256
  handler          = "movie_lens_data_injection_lambda.lambda_handler"
  runtime          = "python3.8"
  timeout          = 300
  memory_size      = 4096
  role             = aws_iam_role.mdp_lambda_role.arn
  tags             = var.tags
}

resource "aws_lambda_function" "data_analysis_lambda" {
  function_name    = "data_analysis_lambda"
  filename         = "./src/aws_lambda/data_analysis_lambda.zip"
  source_code_hash = data.archive_file.data_analysis_lambda_file.output_base64sha256
  handler          = "data_analysis_lambda.lambda_handler"
  runtime          = "python3.8"
  timeout          = 900
  memory_size      = 4096
  role             = aws_iam_role.mdp_lambda_role.arn
  tags             = var.tags
}

# ---------- Glue ------------- #
resource "aws_glue_job" "imdb_data_cleansing_glue" {
  name              = "imdb_data_cleansing_glue"
  role_arn          = aws_iam_role.mdp_glue_role.arn
  glue_version      = "2.0"
  number_of_workers = "2"
  worker_type       = "Standard"
  timeout           = "1440"
  max_retries       = 0
  command {
    name            = "glueetl"
    script_location = "s3://${var.app}.${var.label}/script/glue/imdb_data_cleansing_glue.py"
    python_version  = 3
  }
  default_arguments = {
    "--aws_region"                       = var.region
    "--job_name"                         = "imdb_data_cleansing_glue"
    "--s3_bucket"                        = "${var.app}.${var.label}"
    "--job-language"                     = "python"
    "--job-bookmark-option"              = "job-bookmark-disable"
    "--enable-continuous-cloudwatch-log" = "true"
    "--enable-continuous-log-filter"     = "true"
    "--enable-metrics"                   = "true"
  }
  tags = var.tags
}

resource "aws_glue_job" "movie_lens_data_cleansing_glue" {
  name              = "movie_lens_data_cleansing_glue"
  role_arn          = aws_iam_role.mdp_glue_role.arn
  glue_version      = "2.0"
  number_of_workers = "2"
  worker_type       = "Standard"
  timeout           = "1440"
  max_retries       = 0
  command {
    name            = "glueetl"
    script_location = "s3://${var.app}.${var.label}/script/glue/movie_lens_data_cleansing_glue.py"
    python_version  = 3
  }
  default_arguments = {
    "--aws_region"                       = var.region
    "--job_name"                         = "movie_lens_data_cleansing_glue"
    "--s3_bucket"                        = "${var.app}.${var.label}"
    "--job-language"                     = "python"
    "--job-bookmark-option"              = "job-bookmark-disable"
    "--enable-continuous-cloudwatch-log" = "true"
    "--enable-continuous-log-filter"     = "true"
    "--enable-metrics"                   = "true"
  }
  tags = var.tags
}

resource "aws_glue_job" "data_transformation_glue" {
  name              = "data_transformation_glue"
  role_arn          = aws_iam_role.mdp_glue_role.arn
  glue_version      = "2.0"
  number_of_workers = "2"
  worker_type       = "Standard"
  timeout           = "1440"
  max_retries       = 0
  command {
    name            = "glueetl"
    script_location = "s3://${var.app}.${var.label}/script/glue/data_transformation_glue.py"
    python_version  = 3
  }
  default_arguments = {
    "--aws_region"                       = var.region
    "--job_name"                         = "data_transformation_glue"
    "--s3_bucket"                        = "${var.app}.${var.label}"
    "--job-language"                     = "python"
    "--job-bookmark-option"              = "job-bookmark-disable"
    "--enable-continuous-cloudwatch-log" = "true"
    "--enable-continuous-log-filter"     = "true"
    "--enable-metrics"                   = "true"
  }
  tags = var.tags
}

# ---------- Glue Catalog Database ------------- #
resource "aws_glue_catalog_database" "mdp_database" {
  name = "movie_database_platform"
}

# ---------- Glue Crawler ------------- #
resource "aws_glue_crawler" "imdb_data_cleansing_glue_crawler" {
  database_name = aws_glue_catalog_database.mdp_database.name
  name          = "imdb_data_cleansing_glue_crawler"
  role          = aws_iam_role.mdp_glue_role.arn

  s3_target {
    path = "s3://${var.app}.${var.label}/cleansed_zone/imdb/"
  }
}

resource "aws_glue_crawler" "movie_lens_data_cleansing_glue_crawler" {
  database_name = aws_glue_catalog_database.mdp_database.name
  name          = "movie_lens_data_cleansing_glue_crawler"
  role          = aws_iam_role.mdp_glue_role.arn

  s3_target {
    path = "s3://${var.app}.${var.label}/cleansed_zone/movie_lens/"
  }
}

resource "aws_glue_crawler" "data_transformation_glue_crawler" {
  database_name = aws_glue_catalog_database.mdp_database.name
  name          = "data_transformation_glue_crawler"
  role          = aws_iam_role.mdp_glue_role.arn

  s3_target {
    path = "s3://${var.app}.${var.label}/refined_zone/imdb/imdb_title_basics_ratings/"
  }
  s3_target {
    path = "s3://${var.app}.${var.label}/refined_zone/movie_lens/movie_lens_movies_ratings/"
  }
}

# ---------- Glue Workflow ------------- #
resource "aws_glue_workflow" "imdb_data_cleansing_glue_workflow" {
  name = "imdb_data_cleansing_glue_workflow"
}

resource "aws_glue_workflow" "movie_lens_data_cleansing_glue_workflow" {
  name = "movie_lens_data_cleansing_glue_workflow"
}

resource "aws_glue_workflow" "data_transformation_glue_workflow" {
  name = "data_transformation_glue_workflow"
}

# ---------- Glue Trigger ------------- #
resource "aws_glue_trigger" "imdb_data_cleansing_glue_trigger" {
  name          = "imdb_data_cleansing_glue_trigger"
  type          = "ON_DEMAND"
  workflow_name = aws_glue_workflow.imdb_data_cleansing_glue_workflow.name

  actions {
    job_name = aws_glue_job.imdb_data_cleansing_glue.name
  }
}

resource "aws_glue_trigger" "movie_lens_data_cleansing_glue_trigger" {
  name          = "movie_lens_data_cleansing_glue_trigger"
  type          = "ON_DEMAND"
  workflow_name = aws_glue_workflow.movie_lens_data_cleansing_glue_workflow.name

  actions {
    job_name = aws_glue_job.movie_lens_data_cleansing_glue.name
  }
}

resource "aws_glue_trigger" "data_transformation_glue_trigger" {
  name          = "data_transformation_glue_trigger"
  type          = "ON_DEMAND"
  workflow_name = aws_glue_workflow.data_transformation_glue_workflow.name

  actions {
    job_name = aws_glue_job.data_transformation_glue.name
  }
}

resource "aws_glue_trigger" "imdb_data_cleansing_glue_crawler_trigger" {
  name          = "imdb_data_cleansing_glue_crawler_trigger"
  type          = "CONDITIONAL"
  workflow_name = aws_glue_workflow.imdb_data_cleansing_glue_workflow.name

  actions {
    crawler_name = aws_glue_crawler.imdb_data_cleansing_glue_crawler.name
  }

  predicate {
    conditions {
      job_name = aws_glue_job.imdb_data_cleansing_glue.name
      state    = "SUCCEEDED"
    }
  }
}

resource "aws_glue_trigger" "movie_lens_data_cleansing_glue_crawler_trigger" {
  name          = "movie_lens_cleansing_glue_crawler_trigger"
  type          = "CONDITIONAL"
  workflow_name = aws_glue_workflow.movie_lens_data_cleansing_glue_workflow.name

  actions {
    crawler_name = aws_glue_crawler.movie_lens_data_cleansing_glue_crawler.name
  }

  predicate {
    conditions {
      job_name = aws_glue_job.movie_lens_data_cleansing_glue.name
      state    = "SUCCEEDED"
    }
  }
}

resource "aws_glue_trigger" "data_transformation_glue_crawler_trigger" {
  name          = "data_transformation_glue_crawler_trigger"
  type          = "CONDITIONAL"
  workflow_name = aws_glue_workflow.data_transformation_glue_workflow.name

  actions {
    crawler_name = aws_glue_crawler.data_transformation_glue_crawler.name
  }

  predicate {
    conditions {
      job_name = aws_glue_job.data_transformation_glue.name
      state    = "SUCCEEDED"
    }
  }
}

# ---------- Dynamodb Table ------------- #
resource "aws_dynamodb_table" "data_analysis_dynamodb_table" {
  name         = "mdp_data_analysis"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "data_title"

  attribute {
    name = "data_title"
    type = "S"
  }

  lifecycle {
    prevent_destroy = true
  }

  tags = var.tags
}

# -------------------------------------------------------------- #
# --------------------------- Web ------------------------------ #
# -------------------------------------------------------------- #

# ---------- Lambda Function ------------- #
resource "aws_lambda_function" "data_service_lambda" {
  function_name    = "data_service_lambda"
  filename         = "./src/aws_lambda/data_service_lambda.zip"
  source_code_hash = data.archive_file.data_service_lambda_file.output_base64sha256
  handler          = "data_service_lambda.handler"
  runtime          = "nodejs14.x"
  timeout          = 300
  memory_size      = 4096
  role             = aws_iam_role.mdp_lambda_role.arn
  tags             = var.tags
}

# ---------- API Gateway ------------- #
resource "aws_api_gateway_rest_api" "mdp_data_service_gateway" {
  name = "mdp_data_service_gateway"
}

# Data API Gateway Start
resource "aws_api_gateway_resource" "mdp_data_service_gateway_resource_data" {
  rest_api_id = aws_api_gateway_rest_api.mdp_data_service_gateway.id
  parent_id   = aws_api_gateway_rest_api.mdp_data_service_gateway.root_resource_id
  path_part   = "data"
}
resource "aws_api_gateway_resource" "mdp_data_service_gateway_resource_dataTitle" {
  rest_api_id = aws_api_gateway_rest_api.mdp_data_service_gateway.id
  parent_id   = aws_api_gateway_resource.mdp_data_service_gateway_resource_data.id
  path_part   = "{dataTitle}"
}

# GET data method
resource "aws_api_gateway_method" "mdp_data_service_gateway_method_data_get" {
  rest_api_id      = aws_api_gateway_rest_api.mdp_data_service_gateway.id
  resource_id      = aws_api_gateway_resource.mdp_data_service_gateway_resource_dataTitle.id
  http_method      = "GET"
  authorization    = "NONE"
  api_key_required = false
}

# GET data integration
resource "aws_api_gateway_integration" "mdp_data_service_gateway_integration_data_get" {
  rest_api_id             = aws_api_gateway_rest_api.mdp_data_service_gateway.id
  resource_id             = aws_api_gateway_resource.mdp_data_service_gateway_resource_dataTitle.id
  http_method             = aws_api_gateway_method.mdp_data_service_gateway_method_data_get.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.data_service_lambda.invoke_arn
}

# Data API Gateway End

# Comment API Gateway Start
resource "aws_api_gateway_resource" "mdp_data_service_gateway_resource_comment" {
  rest_api_id = aws_api_gateway_rest_api.mdp_data_service_gateway.id
  parent_id   = aws_api_gateway_rest_api.mdp_data_service_gateway.root_resource_id
  path_part   = "comment"
}

# GET comment method
resource "aws_api_gateway_resource" "mdp_data_service_gateway_resource_sectionId" {
  rest_api_id = aws_api_gateway_rest_api.mdp_data_service_gateway.id
  parent_id   = aws_api_gateway_resource.mdp_data_service_gateway_resource_comment.id
  path_part   = "{sectionId}"
}
resource "aws_api_gateway_method" "mdp_data_service_gateway_method_comment_section_get" {
  rest_api_id      = aws_api_gateway_rest_api.mdp_data_service_gateway.id
  resource_id      = aws_api_gateway_resource.mdp_data_service_gateway_resource_sectionId.id
  http_method      = "GET"
  authorization    = "NONE"
  api_key_required = false
}

# GET comment integration
resource "aws_api_gateway_integration" "mdp_data_service_gateway_integration_comment_get" {
  rest_api_id             = aws_api_gateway_rest_api.mdp_data_service_gateway.id
  resource_id             = aws_api_gateway_resource.mdp_data_service_gateway_resource_sectionId.id
  http_method             = aws_api_gateway_method.mdp_data_service_gateway_method_comment_section_get.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.data_service_lambda.invoke_arn
}

# POST comment method
resource "aws_api_gateway_method" "mdp_data_service_gateway_method_comment_section_post" {
  rest_api_id      = aws_api_gateway_rest_api.mdp_data_service_gateway.id
  resource_id      = aws_api_gateway_resource.mdp_data_service_gateway_resource_comment.id
  http_method      = "POST"
  authorization    = "NONE"
  api_key_required = false
}
resource "aws_api_gateway_method_response" "mdp_data_service_gateway_method_comment_section_post_response_200" {
  rest_api_id = aws_api_gateway_rest_api.mdp_data_service_gateway.id
  resource_id = aws_api_gateway_resource.mdp_data_service_gateway_resource_comment.id
  http_method = aws_api_gateway_method.mdp_data_service_gateway_method_comment_section_post.http_method
  status_code = "200"
  response_models = {
    "application/json" = "Empty"
  }
  response_parameters = {
    "method.response.header.Access-Control-Allow-Headers" = true,
    "method.response.header.Access-Control-Allow-Methods" = true,
    "method.response.header.Access-Control-Allow-Origin"  = true
  }
  depends_on = [aws_api_gateway_method.mdp_data_service_gateway_method_comment_section_post]
}
# POST comment integration
resource "aws_api_gateway_integration" "mdp_data_service_gateway_integration_comment_post" {
  rest_api_id             = aws_api_gateway_rest_api.mdp_data_service_gateway.id
  resource_id             = aws_api_gateway_resource.mdp_data_service_gateway_resource_comment.id
  http_method             = aws_api_gateway_method.mdp_data_service_gateway_method_comment_section_post.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.data_service_lambda.invoke_arn
}

# OPTIONS comment for cors
resource "aws_api_gateway_method" "mdp_data_service_gateway_method_comment_section_options" {
  rest_api_id   = aws_api_gateway_rest_api.mdp_data_service_gateway.id
  resource_id   = aws_api_gateway_resource.mdp_data_service_gateway_resource_comment.id
  http_method   = "OPTIONS"
  authorization = "NONE"
}
resource "aws_api_gateway_method_response" "mdp_data_service_gateway_method_comment_section_options_200" {
  rest_api_id = aws_api_gateway_rest_api.mdp_data_service_gateway.id
  resource_id = aws_api_gateway_resource.mdp_data_service_gateway_resource_comment.id
  http_method = aws_api_gateway_method.mdp_data_service_gateway_method_comment_section_options.http_method
  status_code = "200"
  response_models = {
    "application/json" = "Empty"
  }
  response_parameters = {
    "method.response.header.Access-Control-Allow-Headers" = true,
    "method.response.header.Access-Control-Allow-Methods" = true,
    "method.response.header.Access-Control-Allow-Origin"  = true
  }
  depends_on = [aws_api_gateway_method.mdp_data_service_gateway_method_comment_section_options]
}
resource "aws_api_gateway_integration" "mdp_data_service_gateway_integration_comment_options" {
  rest_api_id = aws_api_gateway_rest_api.mdp_data_service_gateway.id
  resource_id = aws_api_gateway_resource.mdp_data_service_gateway_resource_comment.id
  http_method = aws_api_gateway_method.mdp_data_service_gateway_method_comment_section_options.http_method
  request_templates = {
    "application/json" = "{\"statusCode\": 200}"
  }
  type        = "MOCK"
  depends_on  = [aws_api_gateway_method.mdp_data_service_gateway_method_comment_section_options]
}
resource "aws_api_gateway_integration_response" "mdp_data_service_gateway_integration_comment_options_response" {
  rest_api_id = aws_api_gateway_rest_api.mdp_data_service_gateway.id
  resource_id = aws_api_gateway_resource.mdp_data_service_gateway_resource_comment.id
  http_method = aws_api_gateway_method.mdp_data_service_gateway_method_comment_section_options.http_method
  status_code = aws_api_gateway_method_response.mdp_data_service_gateway_method_comment_section_options_200.status_code

  response_templates = {
       "application/json" = ""
   } 
  response_parameters = {
    "method.response.header.Access-Control-Allow-Headers" = "'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'"
    "method.response.header.Access-Control-Allow-Methods" = "'OPTIONS'"
    "method.response.header.Access-Control-Allow-Origin"  = "'*'"
  }

  depends_on = [aws_api_gateway_integration.mdp_data_service_gateway_integration_comment_options]
}

# Comment API Gateway End

resource "aws_lambda_permission" "mdp_data_service_lambda_permission" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.data_service_lambda.function_name
  principal     = "apigateway.amazonaws.com"

  source_arn = "${aws_api_gateway_rest_api.mdp_data_service_gateway.execution_arn}/*/*"
}

# ---------- API Gateway Deployment ------------- #

resource "aws_api_gateway_deployment" "mdp_data_service_gateway_deployment" {
  rest_api_id = aws_api_gateway_rest_api.mdp_data_service_gateway.id

  triggers = {
    redeployment = sha1(jsonencode([
      aws_api_gateway_rest_api.mdp_data_service_gateway.body,
      aws_api_gateway_method.mdp_data_service_gateway_method_data_get,
      aws_api_gateway_method.mdp_data_service_gateway_method_comment_section_get,
      aws_api_gateway_method.mdp_data_service_gateway_method_comment_section_post,
      aws_api_gateway_method.mdp_data_service_gateway_method_comment_section_options

    ]))
  }

  depends_on = [
    aws_api_gateway_integration.mdp_data_service_gateway_integration_data_get,
    aws_api_gateway_integration.mdp_data_service_gateway_integration_comment_get,
    aws_api_gateway_integration.mdp_data_service_gateway_integration_comment_post,
    aws_api_gateway_integration.mdp_data_service_gateway_integration_comment_options
  ]
  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_api_gateway_stage" "mdp_data_service_gateway_stage" {
  deployment_id = aws_api_gateway_deployment.mdp_data_service_gateway_deployment.id
  rest_api_id   = aws_api_gateway_rest_api.mdp_data_service_gateway.id
  stage_name    = "v1"
}

output "mdp_data_service_gateway_endpoint_url" {
  value = aws_api_gateway_deployment.mdp_data_service_gateway_deployment.invoke_url
}

# ---------- Dynamodb Table ------------- #
resource "aws_dynamodb_table" "comment_dynamodb_table" {
  name         = "mdp_comment"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "sectionId"
  range_key    = "createDate"

  attribute {
    name = "sectionId"
    type = "S"
  }
  attribute {
    name = "createDate"
    type = "S"
  }

  lifecycle {
    prevent_destroy = true
  }

  tags = var.tags
}


# -------------------------------------------------------------- #
# --------------------------- IAM ------------------------------ #
# -------------------------------------------------------------- #

# ---------- IAM User ------------- #
resource "aws_iam_user" "mdp_user" {
  name = var.user
  path = "/mdp/"
  tags = var.tags
}

# ---------- IAM User Policy ------------- #
resource "aws_iam_user_policy" "mdp_user_policy" {
  name   = "mdp_user_policy"
  user   = aws_iam_user.mdp_user.name
  policy = data.template_file.mdp_user_policy_data.rendered
}

# ---------- IAM Role Policy ------------- #
resource "aws_iam_role_policy" "mdp_lambda_role_policy" {
  name   = "mdp_lambda_role_policy"
  role   = aws_iam_role.mdp_lambda_role.id
  policy = data.template_file.mdp_lambda_policy_data.rendered
}

resource "aws_iam_role_policy" "mdp_glue_role_policy" {
  name   = "mdp_glue_role_policy"
  role   = aws_iam_role.mdp_glue_role.id
  policy = data.template_file.mdp_glue_policy_data.rendered
}

# ---------- IAM Role ------------- #
resource "aws_iam_role" "mdp_lambda_role" {
  name = "mdp_lambda_role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Sid    = ""
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      },
    ]
  })
  tags = var.tags
}

resource "aws_iam_role" "mdp_glue_role" {
  name = "mdp_glue_role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Sid    = ""
        Principal = {
          Service = "glue.amazonaws.com"
        }
      },
    ]
  })
  tags = var.tags
}

# ---------- IAM Access Key ------------- #
resource "aws_iam_access_key" "circleci" {
  user = aws_iam_user.mdp_user.name
}

# ---------- Credentials------------- #
resource "local_file" "circle_credentials" {
  filename = "tmp/circleci_credentials"
  content  = "${aws_iam_access_key.circleci.id}\n${aws_iam_access_key.circleci.secret}"
}

resource "aws_s3_bucket" "main" {
  tags = {
    Name = "main"
  }
  bucket        = "${var.app}.${var.label}"
  force_destroy = true
}
