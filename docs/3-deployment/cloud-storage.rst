.. _cloud-storage:

Configuring cloud storage
=========================

.. index:: storage, S3, Cloud Storage, Azure Storage

If you generated the project with a cloud provider, static files and user uploads are served from that provider's object storage rather than from your application server. This is independent of the platform you deploy to, so follow this page alongside the deployment guide of your choice.

How the template uses your bucket
---------------------------------

A single bucket (or container, on Azure) holds both kinds of files, under two prefixes:

- ``static/``: the output of ``collectstatic``, meant to be **publicly readable**.
- ``media/``: user uploads, served through ``MEDIA_URL``.

The storages do **not** set a per-object ACL on upload. Uploaded objects simply inherit whatever access rules the bucket has, so making static files reachable is a one-off bucket configuration step, described below for each provider. This matches the current default of all three providers, which is to disable per-object ACLs in favour of bucket-wide policies.

.. warning:: The instructions below deliberately expose only the ``static/`` prefix. Granting public read on the whole bucket also exposes ``media/``, and since the template sets unsigned URLs for media, every user upload would then be readable by anyone able to guess its URL. See `Keeping media private`_ if uploads in your project are not meant to be public.

Amazon S3
---------

New buckets have ACLs disabled (*Object Ownership: bucket owner enforced*) and all four **Block Public Access** settings enabled. You need to relax the two policy-related ones, then attach a bucket policy scoped to the ``static/`` prefix.

.. code-block:: bash

    BUCKET=your-bucket-name

    # Outside of us-east-1, add:
    #   --create-bucket-configuration LocationConstraint=$AWS_REGION
    aws s3api create-bucket --bucket $BUCKET --region us-east-1

    # Allow public *policies*, while still blocking public ACLs
    aws s3api put-public-access-block --bucket $BUCKET \
        --public-access-block-configuration \
        "BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=false,RestrictPublicBuckets=false"

    cat > /tmp/static-policy.json <<EOF
    {
      "Version": "2012-10-17",
      "Statement": [
        {
          "Sid": "PublicReadForStaticFiles",
          "Effect": "Allow",
          "Principal": "*",
          "Action": "s3:GetObject",
          "Resource": "arn:aws:s3:::$BUCKET/static/*"
        }
      ]
    }
    EOF

    aws s3api put-bucket-policy --bucket $BUCKET --policy file:///tmp/static-policy.json

The same can be done from the console, under the bucket's **Permissions** tab: first edit **Block public access**, then **Bucket policy**. S3 will label the bucket as *Publicly accessible* afterwards, which is expected.

The policy applies to objects already in the bucket, so there is no need to re-run ``collectstatic``.

.. note:: Requests for a key that does not exist return ``403 Forbidden`` rather than ``404 Not Found``, because anonymous callers lack ``s3:ListBucket``. If static files still 403 after this, check the object is really there with ``aws s3api head-object --bucket $BUCKET --key static/css/project.css``.

Google Cloud Storage
--------------------

New buckets default to *uniform bucket-level access*, which disables the per-object ACL API. Grant public read through IAM instead. Cloud Storage IAM cannot target a prefix directly, so use a conditional binding to keep the grant limited to ``static/``:

.. code-block:: bash

    BUCKET=your-bucket-name

    gcloud storage buckets add-iam-policy-binding gs://$BUCKET \
        --member=allUsers \
        --role=roles/storage.objectViewer \
        --condition="title=public-static-files,expression=resource.name.startsWith('projects/_/buckets/$BUCKET/objects/static/')"

If you would rather not rely on a conditional binding, use a dedicated bucket for static files and grant ``roles/storage.objectViewer`` to ``allUsers`` on that bucket without a condition.

If the binding is rejected, `public access prevention`_ is enforced on the bucket or inherited from an organization policy, and you will need to either lift it or serve static files from a bucket where it is not enforced.

.. _public access prevention: https://cloud.google.com/storage/docs/public-access-prevention

Azure Storage
-------------

Azure has no per-blob ACL to set; anonymous access is granted at the container level, and recent storage accounts disallow it account-wide by default:

