"""Builds day01_notes_b.html (notebook-style, stand-alone notes). Reading codes: B-<pdf pages> at the bottom of a page."""
def mn(h=62): return f'<div class="mn" style="height:{h}px"></div>'
def page(n, title, body, reading=None, topic="Day 1: Meet your Raspberry Pi 4"):
    rd = f'<div class="reading">{reading}</div>' if reading else ""
    return f'''<div class="pg"><div class="content">
<div class="top"><div class="t">{topic}</div><div class="p">PAGE {n}</div></div>
<div class="title">{title}</div>
{body}
</div>{rd}<div class="folio">Edge AI study course &middot; Day 01 &middot; figures adapted from Rovai (2025)</div></div>
'''
P = []
# ------------------------------------------------------------------ P1
P.append(("Edge AI &amp; the Raspberry Pi", f'''
<div class="small" style="margin:-2px 0 2px">Reading code at the bottom of a page, e.g. <b>B-20-21</b> = read the Edge AI book, PDF pages 20-21.</div>
<div class="sh b">1. By the end of today I can...</div>
<div class="cols">
 <div class="c1"><ul class="ck">
  <li>explain Edge AI in two sentences</li><li>name the main parts of the Pi 4</li>
  <li>write the OS onto a microSD card with my own settings</li><li>power the Pi, read its 2 LEDs, wait out first boot</li>
  <li>log in over <b>SSH</b> from Windows and shut down safely</li></ul></div>
 <div class="c2"><div class="ybox small"><b>My 2 hours</b>
  <table class="t" style="margin:2px 0"><tr><td><b>A</b> big picture</td><td>20 min</td></tr><tr><td><b>B</b> meet the board</td><td>20 min</td></tr><tr><td><b>C</b> prepare microSD</td><td>45 min</td></tr><tr><td><b>D</b> first boot</td><td>15 min</td></tr><tr><td><b>E</b> first SSH login</td><td>20 min</td></tr></table></div></div>
</div>
{mn(56)}
<div class="sh g">2. What is Edge AI?</div>
<div class="cols">
 <div class="c1"><ul class="bl">
  <li><b>Cloud AI:</b> my data travels to a data centre and the answer travels back.</li>
  <li><b>Edge AI:</b> <span class="hl">the AI algorithm runs locally, on the device next to the data</span> (camera, robot, sensor box, a Pi) - not in the cloud.</li>
  <li>Result: devices that are more <b>responsive, private and efficient</b>.</li>
  <li>Two kinds of AI I will build on the Pi: <b>fixed-function</b> (reactive) and <b>generative</b> (proactive).</li></ul></div>
 <div class="c2"><div data-draw="edge"></div></div>
</div>
{mn(52)}
<div class="sh p">3. Five reasons it matters</div>
<table class="t"><tr><th style="width:27%">Advantage</th><th>What it means in practice</th></tr>
<tr><td>Low latency</td><td>answer in milliseconds, no network round trip (a robot reacts <i>now</i>)</td></tr>
<tr><td>Privacy</td><td>sensitive images / audio stay on the device, not on a remote server</td></tr>
<tr><td>Network independence</td><td>keeps working with no Internet: tunnel, field, factory</td></tr>
<tr><td>Less bandwidth</td><td>send only the useful result, not a whole video stream</td></tr>
<tr><td>Energy efficiency</td><td>optimised models on small hardware use little power</td></tr></table>
<div class="ybox small"><b>In one sentence:</b> Edge AI brings intelligence to where data is generated and decisions are needed.</div>
{mn(56)}
''', "B-20-21, 27"))
# ------------------------------------------------------------------ P2
P.append(("How the course fits together", f'''
<div class="sh b">4. What I will learn (the whole path)</div>
<ol class="st">
 <li><b>Essential setup:</b> get the Pi ready for Edge AI work.</li>
 <li><b>Computer vision:</b> image classification and object detection.</li>
 <li><b>Small language models (SLMs):</b> run and optimise them on the Pi.</li>
 <li><b>Vision-language models:</b> multimodal AI (Florence-2).</li>
 <li><b>Physical computing:</b> connect AI to sensors and actuators.</li>
 <li><b>Advanced optimisation:</b> RAG, agents, function calling.</li></ol>
{mn(52)}
<div class="sh v">5. Two families of AI</div>
<div class="cols">
 <div class="c1 bbox"><b>Fixed-function (reactive)</b><ul class="bl small" style="margin:2px 0"><li>analyses a specific input using predetermined patterns / rules</li><li>acts only when a particular trigger arrives</li><li>consistent, predictable output</li><li>excels at structured tasks: classify, detect, recognise</li><li>works within its boundaries</li></ul><span class="note">my Phase 2: classification, detection, counting</span></div>
 <div class="c2 pbox"><b>Generative (proactive)</b><ul class="bl small" style="margin:2px 0"><li>creates new content: text, descriptions, solutions</li><li>understands context</li><li>keeps a dialogue going</li><li>adapts to new situations beyond its training</li></ul><span class="note">my Phase 3: SLMs, vision-language, agents</span></div>
</div>
<table class="t small"><tr><th style="width:22%"></th><th>Fixed-function</th><th>Generative</th></tr>
<tr><td>Core focus</td><td>data analysis, assessment, automation</td><td>content creation, anticipation, dialogue</td></tr>
<tr><td>Examples</td><td>fraud detection, spam filters, image recognition</td><td>ChatGPT, DALL-E, predictive maintenance, smart assistants</td></tr>
<tr><td>Typical use</td><td>banking, medical diagnostics, security</td><td>content, customer support, design, automation</td></tr></table>
<div class="ybox small"><b>Rule of thumb:</b> fixed-function = efficient, predictable, low resources, well-defined tasks. Generative = creative, personalised, anticipatory.</div>
{mn(52)}
<div class="sh g">6. How each topic is taught, and what I should know</div>
<div class="cols">
 <div class="c1"><b>Every chapter has:</b><ul class="bl small"><li>concepts and theory</li><li>step-by-step implementation</li><li>a practical project with code</li><li>performance optimisation tips</li><li>ideas for further exploration</li></ul></div>
 <div class="c2"><b>Helpful background:</b><ul class="bl small"><li>basic Python</li><li>Linux command-line basics</li><li>elementary machine-learning ideas</li><li>earlier Pi experience (helpful, not required)</li></ul></div>
</div>
{mn(52)}
''', "B-21-23, 25-27"))
# ------------------------------------------------------------------ P3
P.append(("Why the Raspberry Pi?", f'''
<div class="sh y">7. What makes the Pi good for engineers</div>
<div class="cols">
 <div class="c1"><ul class="bl small">
  <li><b>Computational power:</b> multi-core ARM processors, up to 8 GB RAM on the newest models.</li>
  <li><b>GPIO:</b> a 40-pin header to talk directly to sensors and actuators.</li>
  <li><b>Connectivity:</b> Wi-Fi, Bluetooth, Ethernet, several USB ports.</li></ul></div>
 <div class="c2"><ul class="bl small">
  <li><b>Low-level access:</b> I2C, SPI and UART interfaces.</li>
  <li><b>Soft real-time:</b> with proper configuration, usable for control and signal processing.</li>
  <li><b>Power efficiency:</b> low consumption, good for battery-powered designs.</li></ul></div>
</div>
<div class="small">Plus: a full Linux OS, a huge community, and low cost. That combination is why it is a good Edge AI platform.</div>
{mn(40)}
<div class="sh b">8. Pi models compared</div>
<table class="t small"><tr><th style="width:17%"></th><th>Zero 2 W</th><th>Pi 4 (my board)</th><th>Pi 5</th></tr>
<tr><td>CPU</td><td>1 GHz quad-core Cortex-A53 (64-bit)</td><td>quad-core Cortex-A72, 1.5 GHz</td><td>quad-core Cortex-A76, 2.4 GHz</td></tr>
<tr><td>RAM</td><td>512 MB</td><td>4 GB (mine)</td><td>2 / 4 / 8 GB (8 GB best for AI)</td></tr>
<tr><td>Wi-Fi / BT</td><td>2.4 GHz only, BT 4.2</td><td>dual-band, BT 5.0</td><td>dual-band 802.11ac, BT 5.0</td></tr>
<tr><td>Ports</td><td>mini-HDMI, micro-USB OTG, CSI camera</td><td>2 micro-HDMI, 2 USB 3 + 2 USB 2, CSI, DSI</td><td>2 micro-HDMI, 2 USB 3 + 2 USB 2, CSI, DSI, PCIe</td></tr>
<tr><td>Power</td><td>5 V / 2.5 A micro-USB</td><td>5 V / 3 A USB-C</td><td>5 V / 5 A USB-C (27 W)</td></tr>
</table>
<div class="sub">Pi 4 vs Pi 5 - what changes in practice</div>
<table class="t small"><tr><th style="width:22%">Topic</th><th style="width:39%">Pi 4 (mine)</th><th>Pi 5</th></tr>
<tr><td>Speed</td><td>A72, 1.5 GHz</td><td>A76, 2.4 GHz: clearly faster</td></tr>
<tr><td>Power button</td><td>none - plug in = on</td><td>yes</td></tr>
<tr><td>Charger</td><td>5 V / 3 A</td><td>5 V / 5 A (27 W); 3 A limits USB to 600 mA</td></tr>
<tr><td>Cooling</td><td>heatsink / fan case advisable</td><td>hotter, fan connector, active cooler advisable</td></tr>
<tr><td>Camera ports</td><td>1 CSI + 1 DSI (15-pin)</td><td>two 4-lane ports, smaller connector - check cable</td></tr>
<tr><td>OS</td><td>old and new releases</td><td>needs Bookworm or newer</td></tr>
<tr><td>Imager step</td><td>Device = Raspberry Pi 4</td><td>Device = Raspberry Pi 5</td></tr>
<tr><td>Everything else</td><td colspan="2">SSH, commands, updates, shutdown: <b>identical</b></td></tr></table>
<div class="bbox small"><b>For me:</b> vision runs well on the Pi 4. For language models I stay with small ones and expect them slower than on a Pi 5 (more RAM and a faster CPU there).</div>
{mn(40)}
<div class="sh g">9. What I can build with a Pi</div>
<div class="cols">
 <div class="c1"><ul class="bl small"><li><b>Embedded systems</b> design and prototyping</li><li><b>IoT</b> devices (MQTT, CoAP, HTTP/HTTPS)</li><li><b>Control systems</b> (feedback loops, PID, actuators)</li><li><b>Computer vision + AI</b> (OpenCV, TensorFlow Lite)</li></ul></div>
 <div class="c2"><ul class="bl small"><li><b>Data acquisition</b> and logging</li><li><b>Robotics</b> controllers, motion planning</li><li><b>Signal processing</b> and DSP</li><li><b>Network security</b> (VPNs, firewalls, testing)</li></ul></div>
</div>
{mn(44)}
''', "B-29-32"))
# ------------------------------------------------------------------ P4
P.append(("Meet the board", f'''
<div class="sh b">10. Anatomy of the Raspberry Pi 4</div>
<div data-draw="pi"></div>
<table class="t small"><tr><th style="width:24%">Part</th><th style="width:34%">What it does</th><th>Why I care</th></tr>
<tr><td>CPU, 4 cores</td><td>runs the OS + my code</td><td>does the neural-network maths</td></tr>
<tr><td>RAM 4 GB</td><td>working memory</td><td>models must fit in it</td></tr>
<tr><td>microSD</td><td>the "hard disk"</td><td>always shut down first</td></tr>
<tr><td>GPIO, 40 pins</td><td>sensors, LEDs, buttons</td><td>physical computing (Phase 3)</td></tr>
<tr><td>CSI / USB</td><td>camera ports</td><td>vision projects (Day 4)</td></tr></table>
<div class="small">The Pi 5 (not mine) adds a power button and a PCIe connector.</div>
{mn(56)}
<div class="sh y">11. My turn</div>
<ul class="ck"><li>find every part on my real board, take a top-down photo, label it</li><li>hold the board by its edges - no metal table, no wet fingers</li></ul>
{mn(70)}
''', "B-32-33"))
# ------------------------------------------------------------------ P5
P.append(("The operating system", f'''
<div class="sh g">12. What is an operating system (OS)?</div>
<ul class="bl"><li>Software that <b>manages the hardware and the software</b> and gives programs standard services. The layer between hardware and applications.</li></ul>
<div class="cols">
 <div class="c1 gbox"><b>What it does</b><ul class="bl small" style="margin:2px 0"><li><b>Processes:</b> shares CPU time between programs</li><li><b>Memory:</b> gives out and frees RAM</li><li><b>Files:</b> organises files and folders</li><li><b>Devices:</b> talks to connected hardware</li><li><b>User interface:</b> lets me use the computer</li></ul></div>
 <div class="c2 bbox"><b>What it is made of</b><ul class="bl small" style="margin:2px 0"><li><b>Kernel:</b> the core, controls the hardware</li><li><b>Shell:</b> where I type commands</li><li><b>File system:</b> how data is stored</li><li><b>Drivers:</b> let the OS talk to devices</li></ul></div>
</div>
{mn(52)}
<div class="sh p">13. Raspberry Pi OS</div>
<ul class="bl"><li>A version of <b>Linux (Debian)</b> made for the Pi's ARM processor and limited resources. Formerly called Raspbian.</li>
<li><b>Lightweight</b>, <b>versatile</b> (many languages), <b>open source</b>, supports <b>GPIO</b>, regularly updated.</li>
<li>Standard Linux tools and libraries work, so it is a full computer in a small package: IoT devices up to edge machine-learning projects.</li></ul>
<div class="bbox small"><b>Version note:</b> the course text was written on Debian 12 "Bookworm". A newer Imager may offer a newer Debian. The steps are the same, but the <b>Python version</b> can differ, and TensorFlow Lite is picky - I record it today and check on Day 4-5.</div>
{mn(52)}
<div class="sh y">14. Which OS image do I choose?</div>
<table class="t"><tr><th style="width:30%">Choice in Imager</th><th>What it is</th><th style="width:18%">Mine?</th></tr>
<tr><td><b>Raspberry Pi OS (64-bit)</b></td><td>full system <b>with desktop</b>; 64-bit is needed by many AI libraries</td><td class="green"><b>YES</b></td></tr>
<tr><td>Raspberry Pi OS Lite (64-bit)</td><td>no desktop, saves RAM (used on tiny boards like the Zero)</td><td>not today</td></tr>
<tr><td>32-bit versions</td><td>older, less compatible</td><td class="red">avoid</td></tr></table>
{mn(56)}
''', "B-34-35"))
# ------------------------------------------------------------------ P6
P.append(("Prepare the microSD card", f'''
<div class="sh g">15. The idea</div>
<ul class="bl"><li>By default a Pi looks for an operating system on the <b>microSD card</b> in its slot. It has <b>no hard disk</b>.</li>
<li>"Installing the OS" = writing an <span class="hl">image</span> onto the card with <b>Raspberry Pi Imager</b> (Windows, macOS, Linux).</li>
<li>Imager also pre-sets my <b>credentials and remote-access settings</b>: no monitor or keyboard needed = <b>headless</b>.</li></ul>
<div data-draw="flow"></div>
{mn(52)}
<div class="sh b">16. Before I start</div>
<ul class="ck"><li>Raspberry Pi Imager installed (raspberrypi.com/software)</li><li>microSD card, 32 GB recommended, in a reader</li><li>Wi-Fi name + password ready</li><li>card backed up - Imager <b>erases</b> it</li><li>other USB drives unplugged (so I cannot pick them by mistake)</li></ul>
{mn(52)}
<div class="sh y">17. Steps on Windows</div>
<div class="cols">
 <div class="c1"><ol class="st small">
  <li>Open Imager. If Windows says "format the disk?" -&gt; <b class="red">Cancel</b>.</li>
  <li>Device = <code>Raspberry Pi 4</code> (Pi 5: <code>Raspberry Pi 5</code>)</li>
  <li>OS = <code>Raspberry Pi OS (64-bit)</code></li>
  <li>Storage = my card (check size + drive letter!)</li>
  <li>Next -&gt; open the settings (gear icon / "customise")</li>
  <li>Write -&gt; verify -&gt; "Write successful" -&gt; remove card</li></ol></div>
 <div class="c2" style="text-align:center"><div class="fig"><img src="../../_assets/book/imager_step2.png" width="228"></div><div class="cap">Imager with device, OS and storage chosen (example on a Mac, older release)</div></div>
</div>
{mn(56)}
''', "B-35-36"))
# ------------------------------------------------------------------ P7
P.append(("Settings &amp; first boot", f'''
<div class="sh g">18. Settings I type (very important)</div>
<table class="t"><tr><th style="width:26%">Setting</th><th>What to enter</th></tr>
<tr><td>hostname</td><td><code>raspi4</code> (for my two Pis: <code>raspi-office</code> / <code>raspi-home</code>)</td></tr>
<tr><td>user + password</td><td><code>piuser</code> + a strong password - write it on my connection card</td></tr>
<tr><td>Wi-Fi</td><td>name + password exactly as spelled, country <code>KW</code></td></tr>
<tr><td>zone / keyboard</td><td><code>Asia/Kuwait</code>, <code>us</code></td></tr>
<tr><td><b class="red">SSH</b></td><td><b class="red">ENABLE, password authentication</b> (Services tab) - without it I cannot log in remotely</td></tr></table>
<div class="cols">
 <div class="c1"><div class="pbox small"><b class="red">Careful!</b> Imager erases whatever drive I choose. Wrong drive = lost data.</div>
  <div class="bbox small"><b>Office Wi-Fi</b> may need a login or block devices. Plan B: phone hotspot or an Ethernet cable. Imager stores one Wi-Fi network only; I add the second one on Day 2.</div></div>
 <div class="c2" style="text-align:center"><div class="fig"><img src="../../_assets/book/imager_customisation.png" width="335"></div><div class="cap">settings screens: General (left), Services (right)</div></div>
</div>
{mn(56)}
<div class="sh y">19. First boot (15 min)</div>
<div class="cols">
 <div class="c1"><ol class="st small">
  <li>Card into the slot on the <b>underside</b> (contacts toward the board).</li>
  <li>Optional monitor / keyboard first.</li>
  <li>Power <b>last</b> (USB-C, 5 V / 3 A). The Pi 4 has <b>no power button</b> (Pi 5: use the 27 W supply; it has one).</li>
  <li>Wait a few minutes; it may restart once. <b class="red">Do not unplug!</b></li></ol></div>
 <div class="c2"><div data-draw="leds"></div><div class="small">first boot: resizes the file system, applies my settings, starts SSH (1-3 min)</div></div>
</div>
<div class="pbox small"><b>If something is off:</b> nothing lights up = power; red only, green never flickers = no OS found, reseat or re-flash; random restarts = weak charger.</div>
{mn(60)}
''', "B-36-37"))
# ------------------------------------------------------------------ P8
P.append(("First SSH login", f'''
<div class="sh g">20. Logging in from Windows (20 min)</div>
<ul class="bl"><li><b>SSH</b> = Secure SHell: the Pi's command line in a window on my laptop, over Wi-Fi, encrypted. Both machines on the <b>same network</b>.</li>
<li>Windows tools: PowerShell or Command Prompt (older option: PuTTY). Mac/Linux: Terminal.</li>
<li>I can use the IP address (<code>ssh piuser@192.168.x.x</code>) or the name (<code>ssh piuser@raspi4.local</code>).</li></ul>
<div class="cols">
 <div class="c1"><ol class="st small">
  <li>Start -&gt; <b>PowerShell</b>. Test: <code>ssh -V</code></li>
  <li>Connect (below). First time: type <code>yes</code>.</li>
  <li>Password: <b>nothing shows</b> as I type - normal!</li>
  <li>Prompt <code>piuser@raspi4:~ $</code> = I am <b>inside the Pi</b>.</li></ol></div>
 <div class="c2" style="text-align:center"><div class="fig"><img src="../../_assets/book/ssh_first_login.png" width="250"></div><div class="cap">first login (example on a Mac)</div></div>
</div>
<div class="term"><span class="dim">PS C:\\&gt;</span> ssh piuser@raspi4.local<br><span class="dim">Are you sure you want to continue connecting (yes/no)?</span> yes<br>password: <span class="dim">(invisible)</span><br><span class="g2">piuser@raspi4:~ $</span> _</div>
{mn(56)}
<div class="sh b">21. First commands, updates, shutdown</div>
<table class="t small"><tr><th style="width:34%">Command</th><th>What it does / what I should see</th></tr>
<tr><td><code>hostname -I</code></td><td>the Pi's IP address - write it down</td></tr>
<tr><td><code>uname -m</code></td><td>want <b>aarch64</b> (= 64-bit); <code>armv7l</code> means 32-bit</td></tr>
<tr><td><code>cat /etc/os-release</code></td><td>OS version - note it</td></tr>
<tr><td><code>python3 --version</code></td><td>needed on Day 4 (TFLite is picky)</td></tr>
<tr><td><code>free -h</code></td><td>memory: close to 4 GB</td></tr>
<tr><td><code>sudo apt-get update</code><br><code>sudo apt upgrade</code></td><td>update the package list, then the system - do it regularly</td></tr></table>
<div class="fbox"><b class="red">ALWAYS shut down properly:</b> &nbsp;<code>sudo shutdown -h now</code><br>The Pi may still be writing to the card. Wait until the <b>LED stops blinking and goes dark</b>, then unplug. Pulling the plug can lose data or corrupt the card.<br>Start again: <b>Pi 4</b> unplug + replug; <b>Pi 5</b> press the power button.</div>
<div class="small">Moving files between laptop and Pi: pen drive, <code>scp</code> in the terminal, or an FTP/SFTP program (Day 2).</div>
{mn(56)}
''', "B-38-39"))
# ------------------------------------------------------------------ P9
P.append(("Troubleshooting &amp; two Pis", f'''
<div class="sh p">22. When it does not work</div>
<table class="t small"><tr><th style="width:30%">I see</th><th style="width:32%">probably</th><th>try</th></tr>
<tr><td><code>Could not resolve hostname</code></td><td>Pi not on the network yet, Wi-Fi typo, <code>.local</code> blocked</td><td>wait 5 min, check Wi-Fi, use the IP, Ethernet / hotspot</td></tr>
<tr><td><code>Connection timed out</code></td><td>different networks, VPN, guest Wi-Fi</td><td>same Wi-Fi, VPN off</td></tr>
<tr><td><code>Permission denied</code></td><td>wrong user or password</td><td>retype (case!) or re-flash</td></tr>
<tr><td><code>HOST IDENTIFICATION HAS CHANGED</code></td><td>I re-flashed the card</td><td><code>ssh-keygen -R raspi4.local</code></td></tr>
<tr><td>red LED, green never flickers</td><td>no OS found on the card</td><td>reseat, re-flash, other card</td></tr>
<tr><td>no LEDs at all</td><td>no power</td><td>other cable / charger (5 V / 3 A)</td></tr></table>
{mn(96)}
<div class="sh v">23. Two Pis, two laptops</div>
<ul class="bl small"><li>Office laptop + home laptop = two <b>windows</b> into a Pi. Code and notes live on the Pi and in my GitHub repo. <code>raspi4.local</code> only works <span class="hl">inside one network</span>.</li></ul>
<div data-draw="net"></div>
<ul class="bl small"><li><b>Pass 1:</b> learn on one Pi (about 2 hours). <b>Pass 2:</b> repeat on the other Pi from my notes only.</li>
<li>Different host names (<code>raspi-office</code>, <code>raspi-home</code>), same user, <code>git pull</code> everywhere.</li></ul>
{mn(70)}
''', None))
# ------------------------------------------------------------------ P10
P.append(("Quiz &amp; wrap-up", f'''
<div class="sh y">24. Quick quiz (answer here first!)</div>
<ol class="st small">
<li>What is the difference between cloud AI and Edge AI?</li>
<li>Name three advantages of running AI at the edge.</li>
<li>Image classification: fixed-function or generative? Give one example of the other kind.</li>
<li>Name three things an operating system manages.</li>
<li>Why enable SSH in Imager <i>before</i> writing the card?</li>
<li>Red LED steady = ? Green LED flickering = ?</li>
<li>What can go wrong if I unplug the Pi without shutting it down?</li>
<li>Which command shows the IP address? Which shows whether the OS is 64-bit?</li></ol>
{mn(120)}
<div class="sh b">25. My connection card</div>
<table class="t small"><tr><td style="width:38%">hostname</td><td>&nbsp;</td></tr><tr><td>user name</td><td>&nbsp;</td></tr><tr><td>password hint (not the password!)</td><td>&nbsp;</td></tr>
<tr><td>Wi-Fi 1 / Wi-Fi 2</td><td>&nbsp;</td></tr><tr><td>IP address (it can change)</td><td>&nbsp;</td></tr>
<tr><td>OS release / Python version</td><td>&nbsp;</td></tr><tr><td>uname -m / microSD size</td><td>&nbsp;</td></tr><tr><td>date flashed</td><td>&nbsp;</td></tr></table>
{mn(46)}
<div class="sh g">26. Day 1 is done when...</div>
<ul class="ck small"><li>the Pi boots: red LED steady, green flickers</li><li>PowerShell shows <code>piuser@raspi4:~ $</code></li>
<li>all commands ran and I wrote down OS + Python</li><li>I shut down with <code>sudo shutdown -h now</code></li><li>the connection card is filled in</li></ul>
{mn(46)}
<div class="note">Tomorrow, Day 2: remote access like a pro (files, remote desktop, two networks).</div>
''', None))
pages = "".join(page(i + 1, t, b, r) for i, (t, b, r) in enumerate(P))
html = f'''<!doctype html><html><head><meta charset="utf-8"><title>Day 01 - notebook-style notes</title>
<link rel="stylesheet" href="notes_b.css"><script src="notes_b.js"></script></head><body>
{pages}
</body></html>'''
open("day01_notes_b.html", "w").write(html)
print("pages:", len(P))
