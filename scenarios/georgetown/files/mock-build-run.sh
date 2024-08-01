#!/usr/env/bin bash

MOUNT_POINT="/tmp/ephemeral-build"
EXAMPLE_BUILD_ARTIFACT="example-build-artifact.txt"
MAX_BUILD_ARTIFACT_SIZE=10M

# Create the example build file
touch $MOUNT_POINT/$EXAMPLE_BUILD_ARTIFACT

# Use fallocate to allocate the maximum size of the file
fallocate -l "$MAX_SIZE" "$MOUNT_POINT/$EXAMPLE_BUILD_ARTIFACT"

trap
