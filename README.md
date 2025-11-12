# Deadline-Blender

Modified Blender plugin for AWS Deadline
* Allows using GPU rendering if available
* Python script to detect compatible GPUs on workers
* Extends Blender plugin to offer Blender versions
* Extends Blender submission to set OCIO environment variable to the Deadline job
* adds Blender CLI argument --python-use-system-env for compatibility with AYON pipeline

This thread from Deadline Forum is the primary source of the modifications.

https://forums.thinkboxsoftware.com/t/forcing-blender-to-use-gpu/28570/28