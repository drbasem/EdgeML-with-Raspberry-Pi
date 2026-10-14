"""Single source of truth for the study roadmap (used by the DOCX and the sketch-note builders).
Book page numbers are PDF pages of 'Edge-AI-Engineering book.pdf' (printed page + 1)."""
PHASES = [
    # key, title, days(from,to), colour, one-liner, hardware
    ("P0", "Pi bring-up", (1, 5), "#1F3A5F", "Flash, boot, SSH, Linux basics, camera, Python + Jupyter on the Pi", "Pi 4, microSD, power, laptop"),
    ("P1", "ML foundations (Colab)", (6, 13), "#7A4FA0", "Neurons, DNNs, CNNs, datasets, metrics, overfitting, Edge Impulse intro", "Laptop + Google Colab, no Pi needed"),
    ("P2", "Fixed-function AI on the Pi", (14, 26), "#C51A4A", "Image classification, object detection (SSD, FOMO), YOLO, counting objects", "Camera (Pi camera or USB webcam), Edge Impulse account"),
    ("P3", "Generative AI on the Pi", (27, 38), "#2E8B57", "RNN text, distillation, small language models (Ollama), RAG, agents, vision-language, audio, GPIO, IoT control", "USB mic + speaker, breadboard, LEDs, button, sensors"),
    ("P4", "TinyML applications", (39, 42), "#D98E04", "Anomaly detection, keyword spotting, image apps on microcontrollers, responsible AI", "Concepts only (no microcontroller board needed)"),
    ("P5", "Capstone + teaching plan", (43, 46), "#0F8B8D", "Your own project, write-up, and the plan to teach it to students", "Whatever the project needs"),
    ("P6", "Optional: Arduino UNO Q", (47, 56), "#6B7785", "The same ideas on a different board (after you master the Pi and ML)", "Arduino UNO Q (not owned yet)"),
]
# (day, topic, source, book pdf pages, result)
ROWS = {
 "P0": [
  (1, "Meet the Pi 4, flash the microSD, first SSH", "IESTI05 C3", "20-21, 25-27, 29-39", "Pi answers over SSH"),
  (2, "Remote access: file transfer, remote desktop, two Pis and two networks", "IESTI05 C3", "38-44, 56-61", "Copy files both ways; desktop opened remotely"),
  (3, "Linux command line", "IESTI05 C2 (slides + linux_intro.pdf)", "-", "Navigate, edit, install, htop"),
  (4, "Camera, swap memory, updates", "IESTI05 C3 slide 10", "43-55, 62-64", "First photo taken on the Pi"),
  (5, "Python virtual environment + Jupyter on the Pi", "IESTI05 C4", "65-75", "Notebook running on the Pi"),
 ],
 "P1": [
  (6, "Colab and Python review; what is TinyML", "IESTI01 C2-C4b", "-", "Colab notebook running"),
  (7, "The machine-learning paradigm", "IESTI01 C5", "-", "First model fitted"),
  (8, "Neural-network building blocks", "IESTI01 C6", "-", "A small network in TensorFlow"),
  (9, "Regression with a DNN", "IESTI01 C7", "-", "Regression model + plot"),
  (10, "Classification with a DNN", "IESTI01 C8", "-", "Classifier + confusion matrix"),
  (11, "Datasets, splits and metrics", "IESTI01 C9", "-", "Train/validation/test done right"),
  (12, "Convolutions; image classification with a CNN", "IESTI01 C10-C11", "-", "CNN trained in Colab"),
  (13, "Edge Impulse intro (Cifar-10); preventing overfitting", "IESTI01 C12-C13", "-", "Model trained in Edge Impulse"),
 ],
 "P2": [
  (14, "TensorFlow Lite + MobileNetV2 inference", "IESTI05 C5", "75-86", "Classify an image on the Pi"),
  (15, "Live camera classification; a model trained from zero", "IESTI05 C5", "86-93", "Live classification from the camera"),
  (16, "Custom classifier: goal and data collection", "IESTI05 C6", "94-102", "Your own dataset"),
  (17, "Train in Edge Impulse", "IESTI05 C7", "103-111", "Trained, quantised model"),
  (18, "Test, deploy and run live on the Pi", "IESTI05 C7", "112-130", "First custom classifier on the Pi"),
  (19, "Object detection fundamentals", "IESTI05 C8", "131-145", "Pre-trained detector on an image"),
  (20, "Pre-trained detectors and live stream", "IESTI05 C8", "146-153", "Live detection"),
  (21, "Custom detection: data and labeling", "IESTI05 C9", "154-168", "Labeled dataset"),
  (22, "SSD MobileNet in Edge Impulse; deploy", "IESTI05 C10", "169-187", "Detector on the Pi"),
  (23, "FOMO (lightweight detection)", "IESTI05 C10", "188-202", "FOMO model on the Pi"),
  (24, "YOLO with Ultralytics on the Pi", "IESTI05 C11", "203-219", "YOLO inference, NCNN export"),
  (25, "YOLO: custom training and deployment", "IESTI05 C12", "220-237", "Custom YOLO model"),
  (26, "Counting objects (bees) + Part 1 mini-project", "IESTI05 C13-C14, Part 1 assignment", "238-264", "Counting pipeline"),
 ],
 "P3": [
  (27, "Text generation with an RNN (VerneBot)", "IESTI05 C15", "265-289", "Tiny text generator"),
  (28, "Knowledge distillation in practice", "book chapter", "290-308", "Distilled model"),
  (29, "Small language models: first model with Ollama", "IESTI05 C16-C17", "309-335", "SLM answering on the Pi"),
  (30, "Ollama with Python", "IESTI05 C18", "336-360", "Python chat script"),
  (31, "Function (tool) calling", "IESTI05 C19", "361-375", "SLM calling a Python function"),
  (32, "Retrieval-augmented generation (RAG)", "IESTI05 C20", "376-388", "Question answering over your documents"),
  (33, "Agents with small models", "IESTI05 C20a", "560 onward", "Simple tool-using agent"),
  (34, "Vision-language models (Florence-2)", "book chapter", "389-433", "Image captioning on the Pi"),
  (35, "Audio and vision AI pipeline", "book chapter", "434-458", "Speech in, answer out"),
  (36, "GPIO and physical computing: LEDs, buttons", "IESTI05 C21", "459-485", "LED and button under code control"),
  (37, "Sensors and notebooks", "IESTI05 C21", "486-510", "Sensor readings logged"),
  (38, "SLMs for IoT control", "IESTI05 C22", "511-557", "A language model switching hardware"),
 ],
 "P4": [
  (39, "Anomaly detection and K-means", "IESTI01 C21-C22", "-", "Anomaly detector (concept + notebook)"),
  (40, "Keyword spotting (concepts)", "IESTI01 C23-C24", "-", "KWS pipeline understood"),
  (41, "Image apps on microcontrollers; data collection", "IESTI01 C25-C27", "-", "Person detection concept"),
  (42, "Responsible AI; going further with Edge AI", "IESTI01 C28-C29", "-", "Checklist for responsible deployment"),
 ],
 "P5": [
  (43, "Choose and plan the project", "IESTI05 Part 1 / Part 2 assignments", "-", "One-page project plan"),
  (44, "Build", "-", "-", "Working prototype"),
  (45, "Build, test and measure", "-", "-", "Measured results (honest ones)"),
  (46, "Present, write up, and plan how to teach it", "-", "-", "Report + teaching plan"),
 ],
 "P6": [
  (47, "UNO Q: foundations and setup", "IESTI05 UNO Q Ch0-Ch1", "-", "Board working"),
  (50, "SLMs on the UNO Q; benchmarking; Python", "IESTI05 UNO Q Ch2 (C19-C21)", "-", "Model running"),
  (53, "Multimodal and agentic AI", "IESTI05 UNO Q Ch3, Ch5", "-", "Agent running"),
  (55, "Physical AI: Bridge between the two processors", "IESTI05 UNO Q Ch4", "-", "Language model driving hardware"),
 ],
}
MILESTONES = [(5, "Pi ready"), (13, "first CNN"), (18, "own classifier on the Pi"), (26, "YOLO counting"), (32, "RAG"), (38, "SLM drives GPIO"), (46, "capstone")]
