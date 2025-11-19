### MVP Guide: Training Arm Grip and Navigation for PuzzArm (Focus on One Piece)


The PuzzArm Minimum Viable Product (MVP) focuses on training a single xArm1S robotic arm on a Jetson Nano to autonomously pick and place one puzzle piece (e.g., number "3") into its corresponding slot, handling arbitrary rotations.

Using a pre-trained YOLO classifier for piece detection, the MVP uses imitation learning, inspired by NVIDIA's road-following approach, to **train two models**: one for gripping (adjusting from a "ready-to-grab" state above a fixed piece position) and another for navigation (moving from a "ready-to-move" lifted state to the piece's slot). 
Three pre-programmed states—**home**, **ready-to-grab**, and **ready-to-move**—simplify kinematics. 

For each model, **20-30** manual demonstrations (images) are collected by positioning the arm by hand, capturing top-down camera images and joint states (via serial feedback added to image file name). 
The grip model learns to align the end-effector based on piece rotation, using end-effector voltage feedback to confirm success. The navigation model then guides the arm to the slot. 

Training uses PyTorch on Jetson, with TensorRT export for real-time inference (~50ms). The MVP, achievable in 4-6 hours, targets 85%+ success rate for one piece, forming the foundation for scaling to full puzzle automation.


This MVP targets:
- **Grip Training**: 20-30 demos → Model to adjust from "ready-to-grab" to grip based on piece rotation.
- **Navigation Training**: 20-30 demos → Model to move from "ready-to-move" to slot placement.
- **Total Effort**: 4-6 hours (2 for data, 1-2 for training, 1 for testing).

