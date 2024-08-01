#!/usr/bin/bash

BUILD_MOUNT_POINT="/tmp/ephemeral-build"

# Check if the build mount point exists
function check_build_mount_point {
  if [ ! -d $BUILD_MOUNT_POINT ]; then
    echo -b "NO"
    exit 1
  fi
}

# Function to check if both example-build-artifact.txt and
# secondary-artifact.txt exist in the build mount point
# BOTH files need to exist concurrently
function check_build_artifacts {
  BUILD_FILES=(
    "example-build-artifact.txt"
    "secondary-artifact.txt"
  )
  for file in "${BUILD_FILES[@]}"; do
    if [ ! -f "$BUILD_MOUNT_POINT/$file" ]; then
      echo -b "NO"
      exit 1
    else
      echo -b "OK"
      exit 0
    fi
  done
}

# Check if one or both functions executed successfull
check_build_mount_point
check_build_artifacts
