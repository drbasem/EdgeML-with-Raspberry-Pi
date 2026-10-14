"""Single source of truth for the course roadmap (standard document and notebook-style notes)."""
PHASES = [
    # key, title, days, colour, what you learn, what you need
    ("P0", "Pi bring-up", (1, 5), "#1F3A5F", "Flash, boot, remote access, Linux basics, camera, Python and Jupyter on the Pi", "Raspberry Pi 4 or 5, microSD, power supply, laptop"),
    ("P1", "ML foundations (Colab)", (6, 13), "#7A4FA0", "Neurons, deep neural networks, CNNs, datasets, metrics, overfitting, Edge Impulse first steps", "Laptop and Google Colab; the Pi is not needed"),
    ("P2", "Fixed-function AI on the Pi", (14, 26), "#C51A4A", "Image classification, object detection (SSD, FOMO), YOLO, counting objects", "Pi camera or USB webcam; Edge Impulse account"),
    ("P3", "Generative AI on the Pi", (27, 38), "#2E8B57", "RNN text, distillation, small language models, RAG, tools, agents, vision-language, audio, GPIO, IoT control", "USB microphone and speaker; breadboard, LEDs, button, sensors"),
    ("P4", "TinyML applications", (39, 42), "#D98E04", "Anomaly detection, keyword spotting, image applications on microcontrollers, responsible AI", "Concepts only: no microcontroller board needed"),
    ("P5", "Capstone + teaching plan", (43, 46), "#0F8B8D", "Your own project, the write-up, and the plan to teach it to students", "Whatever the project needs"),
    ("P6", "Optional: Arduino UNO Q", (47, 56), "#6B7785", "The same ideas on a second hardware platform, after the Pi and ML are mastered", "Arduino UNO Q board (optional)"),
]
# (day, topic, what you do, you will have)
ROWS = {
 "P0": [
  (1, "Meet the Raspberry Pi; flash the microSD; first boot and SSH", "Learn Edge AI and the Pi 4 / Pi 5; write the OS to a card; boot; log in from your laptop", "A Pi you can log into remotely"),
  (2, "Remote access in depth", "Copy files both ways (scp, SFTP); open the desktop remotely; add a second Wi-Fi network; work with more than one Pi", "Files and desktop reachable from your laptop"),
  (3, "The Linux command line", "Navigate, create, edit and delete files; permissions; processes; monitoring with htop", "Confidence in the terminal"),
  (4, "Camera, swap memory and updates", "Connect a Pi camera or USB webcam; capture a photo; adjust swap; update the system", "First photo captured on the Pi"),
  (5, "Python environment and Jupyter on the Pi", "Create a virtual environment; install packages; run Jupyter remotely", "A notebook running on the Pi"),
 ],
 "P1": [
  (6, "Google Colab, Python refresher, what TinyML is", "Run notebooks in the cloud; revise Python and NumPy", "A working Colab setup"),
  (7, "The machine-learning paradigm", "Fit a first model from data and compare it with rule-based code", "Your first trained model"),
  (8, "Neural-network building blocks", "Neurons, layers, activations, loss, gradient descent; build a small network", "A small network trained from scratch"),
  (9, "Regression with a deep neural network", "Predict a number from data; plot predictions", "A regression model"),
  (10, "Classification with a deep neural network", "Predict classes; read a confusion matrix", "A classifier with metrics"),
  (11, "Datasets, splits and metrics", "Train / validation / test splits; accuracy, precision, recall, F1", "Correct model evaluation"),
  (12, "Convolutions; image classification with a CNN", "Filters and pooling; build and train a CNN", "A CNN trained in Colab"),
  (13, "Edge Impulse first project; preventing overfitting", "Train in the browser; dropout and data augmentation", "A model ready to export"),
 ],
 "P2": [
  (14, "TensorFlow Lite and the first inference on the Pi", "Install TensorFlow Lite; run a pre-trained image classifier", "An image classified on the Pi"),
  (15, "Live camera classification; a model trained from scratch", "Classify live camera frames; run a small CIFAR-10 model", "Live classification"),
  (16, "Custom classifier: goal and data collection", "Define the problem; collect and organise your own images", "Your own dataset"),
  (17, "Training in Edge Impulse", "Impulse design, pre-processing, training, accuracy versus speed", "A trained, quantised model"),
  (18, "Test, deploy and run live on the Pi", "Test the model; deploy it; run live inference", "Your own classifier on the Pi"),
  (19, "Object detection fundamentals", "Bounding boxes, labels, post-processing; a pre-trained detector", "Detection on still images"),
  (20, "Detection on a live stream", "Run a detector on the camera stream", "Live object detection"),
  (21, "Custom detection: data and labelling", "Collect and label images for detection", "A labelled detection dataset"),
  (22, "SSD MobileNet in Edge Impulse; deployment", "Train, deploy and post-process an SSD model", "A detector on the Pi"),
  (23, "FOMO: lightweight detection", "Train and deploy a FOMO model", "FOMO running on the Pi"),
  (24, "YOLO with Ultralytics on the Pi", "Run YOLO; export to an efficient format", "YOLO inference on the Pi"),
  (25, "YOLO: custom training and deployment", "Train YOLO on your data; deploy it", "A custom YOLO model"),
  (26, "Counting objects; Phase 2 mini-project", "Build a counting pipeline; complete a small project", "A counting system"),
 ],
 "P3": [
  (27, "Text generation with an RNN", "Tokens, embeddings, training a small text generator", "A tiny text generator"),
  (28, "Knowledge distillation", "Teach a small student model from a larger teacher", "A distilled model"),
  (29, "Small language models: first model with Ollama", "Install Ollama; choose a model that fits your board (Pi 5 recommended); chat", "A language model answering on the Pi"),
  (30, "Ollama with Python", "Use the Python library; build a chat script", "A Python chat program"),
  (31, "Function (tool) calling", "Let the model call Python functions", "A tool-using model"),
  (32, "Retrieval-augmented generation (RAG)", "Build a vector store; retrieve context for answers", "Question answering over your documents"),
  (33, "Agents with small models", "Design a tool set; build a simple agent loop", "A working agent"),
  (34, "Vision-language models", "Run a vision-language model (Florence-2) for captioning and detection", "Image captioning on the Pi"),
  (35, "Audio and vision AI pipeline", "Microphone to speech-to-text to language model to speech", "Speech in, answer out"),
  (36, "GPIO and physical computing: LEDs and buttons", "Wire a circuit; control it from Python", "An LED and button under code control"),
  (37, "Sensors and notebooks", "Read temperature, humidity and pressure sensors; log data", "Sensor data logged"),
  (38, "Small language models for IoT control", "Let a language model switch real hardware", "Language-model-driven hardware"),
 ],
 "P4": [
  (39, "Anomaly detection and K-means", "Cluster data; detect anomalies", "An anomaly detector (concept + notebook)"),
  (40, "Keyword spotting (concepts)", "Audio features and the keyword-spotting pipeline", "The pipeline understood"),
  (41, "Image applications on microcontrollers; data collection", "Person detection concept; ways to collect data", "A data-collection plan"),
  (42, "Responsible AI; going further with Edge AI", "Fairness, privacy, safety, lifecycle", "A responsible-deployment checklist"),
 ],
 "P5": [
  (43, "Choose and plan the project", "Define the goal, data, model and hardware", "A one-page project plan"),
  (44, "Build", "Implement the system", "A working prototype"),
  (45, "Build, test and measure", "Measure accuracy, speed and resource use honestly", "Measured results"),
  (46, "Present, write up, plan how to teach it", "Report, demo, lesson plan", "Report + teaching plan"),
 ],
 "P6": [
  (47, "UNO Q: foundations and setup", "Understand the board; set it up", "Board working"),
  (50, "Language models on the UNO Q; benchmarking; Python", "Run and benchmark models; script them", "Model running"),
  (53, "Multimodal and agentic AI on the UNO Q", "Combine vision, language and tools", "An agent running"),
  (55, "Physical AI: the two processors working together", "Connect a language model to hardware through the bridge", "A language model driving hardware"),
 ],
}
MILESTONES = [(5, "Pi ready"), (13, "first CNN"), (18, "own classifier on the Pi"), (26, "object counting"), (32, "RAG"), (38, "language model drives GPIO"), (46, "capstone")]
PREP = [
    ("1", "Raspberry Pi 4 or 5, microSD (32 GB or more), the matching USB-C power supply, card reader, Wi-Fi details", "Everything in Phase 0"),
    ("4", "Pi camera module (check the camera cable: it differs between Pi 4 and Pi 5) or a USB webcam", "Camera test and all vision projects"),
    ("6", "Google account", "Colab, ML foundations"),
    ("13", "Edge Impulse account (check the current free tier)", "Training in Phase 2"),
    ("27", "Internet on the Pi for model downloads; enough free space on the card", "Ollama and models"),
    ("35", "USB microphone and speaker", "Audio pipeline"),
    ("36", "Breadboard, jumper wires, LEDs with resistors, push button, DHT temperature sensor, BMP280 pressure sensor (confirm the exact parts in the lessons before buying)", "GPIO and sensors"),
    ("47+", "Arduino UNO Q (optional)", "Alternative hardware track"),
]
REFERENCES = [
    "Rovai, M. (2025). __Edge AI Engineering: Hands-on with the Raspberry Pi__. Open textbook for the course IESTI05, Federal University of Itajubá (UNIFEI), Brazil. Version of 23 October 2025. Online edition: https://mjrovai.github.io/EdgeML_Made_Ease_ebook/",
    "Rovai, M. (2026). __IESTI05 - Edge AI: Edge Machine Learning Systems Engineering__. Course slides, notebooks and video lectures (second semester 2026), UNIFEI, Brazil. Course videos listed by the author: Class 1 (course introduction) https://youtu.be/QAb3MFHwe78 ; Class 2 (Introduction to Linux) https://youtu.be/QkIHILtl0h4 ; Class 3 (Raspberry Pi setup walkthrough) https://youtu.be/YtjsM36LzVE (lectures in Portuguese).",
    "Rovai, M. (2026). __IESTI01 - TinyML: Machine Learning for Embedding Devices__. Course materials (first semester 2026), UNIFEI, Brazil. https://github.com/Mjrovai/UNIFEI-IESTI01-TinyML",
    "Rovai, M. __TinyML4D__: lectures, books, papers and tutorials for embedded machine-learning education. https://github.com/Mjrovai/TinyML4D",
    "Raspberry Pi Imager: download page and software. https://www.raspberrypi.com/software/",
    "Raspberry Pi Ltd. __Raspberry Pi documentation__ (hardware specifications of the Raspberry Pi 4 and Raspberry Pi 5, operating system, remote access). https://www.raspberrypi.com/documentation/",
]
