import os, sys, glob
sys.path.insert(0, os.path.dirname(__file__))
from docx_lib import *
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
FIG = f"{ROOT}/day01/figures"; BOOK = f"{ROOT}/_assets/figures_adapted"; SHOTS = f"{ROOT}/my_screenshots/day01"
OUT = f"{ROOT}/day01"

def user_shot(prefix):
    for ext in ("png", "jpg", "jpeg"):
        m = glob.glob(f"{SHOTS}/{prefix}*.{ext}")
        if m: return m[0]
    return None

def make_filmstrip():
    fr = [Image.open(f"{FIG}/d1_anim_f{i}.png").convert("RGB").resize((800, 450), Image.LANCZOS) for i in range(1, 6)]
    g = 14; W = 3 * 800 + 4 * g; H = 2 * 450 + 3 * g
    sheet = Image.new("RGB", (W, H), "white")
    for i, im in enumerate(fr):
        x = g + (i % 3) * (800 + g); y = g + (i // 3) * (450 + g); sheet.paste(im, (x, y))
        ImageDraw.Draw(sheet).rectangle([x - 1, y - 1, x + 800, y + 450], outline="#C9D1D9", width=2)
    x = g + 2 * (800 + g); y = g + (450 + g)
    d = ImageDraw.Draw(sheet); d.rounded_rectangle([x, y, x + 800, y + 450], radius=18, fill="#E8EEF6", outline="#1F3A5F", width=3)
    fb = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 44); fn = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 30)
    d.polygon([(x + 330, y + 90), (x + 330, y + 210), (x + 440, y + 150)], fill="#C51A4A")
    d.text((x + 400, y + 255), "Play the animation", font=fb, fill="#1F3A5F", anchor="mm")
    d.text((x + 400, y + 320), "animations/", font=fn, fill="#1F2933", anchor="mm")
    d.text((x + 400, y + 360), "Day01_flash_boot_ssh.mp4", font=fn, fill="#1F2933", anchor="mm")
    sheet.save(f"{FIG}/d1_filmstrip.png", dpi=(300, 300)); return f"{FIG}/d1_filmstrip.png"

def slot(d, prefix, placeholder, width, caption):
    p = user_shot(prefix)
    d.figure(p or f"{FIG}/{placeholder}", width, caption + ("" if p else "  (capture slot - add your own screenshot)"))

REFERENCES = [
    "Rovai, M. (2025). __Edge AI Engineering: Hands-on with the Raspberry Pi__. Open textbook for the course IESTI05, Federal University of Itajubá (UNIFEI), Brazil. Version of 23 October 2025. Online edition: https://mjrovai.github.io/EdgeML_Made_Ease_ebook/",
    "Rovai, M. (2026). __IESTI05 - Edge AI: Edge Machine Learning Systems Engineering__. Course slides, notebooks and video lectures (second semester 2026), UNIFEI, Brazil. Course videos listed by the author: Class 1 (course introduction) https://youtu.be/QAb3MFHwe78 ; Class 2 (Introduction to Linux) https://youtu.be/QkIHILtl0h4 ; Class 3 (Raspberry Pi setup walkthrough) https://youtu.be/YtjsM36LzVE (lectures in Portuguese).",
    "Rovai, M. (2026). __IESTI01 - TinyML: Machine Learning for Embedding Devices__. Course materials (first semester 2026), UNIFEI, Brazil. https://github.com/Mjrovai/UNIFEI-IESTI01-TinyML",
    "Rovai, M. __TinyML4D__: lectures, books, papers and tutorials for embedded machine-learning education. https://github.com/Mjrovai/TinyML4D",
    "Raspberry Pi Imager: download page and software. https://www.raspberrypi.com/software/",
    "Raspberry Pi Ltd. __Raspberry Pi documentation__ (hardware specifications of the Raspberry Pi 4 and Raspberry Pi 5, operating system, remote access). https://www.raspberrypi.com/documentation/",
]
FIGURE_CREDIT = ("The screenshots of Raspberry Pi Imager and of the first SSH login, and the labelled photograph of the Raspberry Pi 5, are adapted from reference [1]. "
                 "All other figures and the animation were created for this course.")

