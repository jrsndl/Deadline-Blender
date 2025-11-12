import os
import bpy

# Check for GPU pinning from Deadline or custom env var
gpu_env = os.environ.get("BLENDER_GPUDEVICES")

if gpu_env:
    pinned_ids = [int(i) for i in gpu_env.split(",") if i.strip().isdigit()]
    print(f"GPU pinning detected: enabling GPU(s) {pinned_ids}")
else:
    pinned_ids = None
    print("No GPU pinning detected - enabling all available GPUs")

# Configure Cycles preferences
prefs = bpy.context.preferences.addons["cycles"].preferences
prefs.get_devices()

# Inspect devices for vendor and capabilities
device_names = [d.name.lower() for d in prefs.devices]
print(f"Available GPU devices: {device_names}")

# Detect GPU type and choose best backend
if any("radeon" in name for name in device_names):
    # ignore amd in device names, that would often switch to CPUs
    prefs.compute_device_type = "HIP"
    print("Detected AMD GPU - using HIP backend")
elif any("nvidia" in name or "geforce" in name for name in device_names):
    # prefer CUDA for Nvidias instead of OPTIX
    prefs.compute_device_type = "CUDA"
    print("Detected NVIDIA GPU - using CUDA backend")
elif any("rtx" in name or "optix" in name for name in device_names):
    prefs.compute_device_type = "OPTIX"
    print("Detected NVIDIA RTX GPU - using OptiX backend")
else:
    # Fallback
    prefs.compute_device_type = "CUDA"
    print("No specific GPU detected - defaulting to CUDA")

# Enable GPUs based on pinning, or fallback to all
for i, device in enumerate(prefs.devices):
    device.use = (pinned_ids is None or i in pinned_ids)

# Use GPU for rendering
scene = bpy.context.scene
scene.cycles.device = "GPU"