We'll modify NVIDIA's `road_following.ipynb` (from [NVIDIA-AI-IOT/jetbot](https://github.com/NVIDIA-AI-IOT/jetbot)) to output 6D joint deltas instead of steering/throttle. Train with PyTorch, export to TensorRT for ~50ms inference on Nano.
We will use  https://github.com/ccourson/Hiwonder-xArm1S to control the arm.

#### Step 1: Setup Pre-Programmed States
Hardcode these as joint position arrays in your serial package. Use your Python wrapper to send them (e.g., `set_positions([j1,j2,...])`).

**You will need to adapt the provided code as it is untested and should be considered sudo code !**

```python
# In your xArm serial module (adapt from docs)
import xarm

# arm is the first xArm detected which is connected to USB
arm = xarm.Controller('USB')
print('Battery voltage in volts:', arm.getBatteryVoltage()

def set_state(state_name):
    states = {
        'home': [90, 90, 90, 90, 90, 90],  # Central safe pos (calibrate once)
        'ready_to_grab': [45, 120, 90, 90, 135, 90],  # Above fixed piece spot, gripper open/down
        'ready_to_move': [45, 120, 135, 90, 90, 90]   # Lifted 5-10cm, gripper closed
    }
    if state_name in states:
        ser.write_positions(states[state_name])  # Your method: send via TTL serial
        print(f"Set to {state_name}")
    else:
        print("Invalid state")

def get_joints():
    return ser.read_positions()  # Returns list of 6 floats + voltages

def check_grip_success(threshold=0.5):  # Via end-effector feedback
    positions, voltages = ser.read_positions_and_voltages()
    # Simple: Grip success if voltage spike on gripper servo (j6?)
    return any(v > threshold for v in voltages[-1:])  # Tune threshold
```

- **Calibrate**: Manually jog arm (via python ) to positions, record joints with `get_joints()`, hardcode. Test: `set_state('home')`.

#### Step 2: Data Collection for Grip Training
- **Process**: 
  1. Set to `ready_to_grab`.
  2. Manually nudge arm over piece (by hand—gently push links; no teleop needed).
  3. At good grip alignment (visually: end-effector over peg, aligned to rotation), capture:
     - Cropped image (from YOLO bbox, top-down view).
     - Current joints (`get_joints()`).
     - Label: "grip_action" (model learns to output small deltas from ready_pos).
  4. Repeat 20-30x, varying rotations (place piece rotated 0-360° in fixed spot).
- **Modified Notebook**: Fork `road_following.ipynb` (download from [jetbot repo](https://github.com/NVIDIA-AI-IOT/jetbot/blob/master/examples/road_following.ipynb)). Changes:
  - Input: Cropped image (224x224) + current joints (6D vector).
  - Output: 6D joint deltas (e.g., [-2, 1, 0, 0, -1, 0] for fine tweaks).
  - Data: Save as `dataset_grip/` with images + JSON (joints, deltas= target - current).

Run this cell-by-cell in Jupyter on Jetson:

```python
# Cell 1: Imports & Serial Setup (run once)
import ipywidgets.widgets as widgets
from IPython.display import display
import cv2
from jetbot import Camera  # Or your CSI cam
import torch
import json
import os
from serial import *  # Your xArm serial

# Init cam & serial
camera = Camera.instance()
ser = Serial('/dev/ttyUSB0', 115200)  # Your init
dataset_dir = 'dataset_grip'
os.makedirs(dataset_dir, exist_ok=True)
counter = 0

# Buttons for capture
button_capture = widgets.Button(description="Capture Grip Demo")
output = widgets.Output()

def capture_grip(change):
    global counter
    # Get image & crop (assume YOLO bbox ready; for MVP, crop full view to piece area)
    image = camera.value
    cropped = image[100:200, 150:250]  # Tune to piece region; resize to 224x224
    cv2.imwrite(f'{dataset_dir}/image_{counter}.jpg', cv2.cvtColor(cropped, cv2.COLOR_RGB2BGR))
    
    # Get current joints
    current_joints = get_joints()  # [j1..j6]
    target_joints = current_joints  # For grip, delta=0 at perfect; but record as-is for learning
    
    data = {'joints': current_joints, 'deltas': [0]*6}  # Deltas from ready_to_grab
    with open(f'{dataset_dir}/joints_{counter}.json', 'w') as f:
        json.dump(data, f)
    
    counter += 1
    print(f"Captured {counter}: Joints {current_joints}")
    output.clear_output()
    with output:
        display(image)  # Show full image

button_capture.on_click(capture_grip)
display(button_capture, output)

# Usage: Set arm to ready_to_grab, position manually, click Capture. Do 20-30x.
```

- **Tips**: Place piece in fixed spot (e.g., 10cm left of base). Rotate it each time. After collection: `ls dataset_grip/` should have ~25 image/JSON pairs.

#### Step 3: Train Grip Model (TensorRT Export)
- Adapt `train_resnet_regression.ipynb` from JetBot repo (or dusty-nv/jetson-inference  for TRT examples).
- Model: CNN (ResNet18) on image → FC → 6D deltas. Input concat: flattened image + current joints.
- Train: ~10-20 min on Nano
-  **Train using Colab** ~1-2 mins.

```python
# Cell: Training (run after data collection)
from torch.utils.data import Dataset, DataLoader
import torch.nn as nn
import torch.optim as optim
from torchvision import transforms, models
import glob

class GripDataset(Dataset):
    def __init__(self, dir_path):
        self.images = sorted(glob.glob(f'{dir_path}/*.jpg'))
        self.transforms = transforms.Compose([
            transforms.ToPILImage(),
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ])
    
    def __len__(self): return len(self.images)
    
    def __getitem__(self, idx):
        img_path = self.images[idx]
        img = cv2.imread(img_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = self.transforms(img)
        
        json_path = img_path.replace('.jpg', '.json')
        with open(json_path, 'r') as f:
            data = json.load(f)
        joints = torch.tensor(data['joints'], dtype=torch.float32)
        deltas = torch.tensor(data['deltas'], dtype=torch.float32)  # Target adjustments
        
        return img, torch.cat([img.flatten(), joints]), deltas  # Flattened for simple FC

dataset = GripDataset('dataset_grip')
dataloader = DataLoader(dataset, batch_size=8, shuffle=True)

# ArmModel: Simple ResNet for regression
model = models.resnet18(pretrained=True)
model.fc = nn.Sequential(
    nn.Linear(512 + 6, 128),  # +6 for joints
    nn.ReLU(),
    nn.Linear(128, 6)  # 6D deltas
)
model = model.cuda()
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=1e-3)

# Train loop
for epoch in range(50):
    for imgs, states, targets in dataloader:
        preds = model(states.cuda())
        loss = criterion(preds, targets.cuda())
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
    if epoch % 10 == 0:
        print(f'Epoch {epoch}, Loss: {loss.item():.4f}')

torch.save(model.state_dict(), 'grip_model.pth')

# Export to ONNX for TensorRT (use trtexec or jetson-inference tools)
torch.onnx.export(model, torch.randn(1, 512+6).cuda(), 'grip_model.onnx')
# Then: trtexec --onnx=grip_model.onnx --saveEngine=grip_model.trt
```

- **Test Grip**: Load model, from `ready_to_grab`: Detect piece rotation with YOLO, crop image, infer deltas, apply incrementally (e.g., 5 steps of small moves). Check `check_grip_success()`—if yes, `set_state('ready_to_move')`.

#### Step 4: Data Collection & Training for Slot Navigation
- **Process**: Mirror grip, but:
  1. Grip piece (using new model), lift to `ready_to_move`.
  2. Manually guide arm over target slot.
  3. Capture: Cropped image (piece over slot) + joints.
  4. 20-30x, varying slot approaches.
- **Notebook**: Duplicate grip one, rename `dataset_nav/`. Deltas: From ready_move to placement pose.
- **Training**: Same code, output 6D for navigation (longer sequences if needed via LSTM).

#### Step 5: MVP Integration & Testing
- **Full Loop** (in a ROS2 node or Jupyter):
  ```python
  # Pseudo: Autonomous Grip + Nav
  set_state('ready_to_grab')
  image = camera.value  # Run YOLO: detect piece, get bbox/rotation
  cropped = crop_to_bbox(image, bbox)  # Your func
  state = torch.cat([torch.flatten(transforms.ToTensor()(cropped)), torch.tensor(get_joints())])
  with torch.no_grad():
      deltas = model(state.unsqueeze(0).cuda())[0].cpu().numpy()
  # Apply deltas incrementally: for d in deltas: adjust_joints(d * 0.1)  # Smooth
  if check_grip_success():
      set_state('ready_to_move')
      # Repeat for nav arm_model: infer to slot
  ```
- **Test**: 10 runs on one piece/slot. Success: Grip + place without collision. Debug: Log joints/images.
- **Next**: Scale to all 10 pieces (reuse data), add MoveIt2 fallback.

This gets your MVP gripping and placing one piece reliably. Fork the JetBot repo, add these cells—test on hardware. If serial errors, check Hiwonder repo . 