def build():
    d = Doc("Edge AI with the Raspberry Pi  |  Course material  |  Day 01",
            "Edge AI with the Raspberry Pi  -  Day 01  -  Prof. Basem M. ElHalawany")
    d.title_block("Edge AI with the Raspberry Pi  -  Day 01", "Meet the Raspberry Pi\nand Bring It to Life",
                  "Understand Edge AI and the Raspberry Pi, prepare the operating system, boot for the first time, and log in from your laptop.")
    d.meta_table([
        ("Time needed", "2 hours, in six parts (A to F). Take longer if you want: every part is explained from first principles."),
        ("Boards covered", "**Raspberry Pi 4 Model B** and **Raspberry Pi 5**. Every step works on both boards; where they differ, the text says **Pi 4** or **Pi 5**."),
        ("What you need", "A Raspberry Pi 4 or 5, a microSD card (32 GB or more), the matching USB-C power supply, a card reader, and a laptop with Wi-Fi (Windows steps are given; Mac and Linux differences are noted)."),
        ("No prior knowledge", "None is assumed: not of Linux, networking or machine learning. Everything needed is explained here."),
        ("Outcome", "A Raspberry Pi that boots, joins your Wi-Fi network, and answers you in a terminal window on your laptop, and you understand every step you took."),
        ("Next", "Day 02: remote access in depth (file transfer, remote desktop, working with more than one network)."),
        ("Course author", "Prof. Basem M. ElHalawany. Sources and acknowledgments are listed at the end."),
    ])
    d.h2("By the end of today you will be able to")
    d.checks([
        "Explain what Edge AI is, why it matters, and how it differs from cloud AI.",
        "Distinguish fixed-function (reactive) AI from generative (proactive) AI.",
        "Name the main parts of a Raspberry Pi 4 and a Raspberry Pi 5 and say what each is for.",
        "Explain what an operating system does, and why a Raspberry Pi needs a microSD card.",
        "Understand the basics of a network: router, IP address, host name and the `.local` name.",
        "Write Raspberry Pi OS onto a microSD card with your own host name, user, Wi-Fi and SSH settings.",
        "Boot the Pi, read its LEDs, and know what happens during the first boot.",
        "Log in from Windows over SSH, run your first commands, update the system and shut down safely.",
    ])
    d.h2("Your 2-hour plan")
    d.figure(f"{FIG}/d1_roadmap.png", 16.2, "The two hours at a glance. Part D (the microSD card) is the longest; do not rush it.")
    d.callout("note", "Before you start (10 minutes the evening before)", [
        "- Download **Raspberry Pi Imager** for your laptop from https://www.raspberrypi.com/software/ and install it.",
        "- Write down your **Wi-Fi network name and password**, and decide which network the Pi will live on.",
        "- Back up anything important on the microSD card: **Imager erases the whole card.**",
    ])

    # =========================================================== PART A
    d.h1("Part A  -  The big picture (20 min)")
    d.h2("A1. What is Edge AI?")
    d.p("Most of the AI you meet every day, such as a chatbot, photo tagging or voice dictation, runs in a **data centre**. Your data travels over the network to powerful servers, the model computes the answer, and the answer travels back. This is **cloud AI**.")
    d.p("**Edge AI** turns this around: the AI algorithm runs **locally, on the device that sits next to the data it analyses**: a camera, a robot, a factory sensor, a phone, or a Raspberry Pi. The 'edge' is simply the edge of the network, the place where the data is born. Running AI there makes systems more **responsive, more private and more efficient**.")
    d.figure(f"{FIG}/d1_cloud_edge.png", 15.6, "Cloud AI sends the data to a distant data centre and waits for the answer. Edge AI computes the answer on the device next to the sensor.")
    d.h2("A2. Training and inference: the two lives of a model")
    d.p("A machine-learning **model** is a program whose behaviour is learned from examples instead of being written by hand. It has two life stages:")
    d.table(["Stage", "What happens", "Resources needed", "Where we do it in this course"], [
        ["**Training**", "The model is shown many examples and adjusts its internal numbers until its answers are good.", "Large: lots of data, a fast processor, minutes to days.", "On a laptop or in the cloud (for example Google Colab, Edge Impulse Studio)."],
        ["**Inference**", "The trained model is given new data (a photo, a sound, a question) and produces an answer.", "Small: milliseconds to seconds.", "**On the Raspberry Pi**: this is the 'edge' part."],
    ], [2.4, 6.0, 4.0, 4.8], size=9)
    d.p("In most projects you will train (or download) a model once, shrink it to fit a small device, and then run inference on the Pi again and again.")
    d.h2("A3. Five reasons Edge AI matters")
    d.table(["Advantage", "What it means in practice"], [
        ["**Low latency**", "The answer arrives in milliseconds because there is no network round trip. A robot can react to an obstacle now, not after a server replies."],
        ["**Privacy**", "Sensitive images, audio or measurements stay on the device instead of travelling to a remote server."],
        ["**Network independence**", "The system keeps working with no Internet: in a tunnel, a field, a ship or a factory."],
        ["**Lower bandwidth**", "Send only the useful result (a few bytes) instead of streaming raw video."],
        ["**Energy efficiency**", "Small, optimised models on small hardware use far less power than a round trip to a data centre."],
    ], [4.2, CONTENT_W - 4.2])
    d.callout("note", "The price of the edge", [
        "An edge device has a small processor, limited memory and a limited power budget. Models therefore have to be **small and optimised** (for example by using lower numerical precision). Choosing and shrinking models to fit the hardware is a recurring theme of this course."])
    d.h2("A4. Two families of AI")
    d.p("AI applications fall into two broad families. The course is organised around them.")
    d.table(["", "Fixed-function AI (reactive)", "Generative AI (proactive)"], [
        ["**Idea**", "Analyses a specific input according to predetermined patterns and gives a consistent output.", "Creates new content, understands context, keeps a dialogue going and adapts to new situations."],
        ["**Behaviour**", "Responds to specific triggers; follows defined patterns; excels at structured tasks such as classification, detection and recognition; works within its boundaries.", "Generates text, descriptions or solutions; interprets nuance; maintains context across turns; copes with situations beyond its explicit training."],
        ["**Core focus**", "Data analysis, assessment, automation.", "Content creation, anticipation, dialogue."],
        ["**Examples**", "Fraud detection, spam filters, image recognition, counting objects in a camera view.", "Chat assistants, image generators, predictive maintenance, smart assistants."],
        ["**Typical use**", "Banking, medical diagnostics, security systems.", "Content creation, customer support, design, automation."],
        ["**In this course**", "Phase 2: image classification, object detection, counting.", "Phase 3: small language models, vision-language models, agents."],
    ], [2.8, 7.2, 7.2], size=9)
    d.callout("note", "Rule of thumb", ["Choose **fixed-function** AI when you need efficiency, predictability and low resource use for a well-defined task. Choose **generative** AI when the task calls for creativity, personalisation or anticipation. Both gain the same benefits from running at the edge: lower latency, privacy, reliability without a network, and efficient use of resources."])
    d.h2("A5. What the whole course covers")
    d.p("Day by day, the course takes you from an empty microSD card to working Edge AI systems:")
    d.bullets([
        "**Essential setup:** prepare the Raspberry Pi for Edge AI work (this week).",
        "**Machine-learning foundations:** neurons, networks, datasets, metrics, overfitting, using Google Colab.",
        "**Computer vision:** image classification, object detection and object counting.",
        "**Small language models (SLMs):** run and optimise them on the Pi, then add retrieval (RAG), tools (function calling) and agents.",
        "**Vision-language models:** multimodal AI that understands images and text together.",
        "**Physical computing:** connect AI to sensors and actuators through the GPIO pins.",
        "**Advanced optimisation, a capstone project, and how to teach it.** (The full day-by-day roadmap is a separate document.)",
    ], size=10)
    d.callout("tip", "Checkpoint", ["Close the document and explain, in two sentences, the difference between cloud AI and Edge AI. Then name three advantages of the edge. If you can, move on."])

    # =========================================================== PART B
    d.h1("Part B  -  The Raspberry Pi (25 min)")
    d.h2("B1. A computer on a single board")
    d.p("A **single-board computer (SBC)** is a complete computer built on one circuit board: processor, memory, network and video connectors, and pins for connecting electronics. The Raspberry Pi is the best-known SBC. Its main chip is a **system on a chip (SoC)**, which combines the processor cores, graphics and many controllers in one package.")
    d.p("A Pi has **no built-in disk**. The operating system and your files live on a **microSD card** that you insert into a slot. Switch the card and you switch the computer's whole 'personality'; this is also why we can keep several different cards for different projects.")
    d.h2("B2. Why the Raspberry Pi suits Edge AI")
    d.table(["Feature", "What it gives you"], [
        ["**Computational power**", "Multi-core ARM processors and, on newer models, up to 8 GB of RAM: enough to run optimised AI models."],
        ["**GPIO header**", "A 40-pin header of General-Purpose Input/Output pins. Each pin can read a signal (a button, a sensor) or drive one (an LED, a relay). It connects software to the physical world."],
        ["**Connectivity**", "Wi-Fi, Bluetooth, Gigabit Ethernet and several USB ports for cameras, microphones and storage."],
        ["**Low-level interfaces**", "I2C, SPI and UART: standard serial buses used by sensors, displays and other chips."],
        ["**Soft real-time use**", "With proper configuration, a Pi can run control and signal-processing tasks that tolerate small timing variations."],
        ["**Power efficiency**", "Low consumption suits battery-powered and always-on designs."],
        ["**Full Linux + community**", "A complete operating system with standard tools, a huge community, plenty of tutorials and low cost."],
    ], [4.0, CONTENT_W - 4.0], size=9.5)
    d.h2("B3. What engineers build with a Pi")
    d.table(["Area", "Examples"], [
        ["Embedded systems design", "Prototyping devices before they are turned into products."],
        ["IoT and networked devices", "Sensors that publish data with MQTT, CoAP or HTTP(S)."],
        ["Control systems", "Feedback loops, PID controllers, driving actuators."],
        ["Computer vision and AI", "Image processing with OpenCV, machine learning with TensorFlow Lite."],
        ["Data acquisition", "Collecting sensor data, real-time analysis, data loggers."],
        ["Robotics", "Robot controllers, motion planning, motor drivers."],
        ["Signal processing", "Real-time filtering and DSP experiments."],
        ["Network security", "VPNs, firewalls, security testing labs."],
    ], [5.2, CONTENT_W - 5.2], size=9.5)
    d.h2("B4. The Raspberry Pi models you will meet")
    d.table(["", "Pi Zero 2 W", "Pi 4 Model B", "Pi 5"], [
        ["**CPU**", "1 GHz, 4 cores, Cortex-A53 (64-bit)", "1.5 GHz, 4 cores, Cortex-A72", "2.4 GHz, 4 cores, Cortex-A76"],
        ["**RAM**", "512 MB", "up to 8 GB", "2, 4 or 8 GB (a 16 GB model was added later)"],
        ["**Wi-Fi / Bluetooth**", "2.4 GHz only, Bluetooth 4.2", "dual-band 802.11ac, Bluetooth 5.0", "dual-band 802.11ac, Bluetooth 5.0"],
        ["**Main ports**", "mini-HDMI, micro-USB OTG, camera connector", "2 x micro-HDMI, 2 x USB 3 + 2 x USB 2, Ethernet, camera + display", "2 x micro-HDMI, 2 x USB 3 + 2 x USB 2, Ethernet, 2 camera/display connectors, PCIe"],
        ["**Power**", "5 V / 2.5 A via micro-USB; about 0.6 W idle", "5 V / 3 A via USB-C", "5 V / 5 A (27 W) via USB-C; about 3 to 3.5 W idle"],
        ["**Best for**", "Tiny, battery-powered embedded projects and small models", "All-round: the vision projects of this course (language models: only the very smallest)", "Edge computing, vision and the largest language models; 8 GB recommended for AI"],
    ], [2.6, 4.2, 5.2, 5.2], size=9)
    d.callout("note", "Which board do I use?", [
        "This course works on a **Pi 4 or a Pi 5**, and the boards differ most in **Phase 3 (language models)**. The vision phase (Phases 0, 2, 4, 5) runs well on both. A **Pi 4 does not run language models well**: only very small models, and slowly. For Phase 3 the right board is a **Pi 5 (8 GB recommended)**. With only a Pi 4 you still do the whole course, and treat Phase 3 as a guided demonstration with the smallest models (or run it on a Pi 5 in the lab)."])
    d.h2("B5. Anatomy of the Raspberry Pi 4 and Raspberry Pi 5")
    d.figure(f"{FIG}/d1_pi4_anatomy.png", 16.0, "Raspberry Pi 4 Model B (schematic; port positions are simplified: compare with your real board).")
    d.figure(f"{FIG}/d1_pi5_anatomy.png", 16.0, "Raspberry Pi 5 (schematic; positions simplified). Note the power button, the PCIe connector, the fan connector and the two small camera/display connectors.")
    d.figure(f"{BOOK}/pi5_diagram.png", 12.4, "Raspberry Pi 5: labelled photograph.")
    d.table(["Part", "What it does", "Pi 4", "Pi 5"], [
        ["**CPU (SoC)**", "Runs the operating system and all your code; does the neural-network arithmetic.", "Broadcom BCM2711: 4 x Cortex-A72, 1.5 GHz", "Broadcom BCM2712: 4 x Cortex-A76, 2.4 GHz"],
        ["**RAM**", "Working memory. A model must fit in RAM to run.", "up to 8 GB", "2, 4, 8 GB"],
        ["**microSD slot**", "Holds the card with the operating system and your files (on the underside).", "yes", "yes"],
        ["**40-pin GPIO header**", "Pins to read sensors, buttons and drive LEDs or relays.", "yes", "yes (same pin layout)"],
        ["**USB ports**", "Keyboards, webcams, microphones, storage. Blue ports are USB 3.", "2 x USB 3 + 2 x USB 2", "2 x USB 3 + 2 x USB 2"],
        ["**Ethernet**", "Wired network connection.", "Gigabit", "Gigabit"],
        ["**Wi-Fi + Bluetooth**", "Built-in wireless.", "dual-band, BT 5.0", "dual-band, BT 5.0"],
        ["**micro-HDMI x 2**", "Connect one or two monitors. Use the port nearest the USB-C connector first.", "yes", "yes"],
        ["**Camera / display**", "Ribbon-cable connectors for the Pi camera and touch displays.", "1 camera (CSI) + 1 display (DSI), 15-pin", "2 connectors that serve either, smaller 22-pin"],
        ["**USB-C power input**", "The only power connection.", "5 V / 3 A", "5 V / 5 A (27 W)"],
        ["**Power button**", "Switch the board on and off.", "none", "yes"],
        ["**PCIe connector**", "Fast expansion (storage, accelerators). Not needed in this course.", "none", "PCIe 2.0 x1"],
        ["**Fan connector**", "Powers the cooling fan.", "none", "yes"],
        ["**Status LEDs**", "Red = power, green = activity (see Part E).", "yes", "yes"],
    ], [3.0, 6.0, 4.1, 4.1], size=8.6)
    d.h2("B6. Pi 4 or Pi 5: what changes in practice")
    d.table(["Topic", "Pi 4", "Pi 5", "What it means for you"], [
        ["Speed", "Cortex-A72, 1.5 GHz", "Cortex-A76, 2.4 GHz", "The Pi 5 is clearly faster. Timings differ: models run slower on a Pi 4."],
        ["Memory", "up to 8 GB", "2, 4, 8 GB", "More RAM = bigger models. Matters most for language models."],
        ["Language models (Phase 3)", "only very small models, slowly: not recommended", "comfortable with small models; 8 GB recommended", "Use a Pi 5 for Phase 3 if you can."],
        ["Power supply", "USB-C, 5 V / 3 A", "USB-C, 5 V / 5 A (27 W) recommended. A 3 A supply works but limits USB devices to 600 mA.", "A weak charger causes random crashes on both boards."],
        ["Power button", "none: plugging in switches it on", "yes", "To restart a halted Pi 4, unplug and replug. On a Pi 5 press the button."],
        ["Cooling", "heatsink or fan case advisable for long runs", "runs hotter; has a fan connector; an active cooler is advisable for long runs", "Check temperatures while a model runs (`vcgencmd measure_temp`)."],
        ["Camera cable", "standard 15-pin ribbon", "smaller 22-pin connector", "Cables differ between boards. Check before buying (Day 4)."],
        ["Operating system", "runs older and newer releases", "needs a recent Raspberry Pi OS", "Always take the newest image Imager offers."],
        ["In Imager", "Device = Raspberry Pi 4", "Device = Raspberry Pi 5", "The only change in the flashing steps."],
        ["SSH, commands, updates, shutdown", "same", "same", "Identical on both boards."],
    ], [2.6, 3.7, 4.9, 6.0], size=8.6)
    d.h2("B7. What you need on the desk")
    d.figure(f"{FIG}/d1_kit.png", 16.4, "What you need today (red) and what is nice to have (green).")
    d.bullets([
        "**microSD card:** 32 GB or more; a reputable brand with an A1 or A2 application-performance rating. Cheap or counterfeit cards are a common cause of strange failures.",
        "**Power supply:** the correct one for your board (Pi 4: 5 V / 3 A; Pi 5: 5 V / 5 A, 27 W). A weak or poor cable causes crashes, not a clean error message.",
        "**Card reader:** a USB reader if your laptop has no microSD slot.",
        "**Optional:** a monitor with a micro-HDMI cable, a USB keyboard and mouse, and an Ethernet cable as a fallback for the first connection. A fan or heatsink case helps during long runs (an active cooler on the Pi 5).",
    ], size=10)
    d.h2("B8. Handling and your first exercise")
    d.callout("warn", "Handling", ["Hold the board by its edges. Do not touch the pins and chips with wet or charged fingers, and do not place it on a metal surface while it is powered."])
    d.p("**Your turn (5 min):** hold your Pi with the GPIO header at the top and find every item in the table above. Take a top-down photo, label it in any editor, and save it as `S4_my_board.jpg`.")
    slot(d, "S4", "ph_S4_my_board.png", 13.5, "Your Raspberry Pi, photographed and labelled by you.")

    # =========================================================== PART C
    d.h1("Part C  -  Operating system and network basics (15 min)")
    d.h2("C1. What is an operating system?")
    d.p("An **operating system (OS)** is the software that manages the computer's hardware and software resources and provides standard services to programs. It sits between the hardware and your applications.")
    d.figure(f"{FIG}/d1_os_layers.png", 15.4, "The layers of a computer: you work with the top layers; the operating system hides the details of the hardware underneath.")
    d.table(["The OS manages...", "What that means"], [
        ["**Processes**", "Shares processor time between the programs that are running."],
        ["**Memory**", "Gives RAM to programs and takes it back when they finish."],
        ["**Files**", "Organises data into files and folders on storage."],
        ["**Devices**", "Talks to hardware (Wi-Fi chip, camera, USB, GPIO) through drivers."],
        ["**The user interface**", "Lets you use the computer: a command line (terminal) or a graphical desktop."],
    ], [4.0, CONTENT_W - 4.0], size=9.5)
    d.p("Its main components are the **kernel** (the core that controls the hardware), the **shell** (the program in which you type commands), the **file system** (how data is stored) and the **drivers** (software that lets the OS talk to a device).")
    d.h2("C2. Linux, Debian and Raspberry Pi OS")
    d.p("**Linux** is a family of free, open-source operating systems built around the Linux kernel. A **distribution** packages the kernel with tools, libraries and a package manager. **Debian** is one of the oldest and most widely used distributions. **Raspberry Pi OS** (formerly called Raspbian) is Debian adapted for the Raspberry Pi's ARM processors and limited resources.")
    d.bullets([
        "**Lightweight:** tailored to run efficiently on the Pi's hardware.",
        "**Versatile:** supports many applications and programming languages.",
        "**Open source:** free to customise, with community-driven improvements.",
        "**GPIO support:** lets software talk to sensors and other electronics.",
        "**Regularly updated:** continual improvements to performance and security.",
    ], size=10)
    d.callout("note", "Versions and Python", [
        "Raspberry Pi OS releases follow Debian releases (for example Debian 12 'Bookworm'; newer Debian releases have since appeared). Imager always offers the current release, and the steps in this course work on current releases. What can differ is the **Python version** that ships with the system; some machine-learning packages are slow to support the newest Python. We handle this on Day 5 with virtual environments, and if necessary an older OS image can be used. That is why you will record your OS and Python versions today."])
    d.h2("C3. Which operating-system image do I choose?")
    d.table(["Choice in Imager", "What it is", "Our choice"], [
        ["**Raspberry Pi OS (64-bit)**", "The full system **with a desktop** (windows, mouse). 64-bit is required or preferred by many AI libraries.", "**Yes: for the Pi 4 and the Pi 5**"],
        ["Raspberry Pi OS Lite (64-bit)", "No desktop; terminal only; uses less RAM. Ideal for tiny boards such as the Pi Zero 2 W.", "Not needed on a Pi 4 or Pi 5"],
        ["32-bit versions", "Older style; fewer AI packages available.", "Avoid"],
    ], [4.4, 8.0, 4.8], size=9.2)
    d.callout("tip", "What does 64-bit mean?", [
        "A 64-bit system can address far more memory and uses the full instruction set of the processor. Most machine-learning packages publish only 64-bit builds for the Pi. You can check later with `uname -m`: the answer `aarch64` means 64-bit ARM; `armv7l` means 32-bit."])
    d.h2("C4. Just enough networking")
    d.p("You will reach the Pi from your laptop over the network, so five ideas matter.")
    d.figure(f"{FIG}/d1_netprimer.png", 16.2, "A typical home or lab network: the router connects the devices to each other and to the Internet.")
    d.table(["Idea", "Explanation"], [
        ["**Router**", "The box that connects your devices (by Wi-Fi or cable) to each other and to the Internet."],
        ["**IP address**", "A device's number on the network, for example `192.168.1.57`: four numbers from 0 to 255. Addresses starting `192.168.`, `10.` or `172.16.` to `172.31.` are private: they work only inside your own network."],
        ["**DHCP**", "A service in the router that gives every device an IP address automatically when it joins. Because of it, an address can change from one day to the next."],
        ["**Host name**", "A human-friendly name for a device, such as `raspi4`. You choose it when preparing the card."],
        ["**The `.local` name**", "Devices announce their names inside the network (a technique called mDNS), so `raspi4.local` finds the Pi without knowing its IP address. It works **only inside one network**, and some networks block it."],
        ["**Wi-Fi bands**", "2.4 GHz reaches further but is slower; 5 GHz is faster but shorter range. The Pi 4 and Pi 5 use both; the Pi Zero 2 W only 2.4 GHz."],
    ], [3.6, CONTENT_W - 3.6], size=9.2)
    d.callout("warn", "Networks that make life harder", [
        "- **Guest networks** and some office or university networks isolate devices from each other, so the laptop cannot see the Pi.",
        "- **Enterprise networks** (WPA2-Enterprise) ask for a user name as well as a password; Imager's simple Wi-Fi form cannot set that up.",
        "- **Public portals** that ask you to log in through a web page cannot be used by a Pi without a screen.",
        "In all these cases, use your **phone's hotspot** or an **Ethernet cable** to a home router for the first connection."])

    # =========================================================== PART D
    d.h1("Part D  -  Prepare the microSD card (35 min)")
    d.h2("D1. The idea")
    d.p("When a Pi is powered, its built-in firmware looks for an operating system on the **microSD card**. 'Installing the OS' therefore means writing an **image** (a complete, ready-to-run copy of the system) onto the card. We use **Raspberry Pi Imager**, a free tool for Windows, macOS and Linux that lists the available images and writes them.")
    d.p("Imager can also store your **settings** (host name, user, password, Wi-Fi, SSH) on the card, so the Pi comes up already configured and needs **no monitor and no keyboard**. Working this way is called **headless**.")
    d.figure(f"{FIG}/d1_flash_flow.png", 16.2, "The whole procedure in five steps. Today you do all five.")
    d.figure(f"{FIG}/d1_filmstrip.png", 16.6, "Key frames of the narrated animation 'Day01_flash_boot_ssh.mp4' (about 70 seconds, English voice-over and subtitles): write the card, insert it, power on, join the Wi-Fi, connect over SSH. Play the video for the full story.")
    d.h2("D2. Install Raspberry Pi Imager")
    d.p("Download the installer from https://www.raspberrypi.com/software/, run it (Windows will ask for permission), and start **Raspberry Pi Imager** from the Start menu. On a Mac, drag the app to Applications; on Linux use the package offered on the same page.")
    d.h2("D3. Step by step on Windows")
    d.step(1, "Insert the microSD card", ["Use the card reader or your laptop's slot.", "If Windows says __'You need to format the disk before you can use it'__, click **Cancel**. Do not format it: Imager does everything."])
    d.step(2, "Choose Device, Operating System and Storage", [
        "- **Raspberry Pi Device** -> `Raspberry Pi 4` (or `Raspberry Pi 5`: the only difference between the boards in this procedure)",
        "- **Operating System** -> `Raspberry Pi OS (64-bit)`",
        "- **Storage** -> your microSD card. Check that the size and the drive letter match your card; a 32 GB card shows about 29 to 30 GB.",
        "Then press **Next**."])
    d.callout("warn", "Pick the right storage device", ["Imager erases whatever you choose. If a USB drive or external disk is attached, unplug it first so that it can never be selected by mistake. This is the most common and most costly student accident."])
    u = user_shot("S1")
    d.figure_pair(f"{BOOK}/imager_step2.png", u or f"{FIG}/ph_S1_imager_windows.png", 8.1,
                  "Raspberry Pi Imager with device, operating system and storage chosen (example on a Mac, older release).",
                  "Your Imager window on Windows" + ("." if u else " (capture slot)."))
    d.step(3, "Open the settings (OS customisation)", [
        "Older Imager versions show a **gear icon** after Next. Newer versions ask something like __'Would you like to apply OS customisation settings?'__: choose **Edit settings** or **Customise**, or follow the step-by-step screens. The options are the same; this section lists them."])
    d.h2("D4. The settings, one by one")
    d.table(["Setting", "What to enter", "Why it matters"], [
        ["**Host name**", "`raspi4` (any name with letters, digits and hyphens, no spaces)", "The Pi's name on the network; you will reach it as `raspi4.local`. Give each Pi a different name (for example `raspi-lab`, `raspi-home`)."],
        ["**User name and password**", "your own, e.g. `piuser`, with a strong password", "Raspberry Pi OS no longer has a default user. You need this password for SSH and for administrator commands. It is case-sensitive. **Write it on your connection card.**"],
        ["**Wi-Fi**", "network name (SSID) and password, **exactly as spelled**", "The Pi must join your network by itself at the first boot. A typo here is the most frequent reason a Pi 'cannot be found'."],
        ["**Wi-Fi country**", "the country where the Pi will run, e.g. `KW`, `EG`, `US`", "Radio regulations (channels, power) differ by country; the Pi needs the code to switch its Wi-Fi on legally."],
        ["**Time zone and keyboard**", "e.g. `Asia/Kuwait`, `us`", "Correct clock (logs, certificates) and the right characters when you type."],
        ["**SSH**", "**Enable SSH**, use password authentication (Services tab)", "**Essential.** Without it the Pi accepts no remote logins and you would need a monitor and keyboard."],
    ], [3.4, 5.4, 8.4], size=8.8)
    d.figure(f"{BOOK}/imager_customisation.png", 15.0, "The OS customisation screens: General tab (host name, user, password, Wi-Fi) and Services tab (Enable SSH).")
    slot(d, "S2", "ph_S2_customisation.png", 13.0, "Your customisation screens (hide the Wi-Fi password).")
    d.callout("warn", "Wi-Fi: one network only", ["Imager stores a single Wi-Fi network. If the Pi must work in two places (lab and home), add the second network later from the Pi (Day 2). If your network is an enterprise or guest network (Part C), use a hotspot or an Ethernet cable now."])
    d.h2("D5. Write the card")
    d.step(4, "Write", [
        "Confirm the warning that **all data on the card will be erased**. Imager now **writes** the image and then **verifies** it. This takes several minutes (about 5 to 15, depending on the card and the reader). Do not remove the card or close Imager.",
        "When you see **'Write successful'**, click Continue and remove the card (Imager ejects it for you)."])
    d.callout("tip", "While you wait", ["Watch the animation, or read Part F ahead of time."])

    # =========================================================== PART E
    d.h1("Part E  -  First boot (10 min)")
    d.h2("E1. Steps")
    d.step(1, "Insert the card into the Pi", ["The microSD slot is on the **underside** of the board. Slide the card in with the label facing away from the board (contacts toward the board) until it stops. Do not force it."], color=AMBER)
    d.step(2, "Connect the optional extras first", ["If you have a monitor, plug it into the micro-HDMI port **nearest the USB-C connector**, and connect the keyboard and mouse, **before** the power. With SSH you do not need them."], color=AMBER)
    d.step(3, "Connect the power last", ["Plug the USB-C supply into the Pi and then into the wall. The **Pi 4** has no power button: plugging in switches it on. The **Pi 5** also starts on power and additionally has a power button; use the **27 W (5 V / 5 A)** supply."], color=AMBER)
    d.step(4, "Read the LEDs and wait", [
        "- **Red LED, steady** = power is good.",
        "- **Green LED, flickering** = the Pi is reading the card (it is booting).",
        "The first boot takes **a few minutes**; the Pi may restart once. Do not unplug it."], color=AMBER)
    d.h2("E2. What happens during the first boot")
    d.figure(f"{FIG}/d1_boot.png", 16.2, "The boot sequence. Step 4 happens only the first time: the Pi expands the file system to fill your card and applies the settings you typed in Imager.")
    d.table(["LEDs", "Meaning", "What to do"], [
        ["Red steady, green flickering", "Powered and reading the card: booting.", "Wait 1 to 3 minutes."],
        ["Red steady, green off after a while", "Booted, idle (or no OS found if the green LED never flickered).", "If it never flickered: reseat the card or write it again."],
        ["Nothing lights up", "No power.", "Try another cable or charger (Pi 4: 5 V / 3 A, Pi 5: 5 V / 5 A)."],
        ["Random restarts, red LED dies", "Weak power supply.", "Use the proper charger and cable."],
    ], [4.6, 6.4, 6.2], size=9)
    d.callout("tip", "Heat", ["A Pi that is only idling stays cool, but a Pi 5 (and a Pi 4 under load) gets hot in long runs. If you plan to run models for hours, fit a heatsink or fan (an active cooler on the Pi 5)."])

    # =========================================================== PART F
    d.h1("Part F  -  First SSH login from Windows (15 min)")
    d.h2("F1. What is SSH?")
    d.p("**SSH** (Secure Shell) gives you the Pi's command line in a window on your laptop. Two programs cooperate: an SSH **server** on the Pi (listening on port 22) and an SSH **client** on your laptop. Everything you type and everything the Pi answers travels **encrypted** over your network, which is why you need no monitor, keyboard or mouse on the Pi. Both machines must be on the **same network** (Part C).")
    d.figure(f"{FIG}/d1_ssh_idea.png", 15.5, "What SSH does: your typing travels to the Pi; the Pi's text answers travel back.")
    d.h2("F2. Steps")
    d.step(1, "Open PowerShell", ["Press the Windows key, type `PowerShell` and press Enter. Windows 10 and 11 include the SSH client. Test it: `ssh -V` should print a version. If Windows says it is 'not recognized', add **OpenSSH Client** in Settings -> Apps -> Optional features. (On a Mac or Linux, open Terminal; the command is the same. PuTTY is an older graphical alternative on Windows.)"], color="2E8B57")
    d.step(2, "Connect", ["Type the command below, replacing `piuser` with your user name. You can use the host name, or the IP address of the Pi if you know it (for example from your router's list of connected devices)."], color="2E8B57")
    d.code(["ssh piuser@raspi4.local", "# or, with the IP address:", "ssh piuser@192.168.1.57"])
    d.step(3, "Answer the first-time question", ["The first time, the client does not know this Pi and shows a message with the Pi's 'key fingerprint', asking whether you trust it. Type the whole word `yes` and press Enter. (The client then remembers the Pi. If you re-write the card later, the Pi gets a new identity and you will see a warning: see Part G.)"], color="2E8B57")
    d.step(4, "Type the password", ["**Nothing appears while you type**: no dots, no stars. That is normal: it is a security feature. Type it and press Enter."], color="2E8B57")
    d.code(["PS C:\\> ssh piuser@raspi4.local",
            "The authenticity of host 'raspi4.local (192.168.1.57)' can't be established.",
            "ED25519 key fingerprint is SHA256:...",
            "Are you sure you want to continue connecting (yes/no/[fingerprint])? yes",
            "Warning: Permanently added 'raspi4.local' (ED25519) to the list of known hosts.",
            "piuser@raspi4.local's password:",
            "...",
            "piuser@raspi4:~ $"], kind="term")
    u = user_shot("S3")
    d.figure_pair(f"{BOOK}/ssh_first_login.png", u or f"{FIG}/ph_S3_powershell_login.png", 8.1,
                  "A first SSH login (example on a Mac). The prompt `user@host:~ $` means you are connected.",
                  "Your PowerShell after a successful login" + ("." if u else " (capture slot)."))
    d.h2("F3. Reading the prompt")
    d.table(["Part of `piuser@raspi4:~ $`", "Meaning"], [
        ["`piuser`", "the user you are logged in as"], ["`@`", "'at'"], ["`raspi4`", "the host name of the computer you are on: **the Pi**, not your laptop"],
        ["`:`", "separator"], ["`~`", "the current folder; `~` is your home folder"], ["`$`", "the shell is ready for a command (`#` would mean administrator)"],
    ], [6.5, CONTENT_W - 6.5], size=9.2)
    d.callout("note", "You are now inside the Pi", ["From now on, every command you type runs on the Pi, not on your laptop. The window is only a view. To leave, type `exit`."])
    d.h2("F4. Your first commands")
    d.table(["Command", "What it does", "Typical output"], [
        ["`hostname -I`", "Shows the Pi's IP address(es).", "`192.168.1.57`"],
        ["`uname -m`", "Shows the processor architecture.", "`aarch64` = 64-bit. (`armv7l` would mean a 32-bit system.)"],
        ["`cat /etc/os-release`", "Shows which operating system and release this is.", "`PRETTY_NAME=\"Debian GNU/Linux 12 (bookworm)\"` or a newer release"],
        ["`python3 --version`", "Shows the Python version.", "`Python 3.x.y`. Write it down; we need it on Day 5."],
        ["`free -h`", "Shows memory in a human-readable form.", "total close to 4 GB on a 4 GB board (a little less)"],
        ["`vcgencmd measure_temp`", "Shows the processor temperature.", "`temp=46.2'C`"],
    ], [4.6, 6.0, 6.6], size=9)
    d.h2("F5. Updating the system")
    d.p("Linux software comes in **packages** managed by a tool called `apt`. Two commands keep the system current. `sudo` (superuser do) means 'run this as administrator'; you will be asked for your password.")
    d.code(["sudo apt-get update      # refresh the list of available packages",
            "sudo apt upgrade        # install newer versions of what is already installed",
            "# apt asks 'Do you want to continue? [Y/n]': type Y and press Enter."])
    d.p("This needs the Internet and may take several minutes the first time. Run it regularly. If the upgrade installs a new kernel, restart with `sudo reboot`.")
    d.h2("F6. Shutting down and restarting safely")
    d.p("Never just pull the plug. While the Pi runs, it may still be writing to the microSD card; cutting the power then can lose data or corrupt the card. Use the command, and wait until the **green LED stops flashing and stays dark** before removing the power.")
    d.code(["sudo shutdown -h now    # halt (switch off) the Pi", "sudo reboot              # restart"])
    d.callout("tip", "Starting a halted Pi again", ["**Pi 4:** unplug the power and plug it in again. **Pi 5:** press the power button. (The command does not power the board off completely; it stops the system safely.)"])
    d.h2("F7. Moving files (a preview)")
    d.p("Files move between your laptop and the Pi with a USB drive, with the `scp` command in a terminal, or with an SFTP program such as FileZilla or WinSCP. We do this properly on Day 2.")

    # =========================================================== PART G
    d.h1("Part G  -  When something does not work")
    d.table(["What you see", "Most likely cause", "What to try"], [
        ["`Could not resolve hostname raspi4.local`", "The Pi is not on the network yet; a typo in the Wi-Fi settings; or the network blocks `.local` names.", "Wait 5 minutes. Check the Wi-Fi name and password. Look up the Pi's IP address in your router's device list and use it instead. Try an Ethernet cable or your phone hotspot."],
        ["`Connection timed out`", "Laptop and Pi are on different networks; a VPN is active; or a guest or office network isolates devices.", "Put both on the same Wi-Fi. Switch the VPN off. Use a phone hotspot."],
        ["`Permission denied, please try again`", "Wrong user name or password.", "Both are case-sensitive. Retype slowly; check the keyboard layout. If you forgot the password, write the card again."],
        ["`REMOTE HOST IDENTIFICATION HAS CHANGED`", "You re-wrote the card, so the Pi has a new identity under the same name.", "Run `ssh-keygen -R raspi4.local` on your laptop, then connect again."],
        ["`ssh` is not recognized", "The OpenSSH client is not installed on Windows.", "Settings -> Apps -> Optional features -> add OpenSSH Client."],
        ["Red LED on, green LED never flickers", "The Pi found no operating system on the card.", "Reseat the card; write it again; try another card."],
        ["Nothing lights up", "No power.", "Try another cable and charger."],
        ["The Pi never appears on the network", "Wi-Fi typo, wrong country code, a hidden network, an enterprise or portal network.", "Re-write the card with corrected settings, or use Ethernet or a hotspot."],
        ["It worked yesterday, now it cannot be found", "The router gave the Pi a new IP address, or the Pi is on another network.", "Use `raspi4.local`, or find the new address in the router's list."],
    ], [4.6, 5.4, 7.2], size=8.8)

    # =========================================================== PART H
    d.h1("Working with more than one Pi or computer")
    d.p("Many learners have two Pis (for example one in the lab and one at home) and two laptops. Think of the Pi as the **shared workspace** and each laptop as a **window** into it. Your code and notes live on the Pi and in a shared online repository; the laptops are interchangeable.")
    d.figure(f"{FIG}/d1_network.png", 16.2, "Left: how Day 1 works. Right: when the laptop and the Pi are on different networks, the `.local` name does not work and extra tools are needed.")
    d.bullets([
        "**Learn on one Pi, then repeat on the other from your notes only.** The second pass is faster and reveals every hidden assumption.",
        "**Give each Pi a different host name** (for example `raspi-lab` and `raspi-home`) and the same user name.",
        "**Keep a connection card** (Appendix A) for each Pi.",
        "**Two networks:** either carry the Pi and teach it both Wi-Fi networks (Day 2), or leave it in one place and reach it from elsewhere with a remote-access service (Day 2 compares the options).",
    ], size=10)

    # =========================================================== check yourself / instructor notes
    d.h1("Check yourself")
    d.p("Answer from memory first; the answers follow.", after=3)
    qs = ["What is the difference between cloud AI and Edge AI?",
          "Give three advantages of running AI at the edge, and one price you pay for it.",
          "What is the difference between training and inference? Which one happens on the Pi in this course?",
          "Image classification belongs to which family of AI? Give one example from the other family.",
          "What is a single-board computer, and why does a Raspberry Pi need a microSD card?",
          "Name three things an operating system manages.",
          "What is an IP address? What is DHCP? Why does `raspi4.local` work only inside one network?",
          "Why choose the 64-bit Raspberry Pi OS? Which command tells you which one you have?",
          "Why enable SSH in Imager before writing the card?",
          "What does a steady red LED mean? A flickering green LED?",
          "What can go wrong if you unplug the Pi without shutting it down? How do you restart a halted Pi 4? A Pi 5?",
          "Name three differences between the Pi 4 and the Pi 5."]
    for i, q in enumerate(qs, 1):
        p = d.d.add_paragraph(); p.paragraph_format.left_indent = Cm(0.7); p.paragraph_format.first_line_indent = Cm(-0.7); para_fmt(p, after=3)
        r = p.add_run(f"{i}.  "); r.bold = True; r.font.color.rgb = rgb(RASP); add_runs(p, q, size=10)
    d.callout("note", "Answers", [
        "1) Cloud AI sends data to a data centre and waits for the answer; Edge AI runs the model on the device next to the sensor.  "
        "2) Low latency, privacy, network independence, lower bandwidth, energy efficiency; the price is limited processor, memory and power, so models must be small and optimised.  "
        "3) Training builds the model from examples (heavy, on a laptop or cloud); inference uses it on new data (light, on the Pi).  "
        "4) Fixed-function (reactive); generative examples: language models, image generators, assistants.  "
        "5) A complete computer on one board; it has no built-in disk, so the OS and files live on the microSD card.  "
        "6) Processes, memory, files, devices, the user interface.  "
        "7) A device's number on the network; the router service that hands out addresses automatically; `.local` names are announced only inside the local network.  "
        "8) Many AI packages are built only for 64-bit; `uname -m` shows `aarch64` for 64-bit.  "
        "9) So the Pi accepts remote logins and needs no monitor or keyboard.  "
        "10) Power is good; the Pi is reading the card.  "
        "11) Data loss or a corrupted card; Pi 4: unplug and replug; Pi 5: press the power button.  "
        "12) For example: speed (A72 vs A76), power button, power supply, cooling, camera connector, RAM options."], size=9.3)
    d.h1("Instructor notes")
    d.callout("teach", "A 45-minute classroom version", [
        "- **Before class:** each pair gets a Pi, a card, a reader, a power supply, and a hotspot or router for the network; Imager is pre-installed.",
        "- **10 min:** the big picture (Part A, cloud versus edge and the two families).  **15 min:** flash the cards live (Part D).  **10 min:** boot and LEDs.  **10 min:** SSH and the first commands.",
        "- **Typical mistakes:** the wrong storage device chosen; a Wi-Fi typo; SSH not enabled; a guest or enterprise network; unplugging without shutdown; the 'host identification changed' warning after re-flashing.",
        "- **Mini-assessment:** each pair submits a screenshot showing `hostname -I`, `uname -m` and `free -h` (with Wi-Fi details hidden).",
        "- **Mixed boards:** if the class has both Pi 4 and Pi 5, use the comparison in Part B6 and let students swap boards for the second pass.",
    ])
    d.h1("Glossary")
    d.table(["Term", "Meaning"], [
        ["Edge AI / cloud AI", "AI that runs on the device next to the data / AI that runs in a remote data centre."],
        ["Training / inference", "Building a model from examples / using a trained model on new data."],
        ["Fixed-function AI / generative AI", "Reactive AI for defined tasks / AI that creates content and keeps context."],
        ["SBC, SoC", "Single-board computer; system on a chip (processor, graphics and controllers in one package)."],
        ["GPIO", "General-purpose input/output pins used to connect electronics."],
        ["CSI, DSI", "Ribbon-cable connectors for a camera / for a display."],
        ["microSD card", "The removable storage that holds the Pi's operating system and files."],
        ["Image, Imager", "A complete copy of an operating system; the tool that writes it to a card."],
        ["Operating system, kernel, shell", "The software that manages the hardware; its core; the program in which you type commands."],
        ["Linux, Debian, Raspberry Pi OS", "A family of open-source operating systems; a major distribution; the Debian-based system for the Pi."],
        ["64-bit, aarch64", "A system that uses the full 64-bit processor; the name of 64-bit ARM."],
        ["Headless", "Working with a computer that has no monitor, keyboard or mouse."],
        ["Router, IP address, DHCP", "The device that connects a network; a device's number; the service that assigns numbers."],
        ["Host name, mDNS, `.local`", "A device's name; the way names are announced inside a network; the name suffix that results."],
        ["SSID, 2.4 GHz / 5 GHz", "A Wi-Fi network's name; the two Wi-Fi radio bands."],
        ["SSH, terminal, PowerShell", "Secure remote command line; a text window for commands; Windows' command-line program."],
        ["`sudo`, `apt`", "Run as administrator; the package manager that installs and updates software."],
        ["Firmware", "Built-in software on the board that starts the boot process."],
    ], [5.2, CONTENT_W - 5.2], size=9)

    # =========================================================== appendices
    d.page_break()
    d.h1("Appendix A  -  My connection card")
    d.p("Fill this in for each Pi and keep it with the board. (Do not write the password itself if the page will be shared.)", after=3)
    rows = ["Board (Pi 4 / Pi 5, RAM)", "Host name", "User name", "Password hint (not the password)", "Wi-Fi network 1 (name)", "Wi-Fi network 2 (name)", "IP address (can change)", "OS release (cat /etc/os-release)", "Python version", "Architecture (uname -m)", "microSD size and brand", "Date written / notes"]
    t = d.d.add_table(rows=len(rows), cols=2); t.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, k in enumerate(rows):
        a, b = t.rows[i].cells; no_split(t.rows[i]); shade(a, "EEF1F4")
        for c in (a, b): cell_margins(c, 60, 60, 120, 120); borders(c, bottom=(6, "9AA5B1"), top=(6, "9AA5B1") if i == 0 else None, left=(6, "9AA5B1"), right=(6, "9AA5B1"))
        add_runs(a.paragraphs[0], k, size=9.5, bold=True, color=NAVY); para_fmt(a.paragraphs[0], after=0)
    set_col_widths(t, [6.0, CONTENT_W - 6.0]); d.spacer(6)
    d.page_break()
    d.h1("Appendix B  -  My notes and questions")
    t = d.d.add_table(rows=26, cols=1); t.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i in range(26):
        c = t.rows[i].cells[0]; borders(c, bottom=(4, "B8C2CC")); cell_margins(c, 150, 60, 60, 60); para_fmt(c.paragraphs[0], after=0)
    set_col_widths(t, [CONTENT_W])
    d.page_break()
    d.h1("Acknowledgments and references")
    d.p("This course is a compilation: it combines material from the sources below with new explanations, examples, diagrams, exercises and comments written for this course. The original authors are gratefully acknowledged.", size=10)
    d.reflist(REFERENCES)
    d.p(FIGURE_CREDIT, size=9, italic=True)
    d.save(f"{OUT}/Day01_Meet_Your_Raspberry_Pi.docx")

if __name__ == "__main__":
    make_filmstrip()
    build()
    print("built")
