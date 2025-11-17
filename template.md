# Applying CRISP-DM Methodology to the PuzzArm Project

**Document Purpose:**  
This document applies the Cross-Industry Standard Process for Data Mining (CRISP-DM) methodology to the PuzzArm project, structuring the AI/ML components (e.g., image identification for puzzle pieces, pose estimation, and imitation learning for arm control) across its six phases. CRISP-DM provides an iterative, non-linear framework for ML projects, emphasising business alignment and continuous refinement. This application serves as a checkpoint for the clustered AI course, mapping to ICTAII501 (designing AI solutions) and ICTAII502 (implementing ML models).

Use this as Assessment template, filling in project-specific details based on your work (e.g., Roboflow training/Arm training ).

**Project Recap:** PuzzArm is an AI-powered robotic system using Jetson Nano and xArm1S to solve a number puzzle (0-9 pieces), with dual-arm teleop (or similar method) for data collection. The ML focus is on vision-based detection, classification, and motion policies.

**Iteration Note:** CRISP-DM is cyclical—after Deployment, loop back to Business Understanding for refinements (e.g., adding new puzzles).



---

## Phase 1: Business Understanding
**Objective:** Define the problem, goals, and success criteria in business terms. Assess resources and risks.  

- **Business Problem:** Automate puzzle solving to create an educational robotics demo for expo demonstrations  and marketing events.
- **Data Mining Goals:** Develop models for piece detection (~70% accuracy), pose estimation (handling rotations), and arm control (50% pick-place success).  
- **Project Plan:** Timeline (4-6 weeks); resources (Jetson Nano, xArm1S, Roboflow). 
- **Risks:**
	- Flaws with the hardware, causing it to not work as it is supposed to.
	- Object Detection model cannot identify numbers clearly enough or with high enough accuracy.
 	- The CNN (Convolutional Neural Network) model for the arm cannot move the arm in the right direction.
  	- Python version incompatability between the Jetson Nano and xArm1S.


- ***Student Input:*** [Describe how you  addressed the  business need 100-200 words]
	- I addressed the business need to create an automated process of detecting puzzle pieces, picking them up, and placing them by creating two separate models for both number detection and to move the xArm1S's servos to attempt to pick up the puzzle piece. By defining clear goals for how the models should perform, such as > 70% accuracy for number detection and > 50% success rate in picking up the puzzle pieces, I contributed to the business need by making a strong start for the entire puzzle solving process. I ended up ruling out the Jetson Nano as a method of data collection and vision to see the puzzle pieces in order to create an educational robotics demo, as within the timeframe getting past the incompatibility of Python version between hardware components was inviable. By using Roboflow to augment the images, the small dataset was able to become less biased to make it more robust, while also proving to be a useful platform for training the object detection model as well. I used Google Colab to train the CNN (Convolutional Neural Network) model to be able to get the xArm1S to attempt to pick up the puzzle pieces regardless of where they are, as long as they are in range.

   *Mapping to Units:** ICTAII501 PC 1.1-1.2 (confirm work brief via CRISP-DM business phase).*

---

## Phase 2: Data Understanding
**Objective:** Collect initial data, explore it, and identify quality issues.  

- **Initial Data Collection:** 100-200 images of puzzle pieces/slots from top-down camera (via Jetson CSI), plus teleop videos (ROS2 bags) for joint states. Sources: Manual photos, Roboflow public datasets for augmentation.  
- **Data Description:** Structure (images: RGB, 224x224; labels: 0-9 classes; joints: 6D floats). Volume: ~5k samples post-augmentation.  
- **Data Exploration:** Use pandas/matplotlib for histograms (e.g., class balance: 10% per digit); identify issues (e.g., lighting bias via correlation plots).  
- **Student Input:** [From Part 1: Summarise your Roboflow dataset stats, e.g., "50 images/class; explored via Hello AI tools, found 20% rotation variance." Include a sample plot code/output.]  
  ```python
  # Example exploration code (adapt from your work)
  import matplotlib.pyplot as plt
  # Load data and plot class distribution
  plt.bar(classes, counts)
  plt.show()
  ```  
*Mapping to Units ICTAII502 PC 1.1-1.6 (analyse requirements and data attributes using CRISP-DM data phase).*  

---

## Phase 3: Data Preparation
**Objective:** Clean, transform, and construct the final dataset for modeling.  

- **Data Cleaning:** Remove duplicates/blurry images (OpenCV thresholding); handle missing labels via Roboflow auto-annotation.  
- **Feature Engineering:** Augment for rotations (0-360° via Albumentations); normalize images (0-1 scale); engineer joint deltas from teleop recordings.  
- **Final Dataset:** Train (70%): 3.5k samples; Val (20%): 1k; Test (10%): 500. Format: PyTorch DataLoader for Jetson training.  
- **Student Input:** [Detail your prep from thumbs classifier/Roboflow, e.g., "Applied flips and brightness augments to address orientation issues." Include before/after metrics, e.g., variance reduction.]  
- **Mapping to Units:** ICTAII502 PC 2.1-2.4 (set parameters, engineer features per CRISP-DM prep phase).  

---

## Phase 4: Modeling
**Objective:** Select and apply ML techniques, tuning parameters.  

- **Model Selection:** - *Student input* - Name, use etc
- **Techniques Applied:** - *Student input* - eg, Supervised training 
- **Model Building:**  - *Student input* - eg, Train detection first (output: boxes/classes); then policy (input: cropped image + joints; output: 6D deltas). Export to TensorRT.  

*Mapping to Units ICTAII502 PC 3.1-3.5 (arrange validation, refine parameters via CRISP-DM modeling).*  

---

## Phase 5: Evaluation
**Objective:** Assess model performance against business goals; review process.  

- **Model Assessment:** - *Student input* - eg, Metrics: Detection,  Policy success rate, pick-place trials,  Use confusion matrix for classes.
- **Business Criteria Check:** Does it enable full puzzle solve <5 min?  - *Student input* 
- **Process Review:** Data quality issues? (e.g., rotations fixed via augments). Next iteration: - *Student input* 

*Mapping to Units ICTAII502 PC 5.1-5.6 (finalize evaluations, document metrics per CRISP-DM eval phase); ICTAII501 PC 3 (document design outcomes).*  

---

## Phase 6: Deployment
**Objective:** Plan rollout, monitoring, and maintenance.  

- **Deployment Plan:** *Student input* - eg, Deploy on Jetson.  
- **Monitoring:** *Student input* - eg, Log pickup  time (<100ms); retrain quarterly with new demos.  
- **Business Reporting:** *Student input*  - Demo video; report ROI (e.g. What it can do for the time invested). Maintenance: Version models in GitHub/Gitlab]  
- 
*Mapping to Units ICTAII501 PC 2 (design for deployment); ICTAII502 PC 4.1-4.5 (finalize test procedures).*  

---

## Overall Reflection and Iteration Plan
 **Next Steps:** *Student input* - What do you need to do next to achieve the project.  200 -400 words + code samples if required.