.. code-block:: bash

    ACCOUNT=your-account-name
    CONTAINER=your-container-name

    az storage account update --name $ACCOUNT --allow-blob-public-access true

    az storage container set-permission --name $CONTAINER \
        --account-name $ACCOUNT --public-access blob

.. warning:: Because ``--public-access`` is set on the whole container, and the template stores both ``static/`` and ``media/`` in the same container, this also exposes user uploads. Use a second container or a `stored access policy`_ if that is not acceptable.

.. _stored access policy: https://learn.microsoft.com/en-us/rest/api/storageservices/define-stored-access-policy

.. _cloud-storage-cors:

Allowing cross-origin requests
------------------------------

Public reads are enough for most files, but a few kinds of asset are fetched by the browser in *CORS mode*, and those also need the bucket to answer with an ``Access-Control-Allow-Origin`` header. A bucket has no CORS configuration until you add one, so it sends no such header, the browser discards the response, and the asset silently fails to apply.

You need a CORS configuration if your project serves any of:

- **ES module scripts**, which is how ``{% vite_asset %}`` renders bundles if you picked Vite as your frontend pipeline. The page renders, but no JavaScript runs and the console reports ``CORS Missing Allowed Origin``.
- **Web fonts** referenced from ``url()`` inside a stylesheet, whichever frontend pipeline you picked.
- Anything you load with an explicit ``crossorigin`` attribute or a `Subresource Integrity`_ hash.

Substitute your own bucket name and the origin your site is served from:

.. code-block:: bash

    BUCKET=your-bucket-name
    ORIGIN=https://example.com

    cat > /tmp/cors.json <<EOF
    {
      "CORSRules": [
        {
          "AllowedMethods": ["GET", "HEAD"],
          "AllowedOrigins": ["$ORIGIN"],
          "AllowedHeaders": ["*"],
          "MaxAgeSeconds": 3600
        }
      ]
    }
    EOF

    aws s3api put-bucket-cors --bucket $BUCKET --cors-configuration file:///tmp/cors.json

On Google Cloud Storage:

.. code-block:: bash

    cat > /tmp/cors.json <<EOF
    [
      {
        "origin": ["$ORIGIN"],
        "method": ["GET", "HEAD"],
        "responseHeader": ["Content-Type"],
        "maxAgeSeconds": 3600
      }
    ]
    EOF

    gcloud storage buckets update gs://$BUCKET --cors-file=/tmp/cors.json

On Azure Storage, CORS is set per storage account rather than per container:

.. code-block:: bash

    az storage cors add --services b --methods GET HEAD \
        --origins $ORIGIN --allowed-headers '*' --max-age 3600 \
        --account-name your-account-name

To confirm a real asset now answers correctly, ask for it with an ``Origin`` header::

    curl -sSI -H "Origin: $ORIGIN" https://$BUCKET.s3.amazonaws.com/static/<some-asset> \
        | grep -i access-control-allow-origin

.. _Subresource Integrity: https://developer.mozilla.org/en-US/docs/Web/Security/Subresource_Integrity

Keeping media private
---------------------

Making ``static/`` public is expected: those files ship with your application. User uploads are a different matter, and the template's defaults assume they are public.

On AWS, ``AWS_QUERYSTRING_AUTH = False`` in ``config/settings/production.py`` makes ``media`` URLs unsigned and permanent. If uploads in your project are sensitive, remove that setting so django-storages returns time-limited signed URLs, and do not extend any public bucket policy to the ``media/`` prefix. The equivalent settings are ``GS_QUERYSTRING_AUTH`` for Google Cloud Storage and Azure's SAS-token support.

Serving through a CDN
---------------------

Putting a CDN in front of the bucket lets you keep it entirely private, since the CDN authenticates to the origin on your behalf: CloudFront with an `Origin Access Control`_ on AWS, or Cloud CDN backed by a bucket backend on GCP. Once the distribution is set up, point ``DJANGO_AWS_S3_CUSTOM_DOMAIN`` at it so generated URLs use the CDN domain.

.. _Origin Access Control: https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/private-content-restricting-access-to-s3.html
