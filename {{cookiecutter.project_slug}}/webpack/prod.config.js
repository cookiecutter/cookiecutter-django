const { merge } = require('webpack-merge');
const commonConfig = require('./common.config');

// This variable should mirror the one from config/settings/production.py
{%- if cookiecutter.use_whitenoise == 'n' %}
{%- if cookiecutter.cloud_provider == 'AWS' %}
const s3BucketName = process.env.DJANGO_AWS_STORAGE_BUCKET_NAME;
const awsS3Domain = process.env.DJANGO_AWS_S3_CUSTOM_DOMAIN
  ? process.env.DJANGO_AWS_S3_CUSTOM_DOMAIN
  : `${s3BucketName}.s3.amazonaws.com`;
const staticUrl = `https://${awsS3Domain}/static/`;
{%- elif cookiecutter.cloud_provider == 'GCP' %}
const staticUrl = `https://storage.googleapis.com/${process.env.DJANGO_GCP_STORAGE_BUCKET_NAME}/static/`;
{%- elif cookiecutter.cloud_provider == 'Azure' %}
const staticUrl = `https://${process.env.DJANGO_AZURE_ACCOUNT_NAME}.blob.core.windows.net/static/`;
{%- endif %}
{%- else %}
const staticUrl = '/static/';
{%- endif %}

module.exports = merge(commonConfig, {
  mode: 'production',
  devtool: 'source-map',
  bail: true,
  output: {
    publicPath: `${staticUrl}webpack_bundles/`,
  },
});
