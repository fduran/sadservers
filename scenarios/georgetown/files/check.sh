#!/usr/bin/bash

BUILD_MOUNT_POINT="/tmp/ephemeral-build"

# Check if the build mount point exists
function check_build_mount_point {
    if [ ! -d $BUILD_MOUNT_POINT ]; then
        echo "Build mount point $BUILD_MOUNT_POINT does not exist"
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
        echo "Build artifact $file does not exist"
        exit 1
    fi
  done
}

# Check if the build mount point exists
check_build_mount_point

# Infinitely loop to check if the build artifacts exist
while true; do
    check_build_artifacts
    sleep 5
done

