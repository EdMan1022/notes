If there is a glitched deployment-config in openshift already,
then apply could throw errors without you realizing it.

Also, its possible that you could have a deployment that works the first time
you call `oc apply` but then stops working for any subsequent calls of `oc apply`.
The server tries to check the currently running config,
and then fails because it hits a type error.