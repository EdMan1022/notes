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

https://github.com/openshift/jenkins-client-plugin
The above link contains the repository for the openshift java plugin,
which ITPaaS uses to interact with the openshift clusters in the pipelines


# Pipeline Coding Structure

Ideally, we should be able to write code for one of the pipeline scripts
and run a unit test suite.
If the tests pass, we should be 100% certain that the pipeline will at
least execute on the managed jenkins instance when it is committed to `master`.

The problem with this is that it is difficult to exactly duplicate the
structure of Jenkins.
We can use the jenkins-unit test package,
but already we've run into issues where the unit tests pass
but the pipeline fails to compile or execute on Jenkins.

## OOP
To prevent the pipelines from becoming horrifically complicated once we start
introducing more complicated logic, we would like to be able to abstract some
of the concepts into separate classes.

In order to do this with jenkins,
it looks like we need to use a shared library.
We could also just define the classes in the same files that the pipeline
runs in, but that seems suboptimal.

### Update
Actually, we can use a jenkins `load` global variable, which can load arbitrary
groovy scripts dynamically. ~~We can maybe use this to import classes to the
pipeline script itself.~~ This doens't work for our use case,
because classes can't be loaded dynamically in this fashion.
Instead ITPaaS allowed us to add a shared library to our project folder.
The repo at https://gitlab.corp.redhat.com/mkt-ops-de/mktg-ops-pipeline-utils.git
contains the shared library code. We import it into our pipeline scripts using
```java
@Library('MktgOpsPipelineUtils@pipeline-class')
import com.redhat.mktg_ops.pipeline.*
```


### NonCPS decorator
In order to use a method in a classes constructor, that method needs to use the
`@NonCPS` decorator from the cloudbees package.