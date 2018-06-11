##### Introduction

This repository shows a clean way to inspect existing datasamples for errors.

All errors will be written into a separate file while a sanitized version can be used
as a mock for further development.

It checks for custom errors as well as structural errors in the file.

##### Schema creation

Schemas can be created in a very detailed way. See more details here:
https://frictionlessdata.io/specs/table-schema/

##### Disclaimer: Production

As proper tests are missing this should be cautiously used in a production
environment.

It has been proven to be very effective to push all corrupt data rows back to
the owner with the task to fix