import os, sys, glob
sys.path.insert(0, os.path.dirname(__file__))
from docx_lib import *
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
FIG = f"{ROOT}/day01/figures"; BOOK = f"{ROOT}/_assets/book"; SHOTS = f"{ROOT}/my_screenshots/day01"
OUT = f"{ROOT}/day01"
BOOKSRC = "Source: M. Rovai, Edge AI Engineering: Hands-on with the Raspberry Pi (2025), PDF p. {p}"

def user_shot(prefix):
    for ext in ("png", "jpg", "jpeg"):
        m = glob.glob(f"{SHOTS}/{prefix}*.{ext}")
        if m: return m[0]
    return None

# ---- composite: animation filmstrip (3 x 2 grid, last tile = how to play)
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

def shot_or_placeholder(d, prefix, placeholder, width, caption):
    p = user_shot(prefix)
    if p: d.figure(p, width, caption + "  (your own capture)")
    else: d.figure(f"{FIG}/{placeholder}", width, caption + "  -- capture slot, see instructions inside the frame.")

def build():
    d = Doc("Edge AI with the Raspberry Pi  |  Hands-on study course  |  Day 01",
            "Prof. Basem M. ElHalawany  -  personal study & teaching reference  -  figures from Rovai (2025) are credited where used")
    d.title_block("Day 01 of the Edge AI study course", "Meet Your Raspberry Pi 4\nand Bring It to Life",
                  "Flash the operating system, boot for the first time, and log in from your Windows laptop.")
    d.meta_table([
        ("Time needed", "2 hours (5 short parts, A to E).  Slow is fine; the 'Check yourself' section tells you when you are done."),
        ("Your hardware", "Raspberry Pi 4 Model B (4 GB), microSD card, USB-C power supply (5 V / 3 A), Windows laptop with Wi-Fi."),
        ("Book", "Rovai, __Edge AI Engineering: Hands-on with the Raspberry Pi__ (2025) - PDF pp. 20-21, 25-27 and 29-38 (printed pages are one lower)."),
        ("Course material", "IESTI05 Edge AI - Class 3 'Raspberry Pi Setup Walkthrough' (slides + video).  Repo: UNIFEI-IESTI05-EDGE_AI."),
        ("Outcome", "A Pi 4 that boots, joins your Wi-Fi, and answers you in a PowerShell window - and you understand every step you took."),
        ("Next day", "Day 02 - Remote access like a pro: file transfer, remote desktop, working from the office and from home."),
    ])

    d.h2("What you will be able to do by the end of today")
    d.checks([
        "Explain in two sentences what Edge AI is, and why a small, low-cost board is a serious tool for it.",
        "Name the main parts of the Raspberry Pi 4 and say what each is for.",
        "Write a ready-to-boot operating system onto a microSD card, with your own name, user and Wi-Fi settings.",
        "Power the Pi, read its two LEDs, and wait out the first boot calmly.",
        "Open a secure shell (SSH) from Windows, run your first five Linux commands, and shut the Pi down safely.",
    ])
    d.h2("Your 2-hour plan")
    d.figure(f"{FIG}/d1_roadmap.png", 16.2, "The two hours at a glance. Part C (the microSD) is the longest; do not rush it.")
    d.callout("note", "Before you start (10 minutes the evening before)", [
        "- Download **Raspberry Pi Imager** for Windows from https://www.raspberrypi.com/software/ (the address used in the course slides) and install it.",
        "- Check that you know your **Wi-Fi name and password**, and which network the Pi will live on.",
        "- Back up anything you care about on the microSD card. **Imager will erase the whole card.**",
    ])

    # ------------------------------------------------------------------ PART A
    d.h1("Part A  -  The big picture (20 min)")
    d.callout("book", None, ["Book PDF pp. 20-21 (Introduction: why Edge AI, the Raspberry Pi advantage) and pp. 25-27 (Classification of AI applications).",
                                     "Read once quickly, then come back and fill in the sketch below in your own words."])
    d.h2("A1. What is Edge AI?")
    d.p("Most AI you use (a chatbot, a photo-tagging app) runs in a **data centre**: your data travels there, the answer travels back. "
        "**Edge AI** runs the model **on the device that is next to the data** - a camera, a robot, a sensor box, a Raspberry Pi. "
        "The book gives five reasons this matters:")
    d.table(["Advantage", "What it means in practice"], [
        ["Low latency", "Answer in milliseconds - no round trip to a server (a robot can react to an obstacle now)."],
        ["Privacy", "Raw images/audio never leave the device."],
        ["Network independence", "Works in a tunnel, a field or a factory with no Internet."],
        ["Lower bandwidth", "Send a 5-byte result instead of a video stream."],
        ["Energy efficiency", "Small, optimised models on small hardware use far less power than a cloud round trip."],
    ], [4.2, CONTENT_W - 4.2])
    d.h2("A2. The two families of AI in this course")
    d.p("The book splits its chapters into two families. Keep this map in mind - the whole study plan follows it.")
    d.table(["", "Fixed-function AI (reactive)", "Generative AI (proactive)"], [
        ["Idea", "Looks at an input and returns a fixed kind of answer", "Creates new content: text, descriptions, plans"],
        ["Examples in the book", "Image classification, object detection, counting objects with YOLO", "Small language models (SLMs), vision-language models, agents"],
        ["Typical resources", "Small, fast, predictable", "Bigger models: RAM matters a lot"],
        ["Where in your plan", "Phase 2 (Days 14-26)", "Phase 3 (Days 27-36)"],
    ], [3.4, 6.9, 6.9])
    d.callout("note", "A note about YOUR board (Pi 4, 4 GB)", [
        "The book is written mainly around the **Raspberry Pi Zero 2 W and the Pi 5**, and says the Pi 5 instructions also apply to the Pi 3 and Pi 4 (PDF p. 29). "
        "Everything in Phase 2 (vision) will run well on a Pi 4. For Phase 3 (language models) a 4 GB Pi 4 can run only the **small** models and will be slower than the book's Pi 5 timings - "
        "we will adapt the model choices when we get there, and I will tell you honestly when a result is slower than the book's."])

    # ------------------------------------------------------------------ PART B
    d.h1("Part B  -  Meet the board (20 min)")
    d.callout("book", None, ["Book PDF pp. 29-33 (Setup: introduction, models, hardware overview). The book's labelled figure is for the Pi 5 - your Pi 4 is similar, as compared below."])
    d.h2("B1. What is in the box on your desk")
    d.figure(f"{FIG}/d1_kit.png", 16.4, "What you need today (red) and what is nice to have (green).")
    d.h2("B2. Anatomy of the Pi 4")
    d.figure(f"{FIG}/d1_pi4_anatomy.png", 16.2, "Schematic of the Raspberry Pi 4 B. Port positions are simplified: compare with your real board and correct the picture if you spot a difference.")
    d.figure(f"{BOOK}/pi5_diagram.png", 12.8, "The book's labelled photo of the Raspberry Pi 5 (for comparison; the Pi 5 adds a power button and a PCIe connector that your Pi 4 does not have).",
             BOOKSRC.format(p="33"))
    d.table(["Part", "What it does", "Why you will care later"], [
        ["CPU (Cortex-A72, 4 cores, 1.5 GHz)", "Runs the OS and all your code", "It does the neural-network maths. Slower than a Pi 5, but enough for Phase 2."],
        ["RAM (4 GB)", "Working memory for running programs", "Models must fit in RAM. This is the limit to watch in Phase 3."],
        ["microSD card", "The Pi's hard disk: OS + your files", "Quality matters. Always shut down before unplugging."],
        ["40-pin GPIO header", "Pins to read sensors and switch LEDs/relays", "Physical computing - Phase 3."],
        ["Camera connector (CSI) / USB ports", "Plug in a Pi camera or a USB webcam", "Vision projects, Day 5."],
        ["Wi-Fi, Bluetooth, Ethernet", "Network access", "How you will talk to the Pi from your laptop."],
        ["2 x micro-HDMI", "Connect a monitor", "Optional: SSH makes a screen unnecessary."],
        ["USB-C power input", "Needs 5 V / 3 A", "A weak charger causes random crashes."],
    ], [4.6, 5.8, 6.8], size=9)
    d.p("**Your turn (5 min):** take your Pi, hold it with the GPIO header at the top, and find every item in the table. "
        "Take a top-down photo with your phone and label it - save it as `S4_my_board.jpg` (instructions below).")
    shot_or_placeholder(d, "S4", "ph_S4_my_board.png", 13.5, "Your Pi 4, photographed and labelled by you.")
    d.callout("warn", "Handling", ["Hold the board by its edges. Do not touch the golden pins and chips with wet or charged fingers; do not put it on a metal surface while it is powered."])

    # ------------------------------------------------------------------ PART C
    d.h1("Part C  -  Prepare the microSD card (45 min)")
    d.callout("book", None, ["Book PDF pp. 34-37 (Installing the Operating System: installation, initial configuration).  Course video: Class 3 'Raspberry Pi Setup Walkthrough' (see Resources)."])
    d.h2("C1. First, the idea")
    d.p("A Pi has no built-in storage. When it is powered, it looks for an operating system (OS) on the **microSD card**. "
        "So 'installing the OS' means **writing an image** - a complete copy of a ready-to-run system - onto the card. "
        "We use **Raspberry Pi Imager** for that, and, very usefully, we also use it to bake in our **settings** (computer name, user, Wi-Fi, SSH) so that the Pi comes up already configured and needs **no monitor and no keyboard** (this is called a *headless* setup).")
    d.figure(f"{FIG}/d1_flash_flow.png", 16.2, "The whole procedure in five steps. Today you do all five.")
    d.figure(f"{FIG}/d1_filmstrip.png", 16.6, "Key frames of the narrated animation 'Day01_flash_boot_ssh.mp4' (about 70 s, English voice-over + subtitles): write the card, insert it, power on and first boot, join Wi-Fi, SSH from the laptop. Play the video file for the full story.")
    d.h2("C2. Which operating system?")
    d.p("The OS for the Pi is **Raspberry Pi OS**, a version of Linux (Debian). The book explains OS, kernel, shell and file system on PDF p. 34; skim it now.")
    d.table(["Choice in Imager", "What it is", "Our decision"], [
        ["Raspberry Pi OS (64-bit)", "Full system **with a desktop** (windows, mouse). 64-bit is required by many AI libraries.", "**Choose this one** - you can plug in a monitor, and we can later open the desktop remotely."],
        ["Raspberry Pi OS Lite (64-bit)", "No desktop; terminal only; uses less RAM. (Avoid the 32-bit versions.)", "The book uses Lite for the tiny Pi Zero. Not needed on your 4 GB Pi 4 today."],
    ], [4.4, 7.4, 5.4], size=9)
    d.callout("note", "The book says 'Bookworm' - your Imager may offer something newer", [
        "The book (Oct 2025) mentions the then-latest release, **Debian 12 'Bookworm'**. A newer Imager may offer a newer Debian base. The steps are identical. "
        "What can differ is the **Python version**, and TensorFlow Lite (Day 4-5) is picky about it. That is why Part E records your OS and Python version - we will check them on Day 4 rather than guess now."])

    d.h2("C3. Step by step on Windows")
    d.step(1, "Install and open Raspberry Pi Imager", ["Run the installer you downloaded, then start **Raspberry Pi Imager** from the Start menu. If Windows asks permission, allow it."])
    d.step(2, "Insert the microSD card", ["Use the card reader (or your laptop's slot).",
                                           "If Windows says __'You need to format the disk before you can use it'__ - click **Cancel**. Do **not** format it; Imager handles everything."])
    d.step(3, "Choose Device, OS and Storage", [
        "- **Raspberry Pi Device** -> `Raspberry Pi 4`",
        "- **Operating System** -> `Raspberry Pi OS (64-bit)`",
        "- **Storage** -> your microSD card. Check the size and drive letter match your card. A 32 GB card shows about 29-30 GB.",
        "Then press **Next**."])
    d.callout("warn", "Pick the right storage device", ["Imager erases whatever you choose. If you also have a USB drive or external disk attached, unplug it first, so it can never be selected by mistake. This is the number-one student accident."])
    u = user_shot("S1")
    d.figure_pair(f"{BOOK}/imager_step2.png", u or f"{FIG}/ph_S1_imager_windows.png", 8.1,
                  "The book's Imager (v1.8.5 on macOS): Pi 5 + full 64-bit OS chosen. Yours: Pi 4.",
                  "Your Imager window on Windows" + ("." if u else " (capture slot)."), BOOKSRC.format(p="36"))
    d.step(4, "Open the customisation (settings) screen", [
        "The book clicks the **gear icon** after Next. Newer Imager versions ask something like __'Would you like to apply OS customisation settings?'__ - answer **Edit settings / Customise**, "
        "or follow their step-by-step screens. Look for the same options on the two tabs described below."])
    d.table(["Setting", "What to enter", "Why"], [
        ["Hostname", "`raspi4`", "The Pi's name on the network. You will reach it as `raspi4.local`."],
        ["Username / password", "your own, e.g. `piuser` + a strong password", "There is no default user any more. **Write it on your connection card** (Appendix A)."],
        ["Wi-Fi (SSID + password)", "your network exactly as spelled (case matters)", "The Pi has to join your network on its own at first boot."],
        ["Wi-Fi country", "`KW` (use the country where the Pi will run)", "The Pi needs it to enable the right Wi-Fi channels."],
        ["Time zone / keyboard", "`Asia/Kuwait`, `us`", "Correct clock and keyboard layout."],
        ["SSH (Services tab)", "**Enable SSH**, use password authentication", "**Very important** (the book says so). Without it you cannot log in remotely."],
    ], [4.0, 5.7, 7.5], size=9)
    d.figure(f"{BOOK}/imager_customisation.png", 15.0, "The book's customisation screens: left = General (hostname, user, password, Wi-Fi), right = Services (Enable SSH).", BOOKSRC.format(p="37"))
    shot_or_placeholder(d, "S2", "ph_S2_customisation.png", 15.0, "Your customisation screens (hide the Wi-Fi password).")
    d.callout("warn", "Office Wi-Fi may not work for the Pi", [
        "Many offices and universities use a login-based network (WPA2-Enterprise) or a guest network that blocks device-to-device traffic. "
        "Imager's simple Wi-Fi form takes only a name and a password. If your office network needs a username, use your **phone's hotspot** (2.4/5 GHz) or an **Ethernet cable** for the first boot. "
        "Also: you can only store one network in Imager today; we will add the second (home/office) on Day 2.",
    ])
    d.step(5, "Write the card", ["Confirm the warning that all data on the card will be erased. Imager now **writes** and then **verifies**. This takes several minutes - do not remove the card or close Imager.",
                                  "When you see **'Write successful'**, click Continue and remove the card (Imager ejects it for you)."])
    d.callout("tip", "While you wait", ["Watch the narrated animation (tutorials/day01/animations) or read Part E ahead of time."])

    # ------------------------------------------------------------------ PART D
    d.h1("Part D  -  First boot (15 min)")
    d.step(1, "Insert the card into the Pi", ["The microSD slot is on the **underside** of the board, on the short edge opposite the Ethernet/USB ports. Slide the card in with the **label facing away from the board** (contacts toward the board) until it stops.", "Do not force it."], color=AMBER)
    d.step(2, "Connect the optional extras first", ["If you have a monitor/keyboard, connect them **before** the power (the Pi reads the screen when it starts). With SSH you do not need them."], color=AMBER)
    d.step(3, "Power it last", ["Plug the USB-C supply into the Pi, then into the wall. The Pi 4 has **no power button** - plugging in turns it on."], color=AMBER)
    d.step(4, "Read the LEDs and wait", [
        "- **Red LED, steady** = power is good.", "- **Green LED, flickering** = the Pi is reading the card (booting).",
        "The first boot takes **a few minutes** (the book says so too) because the Pi resizes the file system and applies your settings; it may restart once. Do not unplug it."], color=AMBER)
    d.callout("warn", "If something is off", ["- Nothing lights up: check the power supply and cable.", "- Red LED only, green never flickers: the Pi found no system on the card - reseat the card; if that fails, write it again.", "- It dies or restarts randomly: suspect a weak power supply (5 V / 3 A needed)."])

    # ------------------------------------------------------------------ PART E
    d.h1("Part E  -  First SSH login from Windows (20 min)")
    d.callout("book", None, ["Book PDF pp. 38-39 (Remote Access: SSH Access, shutting down). Slides: Class 3, slide 7 (says: on Windows use Command Prompt or PowerShell)."])
    d.p("**SSH** (Secure Shell) gives you the Pi's command line in a window on your laptop, over your Wi-Fi, encrypted. Both machines must be on the **same network**. "
        "The Pi 4 is dual-band (2.4 and 5 GHz); the book notes the Pi Zero is 2.4 GHz only.")
    d.figure(f"{FIG}/d1_ssh_idea.png", 15.5, "What SSH does: your typing travels to the Pi; the Pi's text answers travel back.")
    d.step(1, "Open PowerShell", ["Press the Windows key, type `PowerShell`, press Enter.  Windows 10/11 already includes the SSH program. Test it: `ssh -V` should print a version.  If it says 'not recognized', add **OpenSSH Client** in Settings -> Apps -> Optional features."], color="2E8B57")
    d.step(2, "Connect", ["Type the command below (replace `piuser`). The first time, Windows asks if you trust this host - type `yes` and press Enter. Then type your password: **nothing appears while you type - that is normal.**"], color="2E8B57")
    d.code(["ssh piuser@raspi4.local"])
    d.step(3, "Recognise success", ["The prompt changes to `piuser@raspi4:~ $`. This means you are now **inside the Pi**. Every command you type runs on the Pi, not on your laptop."], color="2E8B57")
    u = user_shot("S3")
    d.figure_pair(f"{BOOK}/ssh_first_login.png", u or f"{FIG}/ph_S3_powershell_login.png", 8.1,
                  "The book's first login (macOS). The prompt `user@host:~ $` means you are connected.",
                  "Your PowerShell after a successful login" + ("." if u else " (capture slot)."), BOOKSRC.format(p="38"))
    d.step(4, "Run your first five commands", ["Type each, press Enter, and read the output."], color="2E8B57")
    d.table(["Command", "What it does", "What you should see"], [
        ["`hostname -I`", "Shows the Pi's IP address(es) (book p. 38)", "An address like 192.168.x.x - write it on your card"],
        ["`uname -m`", "Shows the CPU architecture", "`aarch64` = 64-bit. If you see `armv7l`, you installed a 32-bit OS"],
        ["`cat /etc/os-release`", "Names the OS release", "Debian-based Raspberry Pi OS; note the version"],
        ["`python3 --version`", "The Python version", "Note it: we need it on Day 4"],
        ["`free -h`", "Memory", "Total close to 4 GB (a little less)"],
    ], [4.0, 6.0, 7.2], size=9)
    d.step(5, "Shut down properly - every time", ["Never just pull the plug. Run the command below, then wait until the **green LED stops flashing and stays dark**, and only then remove the power (book p. 38).", ], color="2E8B57")
    d.code(["sudo shutdown -h now"])
    d.callout("tip", "The best habit you can form today", ["Always shut down with the command. Pulling the plug while the Pi writes to the card can corrupt the card - the book warns about this."])

    d.h2("Troubleshooting")
    d.table(["What you see", "Most likely cause", "Try this"], [
        ["`Could not resolve hostname raspi4.local`", "Pi not on the network yet, a typo in the Wi-Fi settings, or `.local` blocked", "Wait 5 min. Check Wi-Fi name/password. Try the Pi's IP from your router's device list. Try an Ethernet cable or your phone hotspot."],
        ["`Connection timed out`", "Laptop and Pi on different networks, a VPN, or a guest/office network that isolates devices", "Put both on the same Wi-Fi; turn off VPN; use a phone hotspot."],
        ["`Permission denied, please try again`", "Wrong username or password", "Case matters. Retype slowly. If forgotten, write the card again."],
        ["`REMOTE HOST IDENTIFICATION HAS CHANGED`", "You re-flashed the card; the Pi's identity changed", "Run `ssh-keygen -R raspi4.local`, then connect again."],
        ["Red LED but the green never flickers", "No OS found on the card", "Reseat the card; write it again; try another card."],
        ["Nothing lights up", "No power", "Try another cable/charger (5 V / 3 A)."],
    ], [4.6, 5.6, 7.0], size=9)

    # ------------------------------------------------------------------ extras
    d.h1("Two laptops, one Pi - how to think about it")
    d.p("You work from an office laptop **and** a home laptop. The Pi is the **shared workspace**: your code and models live on the Pi (and in your GitHub repo); each laptop is just a **window** into it. "
        "This works beautifully when the laptop and the Pi share a network, but `raspi4.local` only works **inside one network**.")
    d.figure(f"{FIG}/d1_network.png", 16.2, "Left: how Day 1 works. Right: the problem to solve on Day 2 when the Pi is in one place and the laptop is in another.")
    d.bullets(["**Option 1:** carry the Pi (+ its charger) between office and home, and teach it both Wi-Fi networks (Day 2).",
               "**Option 2:** leave the Pi in one place and reach it from the other with a remote-access service (Day 2 - I will verify the current options before recommending one).",
               "Either way, keep the **connection card** (Appendix A) up to date."])

    d.h1("Check yourself")
    d.p("Answer from memory first; answers are at the end of this page.", after=3)
    qs = ["Image classification belongs to which family of AI in the book: fixed-function or generative?",
          "Why do we enable SSH in Imager __before__ writing the card?",
          "What does a red steady LED mean? A flickering green LED?",
          "What can go wrong if you unplug the Pi without shutting it down?",
          "Why does `ssh piuser@raspi4.local` fail from your home laptop if the Pi is on the office network?",
          "Why does nothing appear while you type your SSH password?",
          "Which command shows the Pi's IP address? Which shows whether the OS is 64-bit?",
          "Give three advantages of running AI at the edge."]
    for i, q in enumerate(qs, 1):
        p = d.d.add_paragraph(); p.paragraph_format.left_indent = Cm(0.7); p.paragraph_format.first_line_indent = Cm(-0.7); para_fmt(p, after=3)
        r = p.add_run(f"{i}.  "); r.bold = True; r.font.color.rgb = rgb(RASP); add_runs(p, q)
    d.callout("note", "Answers", ["1) Fixed-function (reactive).  2) So the Pi comes up configured and reachable with no monitor or keyboard.  3) Power OK; the Pi is reading the SD card.  "
                                  "4) Data loss or a corrupted card.  5) `.local` names only resolve inside one network - the two laptops and the Pi are on different networks.  "
                                  "6) A security feature - the terminal does not echo passwords.  7) `hostname -I`; `uname -m` (aarch64).  "
                                  "8) Low latency, privacy, network independence, lower bandwidth, energy efficiency."], size=9.5)

    d.h1("Teach it to your students")
    d.callout("teach", "A 45-minute lab version", [
        "- **Before class:** each pair gets a Pi, a card, a reader, a charger; Imager pre-installed; hotspot ready as the network.",
        "- **10 min:** the big picture (Part A) with the roadmap figure.  **15 min:** flash (Part C), live on screen.  **10 min:** boot + LEDs.  **10 min:** SSH + five commands.",
        "- **Typical mistakes:** wrong storage device chosen; Wi-Fi typo; SSH not enabled; guest/enterprise network; unplugging without shutdown; re-flashing and then hitting the 'host identification changed' warning.",
        "- **Mini-assessment:** each pair submits a screenshot of `hostname -I`, `uname -m` and `free -h` (with Wi-Fi details hidden).",
    ])

    d.h1("Resources")
    d.table(["Resource", "Where", "Note"], [
        ["Book - Setup chapter", "PDF pp. 29-50 in 'Edge-AI-Engineering book.pdf' (UNIFEI-IESTI05-EDGE_AI repo)", "Online: https://mjrovai.github.io/EdgeML_Made_Ease_ebook/raspi/setup/setup.html (link from the course README)"],
        ["Slides: Class 3 - Raspberry Pi Setup Walkthrough", "00_Curso_Folder/1-Fixed_Function_AI/Class_03/3-Raspberry_Pi-Setup_Walkthrough.pdf", "13 slides: board layout, imager, SSH, first commands, tips"],
        ["Video: Class 3 - Raspberry Pi Setup Walkthrough", "https://youtu.be/YtjsM36LzVE", "Listed in the course README; in Portuguese. I could not open YouTube from my sandbox, so I have not watched it."],
        ["Video: Class 2 - Introduction to Linux", "https://youtu.be/QkIHILtl0h4", "Same note. Good preview for Day 3."],
        ["Video: Class 1 - Course introduction", "https://youtu.be/QAb3MFHwe78", "Same note."],
        ["Raspberry Pi Imager download", "https://www.raspberrypi.com/software/", "Address used in the course slides."],
        ["Animation for today", "tutorials/day01/animations/Day01_flash_boot_ssh.mp4 (silent copy and .gif also there)", "About 70 s with English narration and subtitles (script in animations/narration/): write the card, boot, Wi-Fi, SSH."],
    ], [4.6, 6.9, 5.7], size=8.8)

    d.h1("Appendix A  -  My connection card")
    d.p("Fill this in by hand or on screen. Keep it with the Pi. (Do not write the password here if the page will be shared.)", after=3)
    rows = ["Hostname", "Username", "Password hint (not the password)", "Wi-Fi network 1 (name)", "Wi-Fi network 2 (name)", "IP address (can change)", "OS release (cat /etc/os-release)", "Python version", "Architecture (uname -m)", "microSD size / brand", "Date flashed / notes"]
    t = d.d.add_table(rows=len(rows), cols=2); t.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, k in enumerate(rows):
        a, b = t.rows[i].cells; no_split(t.rows[i]); shade(a, "EEF1F4")
        for c in (a, b): cell_margins(c, 60, 60, 120, 120); borders(c, bottom=(6, "9AA5B1"), top=(6, "9AA5B1") if i == 0 else None, left=(6, "9AA5B1"), right=(6, "9AA5B1"))
        add_runs(a.paragraphs[0], k, size=9.5, bold=True, color=NAVY); para_fmt(a.paragraphs[0], after=0)
    set_col_widths(t, [6.0, CONTENT_W - 6.0]); d.spacer(8)
    d.page_break()
    d.h1("Appendix B  -  My notes and questions")
    t = d.d.add_table(rows=24, cols=1); t.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i in range(24):
        c = t.rows[i].cells[0]; borders(c, bottom=(4, "B8C2CC")); cell_margins(c, 150, 60, 60, 60); para_fmt(c.paragraphs[0], after=0)
    set_col_widths(t, [CONTENT_W])
    d.save(f"{OUT}/Day01_Meet_Your_Raspberry_Pi.docx")

if __name__ == "__main__":
    make_filmstrip()
    build()
    print("built")
