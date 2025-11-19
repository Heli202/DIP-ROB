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
	- My Roboflow dataset originated from 2745 images from a [different dataset](https://universe.roboflow.com/srr-yrcal-anadolu-lisesi/numbers-xnrog), along with 96 images of the puzzle pieces for feature engineering of our specific use case. Each image has 3 outputs for augmentation including rotating clockwise, anti clockwise and upside down, grayscale of 21% of the images, and blur up to 1.7 px. This produced 8155 total images, where an accuracy for the test images reached was between 60 and 95%.
 - As my entire dataset was on Roboflow, I was not able to get a sample plot code/output, however below is some metrics of my dataset:
<img width="1500" height="202" alt="Screenshot 2025-11-19 095200" src="https://github.com/user-attachments/assets/cbec7b1c-5c86-462c-b8ce-0cd845f3463f" />
<img width="800" height="800" alt="Screenshot 2025-11-19 094816" src="https://github.com/user-attachments/assets/4fffde3d-08db-44bd-9479-b1feb51051d3" />
<img width="800" height="700" alt="Screenshot 2025-11-19 094837" src="https://github.com/user-attachments/assets/329e67bb-5f78-4ef1-9131-6828b8d6566c" />

*Mapping to Units ICTAII502 PC 1.1-1.6 (analyse requirements and data attributes using CRISP-DM data phase).*  

---

## Phase 3: Data Preparation
**Objective:** Clean, transform, and construct the final dataset for modeling.  

- **Data Cleaning:** Remove duplicates/blurry images (OpenCV thresholding); handle missing labels via Roboflow auto-annotation.  
- **Feature Engineering:** Augment for rotations (0-360° via Albumentations); normalize images (0-1 scale); engineer joint deltas from teleop recordings.  
- **Final Dataset:** Train (70%): 3.5k samples; Val (20%): 1k; Test (10%): 500. Format: PyTorch DataLoader for Jetson training.  
- **Student Input:** As I was using Roboflow, applying augmentation to the images in my dataset was very easy, and this consisted of rotating the images clockwise, anti clockwise, upside down, grayscaling 21% of images and blurring up to 1.7 px. This allowed the dataset to become less biased in the quality of images, so that when using a lower quality webcam, the model has a better time recognising different numbers. This helped my model generalise and made it more robust both in training and in the final product.
- **Mapping to Units:** ICTAII502 PC 2.1-2.4 (set parameters, engineer features per CRISP-DM prep phase).  

---

## Phase 4: Modeling
**Objective:** Select and apply ML techniques, tuning parameters.  

- **Model Selection:** - Name: 'numbers 1' with ID: 'numbers-xnrog-d6zw6/1', with the model type: YOLOv11 Object Detection (Accurate) 
- **Techniques Applied:**
	- Supervised training, with labelled data.
 	- Augmentation:
  		- Rotation: clockwise, anti clockwise, upside down
    	- Grayscale on 21% of images.
     	- Blurring up to 1.7 px.
  	- Manual early stopping once loss stagnated to avoid overfitting.
  	- Data splitting for training, validation and test subsets.  
- **Model Building:**  - I trained the object detection model first, then trained the policy model by saving images of where the puzzle piece is in relation to the robot arm, while the file names were the positions of each of the servos at that time. I then used inference through the use of API to access the model.

*Mapping to Units ICTAII502 PC 3.1-3.5 (arrange validation, refine parameters via CRISP-DM modeling).*  

---

## Phase 5: Evaluation
**Objective:** Assess model performance against business goals; review process.  

- **Model Assessment:** - During training my object detection model was a lot better than the reality when using a webcame. During training, when it actually detected a number, the accuracy was quite high at around 80%+, however when using the webcam in a different angle than my training data, it was much lower, and there were plenty of times where it detected nothing at all. It successfully detected a number around 40-70% of the time depending on the specific angle of the number and its position. A mistake I made during gathering my training data was not setting up the same conditions as what it ended up being. If I gathered training data of the same angle and incorported that into my feature engineering of my large dataset, I would have likely seen much better results.

As for my policy model, it was much lower, and is very unlikely to be able to pick up the number. It did at least attempt a different way depending on where you put the number, however even with a dataset being composed of 114 images, the data was very biased and I found that a lot of the images had the same servo angles as the file names or very similar. Another issue is that when placing the number far away it is extremely unlikely to even tell there is a number there at all, and will continue to print out messages saying it cant find the number. With my first attempts at creating a model, there was no normalisation of the images for the servo angles, so with numbers between 0-1000 to try and predict, it performed very poorly. After changing the servo angles to be normalised, a large improvement was made, in that it got a little closer, and the metrics of the model were quite a lot better, such as a consistently lowering loss over time. In the end however it is unable to pick up a puzzle piece which is largely due to both biased data and not enough data with the policy model. The object detection model is good enough however, but it is bottle necked in the process of completing the puzzle from the policy model. A revision of the training of the policy model would also be advised, as there is potential for changes in the hyperparameters that may give a better result and particularly with the optimizer, I was unable to research enough about the different types, and ended up using the first one that worked. More augmentation could also be used to create more varied data with a limited dataset, however care should be taken to make sure that the augmentation does not provide data that is unrealistic to the actual conditions.

- **Business Criteria Check:** Does it enable full puzzle solve <5 min?  - No it does not. With less biased data and more varied data, and more time given to refine hyperparameters, a newly trained model will be likely to do a full puzzle solve.
- **Process Review:** Data quality issues? (e.g., rotations fixed via augments). Next iteration: - Data quality was a lot higher for 

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

