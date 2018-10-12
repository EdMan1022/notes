# Managed Platform Pipeline Notes

## What does the pipeline need to do?

- Build application images from source code
- Validate the application images
- Deploy the application images to the various Managed Platform OpenShift
clusters

## What are the open questions around the requirements for this software?

- How do the source code branches and the different clusters relate?
    - I think that the deployment to the `dev` cluster should use `/develop`
    - `/master` obviously should be used for deployment to the `prod` cluster
    - If we want to deploy different branches to different clusters,
    we'll need to have differential builds and different image tags to go
    along with that.

- What is the deal with the pipeline helper image validation function?
    - Current implementation fails with errors that don't line up with
    current documentation from ITPaaS

- Do we want to do anything fancy when it comes to merging code into master
from staging? For example merging into `/staging` could trigger a pipeline that:
    1. Builds image in OpenShift
    1. Checks out image
    1. Runs validation on the image
    1. Runs custom image tests on image
    1. Boots up container and runs unit tests using image
    1. Finishes a deployment on the qa cluster
    1. Opens and merges a merge request from `/staging` into `/master`



## More in depth description of the pipeline workflow

When we merge a feature branch (or push code directly) into develop,
it should kick off a build and deployment of that code into the dev OpenShift
cluster.

When we merge code into 