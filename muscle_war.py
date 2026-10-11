#!/usr/bin/env python3
"""
Muscle War website - run as a Python program.

Usage:
    python muscle_war.py            # serves on http://localhost:8000 and opens your browser
    python muscle_war.py 9000       # use a different port

Needs only the Python standard library (3.7+). Press Ctrl+C to stop.
Optional images (hero.jpg, trainer1.jpg, trainer2.jpg, trainer3.jpg) are served
if you place them in the same folder as this file.
"""
import sys
import threading
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Muscle War — Build Your Stronger Self</title>
<meta name="description" content="Premium gym with modern equipment, expert trainers, group classes and flexible memberships.">
<style>
:root{--bg:#0b0b0c;--card:#161618;--text:#f3f3f3;--muted:#a0a0a8;--accent:#ff3b1f;--line:#2a2a2e}
*{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth}
body{font-family:'Segoe UI',Arial,sans-serif;background:var(--bg);color:var(--text);line-height:1.6}
a{color:inherit;text-decoration:none}
section{padding:80px 6%;max-width:1200px;margin:auto}
h1,h2,h3{text-transform:uppercase;letter-spacing:.5px}
h2{font-size:2.2rem;margin:6px 0 10px}
.label{color:var(--accent);font-weight:700;font-size:.85rem;text-transform:uppercase;letter-spacing:2px}
.sub{color:var(--muted);margin-bottom:34px}
.btn{display:inline-block;background:var(--accent);color:#fff;padding:12px 26px;border:0;border-radius:6px;font-weight:700;cursor:pointer;font-size:1rem}
.btn.ghost{background:transparent;border:2px solid #fff}
.grid{display:grid;gap:20px;grid-template-columns:repeat(auto-fit,minmax(230px,1fr))}
.card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:24px}
.card p{color:var(--muted);margin-top:6px}

/* NAV */
nav{position:sticky;top:0;z-index:10;background:rgba(11,11,12,.95);display:flex;justify-content:space-between;align-items:center;padding:14px 6%;border-bottom:1px solid var(--line);flex-wrap:wrap;gap:10px}
.logo{font-weight:900;font-size:1.3rem;letter-spacing:2px}
.logo span{color:var(--accent)}
nav ul{display:flex;gap:18px;list-style:none;flex-wrap:wrap}
nav a{text-transform:capitalize;color:var(--muted);font-size:.95rem}
nav a:hover{color:#fff}

/* HERO */
#home{max-width:none;min-height:88vh;display:flex;flex-direction:column;justify-content:center;
background:linear-gradient(90deg,rgba(0,0,0,.85),rgba(0,0,0,.35)),url('hero.jpg') center/cover,#222}
#home h1{font-size:clamp(2.5rem,7vw,5rem);max-width:700px;line-height:1.05}
#home p{margin:16px 0 28px;font-size:1.2rem;color:#ddd}
#home .btns{display:flex;gap:14px;flex-wrap:wrap}

/* PLANS */
.plan{position:relative;text-align:center}
.plan .price{font-size:2.2rem;font-weight:800;color:var(--accent);margin:10px 0}
.plan ul{list-style:none;margin:14px 0 20px;text-align:left}
.plan li{padding:5px 0;border-bottom:1px solid var(--line);color:var(--muted)}
.plan li::before{content:"✓ ";color:var(--accent)}
.plan.popular{border-color:var(--accent)}
.badge{position:absolute;top:-12px;left:50%;transform:translateX(-50%);background:var(--accent);padding:3px 14px;border-radius:20px;font-size:.75rem;font-weight:700}

/* FORMS */
form{display:grid;gap:14px;max-width:560px}
label{font-size:.9rem;color:var(--muted);display:grid;gap:6px}
input,select{padding:12px;border-radius:6px;border:1px solid var(--line);background:#0f0f11;color:#fff;font-size:1rem;width:100%}
.row{display:grid;grid-template-columns:1fr 1fr;gap:14px}
.seg{display:flex;gap:10px}
.seg label{flex:1;display:block}
.seg input{display:none}
.seg span{display:block;text-align:center;padding:11px;border:1px solid var(--line);border-radius:6px;cursor:pointer;text-transform:capitalize}
.seg input:checked+span{background:var(--accent);border-color:var(--accent);color:#fff}
#result{margin-top:24px;max-width:560px;display:none;border-left:4px solid var(--accent)}
#result h3{margin-bottom:10px}
#result li{margin-left:18px;color:#ddd}
.warn{color:#ffb020;font-size:.85rem;margin-top:10px}

/* TRAINERS */
.trainer img{width:100%;height:240px;object-fit:cover;border-radius:8px;background:#222;margin-bottom:12px}

/* SCHEDULE */
.tbl{overflow-x:auto}
table{width:100%;border-collapse:collapse;min-width:620px}
th,td{padding:12px;border:1px solid var(--line);text-align:center}
th{background:var(--card);color:var(--accent)}

/* CONTACT */
.contact{display:grid;gap:40px;grid-template-columns:repeat(auto-fit,minmax(280px,1fr))}
footer{text-align:center;padding:26px;color:var(--muted);border-top:1px solid var(--line)}
</style>
</head>
<body>

<nav>
  <a href="#home" class="logo">MUSCLE <span>WAR</span></a>
  <ul>
    <li><a href="#home">home</a></li>
    <li><a href="#about">about</a></li>
    <li><a href="#facilities">facilities</a></li>
    <li><a href="#membership">membership</a></li>
    <li><a href="#calculator">calculator</a></li>
    <li><a href="#trainers">trainers</a></li>
    <li><a href="#schedule">schedule</a></li>
    <li><a href="#contact">contact</a></li>
  </ul>
</nav>

<section id="home">
  <h1>Build Your Stronger Self.</h1>
  <p>Your goals. Your discipline. Your transformation.</p>
  <div class="btns">
    <a class="btn" href="#membership">Explore Memberships</a>
    <a class="btn ghost" href="#contact">Contact Us</a>
  </div>
</section>

<section id="about">
  <div class="label">About Us</div>
  <h2>Discipline. Built Daily.</h2>
  <p class="sub">Muscle War is built for people who show up. Our philosophy is simple: consistent effort, smart training and a community that pushes you further than you'd go alone. Whether you're picking up your first dumbbell or chasing a new PR, we give you the tools and support to get there.</p>
  <div class="grid">
    <div class="card"><h3>Modern Equipment</h3><p>Premium machines and free weights, maintained to the highest standard.</p></div>
    <div class="card"><h3>Supportive Trainers</h3><p>Certified coaches who guide, correct and motivate.</p></div>
    <div class="card"><h3>Motivating Environment</h3><p>High energy, zero judgement — a space built to perform.</p></div>
  </div>
</section>

<section id="facilities">
  <div class="label">Facilities</div>
  <h2>Everything You Need</h2>
  <div class="grid" style="margin-top:30px">
    <div class="card"><h3>Weight Training</h3><p>Free weights, racks and plate-loaded machines for every lift.</p></div>
    <div class="card"><h3>Cardio Equipment</h3><p>Treadmills, bikes, rowers and climbers to build your engine.</p></div>
    <div class="card"><h3>Personal Training</h3><p>One-on-one coaching tailored to your goals.</p></div>
    <div class="card"><h3>Strength &amp; Conditioning</h3><p>Athletic programming for power, speed and endurance.</p></div>
    <div class="card"><h3>Group Fitness</h3><p>High-energy classes that keep you accountable.</p></div>
  </div>
</section>

<section id="membership">
  <div class="label">Membership Plans</div>
  <h2>Choose Your Plan</h2>
  <div class="grid" style="margin-top:34px" id="plans"></div>
</section>

<section id="calculator">
  <div class="label">Goal Calculator</div>
  <h2>Plan Your Target</h2>
  <p class="sub">Enter your details and pick a timeframe to see how much to lose or gain.</p>
  <form id="calcForm">
    <div class="row">
      <label>Height (cm)<input type="number" id="height" min="100" max="250" required></label>
      <label>Weight (kg)<input type="number" id="weight" min="30" max="300" step="0.1" required></label>
    </div>
    <div class="row">
      <label>Age<input type="number" id="age" min="14" max="90" required></label>
      <div>
        <label style="margin-bottom:6px">Sex</label>
        <div class="seg">
          <label><input type="radio" name="sex" value="male" checked><span>male</span></label>
          <label><input type="radio" name="sex" value="female"><span>female</span></label>
        </div>
      </div>
    </div>
    <label>Activity level
      <select id="activity">
        <option value="1.2">Little or no exercise</option>
        <option value="1.375" selected>Light (1-3 days/week)</option>
        <option value="1.55">Moderate (3-5 days/week)</option>
        <option value="1.725">Heavy (6-7 days/week)</option>
      </select>
    </label>
    <label>Target weight in kg (optional)<input type="number" id="target" step="0.1"></label>
    <div>
      <label style="margin-bottom:6px">Plan length</label>
      <div class="seg">
        <label><input type="radio" name="months" value="3" checked><span>3 months</span></label>
        <label><input type="radio" name="months" value="6"><span>6 months</span></label>
        <label><input type="radio" name="months" value="12"><span>12 months</span></label>
      </div>
    </div>
    <button class="btn" type="submit">Calculate</button>
  </form>
  <div class="card" id="result"></div>
</section>

<section id="trainers">
  <div class="label">Trainers</div>
  <h2>Meet The Coaches</h2>
  <p class="sub">Names and qualifications are placeholders until real information is provided.</p>
  <div class="grid" id="trainerGrid"></div>
</section>

<section id="schedule">
  <div class="label">Workout Schedule</div>
  <h2>Weekly Classes</h2>
  <p class="sub">Sample timings — subject to change.</p>
  <div class="tbl">
    <table>
      <thead><tr><th>Time</th><th>Mon</th><th>Tue</th><th>Wed</th><th>Thu</th><th>Fri</th><th>Sat</th></tr></thead>
      <tbody>
        <tr><td>6:00 AM</td><td>HIIT</td><td>Strength</td><td>HIIT</td><td>Strength</td><td>HIIT</td><td>Bootcamp</td></tr>
        <tr><td>8:00 AM</td><td>Yoga</td><td>Cardio Blast</td><td>Yoga</td><td>Cardio Blast</td><td>Yoga</td><td>—</td></tr>
        <tr><td>6:00 PM</td><td>Strength</td><td>Zumba</td><td>Strength</td><td>Zumba</td><td>Functional</td><td>—</td></tr>
        <tr><td>8:00 PM</td><td>Core</td><td>Boxing</td><td>Core</td><td>Boxing</td><td>Core</td><td>—</td></tr>
      </tbody>
    </table>
  </div>
</section>

<section id="contact">
  <div class="label">Contact</div>
  <h2>Start Today</h2>
  <div class="contact" style="margin-top:30px">
    <div>
      <p>Bharathi Salai, Andavar Nagar, Ramapuram, Chennai, Tamil Nadu 600089</p><br>
      <p>Mon – Sat: 5:00 AM – 11:00 PM</p>
      <p>Sunday: 7:00 AM – 1:00 PM</p><br>
      <p>099411 70909</p><br>
      <a class="btn" target="_blank" rel="noopener"
         href="https://wa.me/919941170909?text=Hi%20Muscle%20War!%20I'd%20like%20to%20know%20more%20about%20your%20memberships.">Enquire on WhatsApp</a>
    </div>
    <div>
      <h3 style="margin-bottom:14px">Membership Enquiry</h3>
      <form id="enquiryForm">
        <label>Full name *<input id="eName" required></label>
        <label>Phone number *<input id="ePhone" type="tel" required></label>
        <label>Membership plan *
          <select id="ePlan" required>
            <option value="">Select a plan</option>
            <option>1 Month — ₹700</option>
            <option>3 Months — ₹2,000</option>
            <option>6 Months — ₹4,000</option>
            <option>12 Months — ₹8,000</option>
          </select>
        </label>
        <button class="btn" type="submit">Send Enquiry via WhatsApp</button>
      </form>
    </div>
  </div>
</section>

<footer>© 2026 Muscle War. All rights reserved.</footer>

<script>
/* ---------- Membership plans ---------- */
const plans = [
  {name:"1 Month", tag:"Get started", price:"₹700", feats:["Full gym floor access","Cardio zone","Locker room access"]},
  {name:"3 Months", tag:"Build the habit", price:"₹2,000", feats:["Full gym floor access","Cardio zone","Locker room access","Fitness assessment"]},
  {name:"6 Months", tag:"Most popular", price:"₹4,000", popular:true, feats:["Full gym floor access","Cardio zone","Locker room access","Progress reviews"]},
  {name:"12 Months", tag:"Best value", price:"₹8,000", feats:["Full gym floor access","Cardio zone","Locker room access","Progress reviews","Diet guidance"]}
];
document.getElementById("plans").innerHTML = plans.map(p => `
  <div class="card plan ${p.popular ? "popular" : ""}">
    ${p.popular ? '<span class="badge">Most Popular</span>' : ""}
    <h3>${p.name}</h3>
    <p>${p.tag}</p>
    <div class="price">${p.price}</div>
    <ul>${p.feats.map(f => `<li>${f}</li>`).join("")}</ul>
    <a class="btn" href="#contact">Join Now</a>
  </div>`).join("");

/* ---------- Trainers ---------- */
const trainers = [
  ["Trainer Name 1","Strength & Powerlifting","trainer1.jpg"],
  ["Trainer Name 2","Functional Fitness & Mobility","trainer2.jpg"],
  ["Trainer Name 3","HIIT & Conditioning","trainer3.jpg"]
];
document.getElementById("trainerGrid").innerHTML = trainers.map(t => `
  <div class="card trainer">
    <img src="${t[2]}" alt="${t[1]}">
    <h3>${t[0]}</h3>
    <p>${t[1]}</p>
    <p>Qualification: Placeholder</p>
  </div>`).join("");

/* ---------- Goal calculator ---------- */
document.getElementById("calcForm").addEventListener("submit", e => {
  e.preventDefault();
  const h = +document.getElementById("height").value;
  const w = +document.getElementById("weight").value;
  const age = +document.getElementById("age").value;
  const sex = document.querySelector('input[name="sex"]:checked').value;
  const act = +document.getElementById("activity").value;
  const tVal = document.getElementById("target").value;
  const months = +document.querySelector('input[name="months"]:checked').value;

  // Mifflin-St Jeor BMR and daily maintenance calories
  const bmr = 10*w + 6.25*h - 5*age + (sex === "male" ? 5 : -161);
  const tdee = Math.round(bmr * act);

  // BMI and healthy range (BMI 18.5 – 24.9)
  const hm = h/100;
  const bmi = w/(hm*hm);
  const minHealthy = 18.5*hm*hm, maxHealthy = 24.9*hm*hm;

  // Goal weight: user's target, otherwise nearest healthy weight
  let target;
  if (tVal) target = +tVal;
  else if (w > maxHealthy) target = maxHealthy;
  else if (w < minHealthy) target = minHealthy;
  else target = w;

  let diff = target - w;
  // Safe pace cap: about 0.5 kg per week (~2 kg/month)
  const maxChange = 2 * months;
  let capped = false;
  if (Math.abs(diff) > maxChange) { diff = Math.sign(diff) * maxChange; capped = true; }

  const achievable = w + diff;
  const perWeek = Math.abs(diff) / (months * 4.345);
  const dailyDelta = Math.round(Math.abs(diff) * 7700 / (months * 30.4));
  const goal = diff < -0.05 ? "lose" : diff > 0.05 ? "gain" : "maintain";
  const calories = goal === "lose" ? tdee - dailyDelta : goal === "gain" ? tdee + dailyDelta : tdee;

  const box = document.getElementById("result");
  box.style.display = "block";
  box.innerHTML = `
    <h3>Your ${months}-month plan</h3>
    <ul>
      <li>BMI: <b>${bmi.toFixed(1)}</b> (healthy range ${minHealthy.toFixed(1)}–${maxHealthy.toFixed(1)} kg)</li>
      <li>Maintenance calories: <b>${tdee} kcal/day</b></li>
      <li>Goal: <b>${goal === "maintain" ? "Maintain your weight" : goal + " " + Math.abs(diff).toFixed(1) + " kg"}</b></li>
      <li>Target weight in ${months} months: <b>${achievable.toFixed(1)} kg</b></li>
      <li>Pace: <b>${perWeek.toFixed(2)} kg/week</b></li>
      <li>Daily calories to aim for: <b>${Math.max(calories, sex === "male" ? 1500 : 1200)} kcal</b></li>
    </ul>
    ${capped ? '<p class="warn">Your target was adjusted to a safe pace. Choose a longer plan to reach it.</p>' : ""}
    <p class="warn">Estimates only — consult a doctor or trainer before major diet changes.</p>`;
});

/* ---------- WhatsApp enquiry ---------- */
document.getElementById("enquiryForm").addEventListener("submit", e => {
  e.preventDefault();
  const msg = `Hi Muscle War! My name is ${eName.value}. Phone: ${ePhone.value}. I'm interested in the ${ePlan.value} plan.`;
  window.open("https://wa.me/919941170909?text=" + encodeURIComponent(msg), "_blank");
});
</script>
</body>
</html>
"""

BASE_DIR = Path(__file__).resolve().parent
IMAGE_TYPES = {".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png",
               ".webp": "image/webp", ".gif": "image/gif", ".svg": "image/svg+xml"}


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = self.path.split("?")[0]
        if path in ("/", "/index.html"):
            return self._send(200, "text/html; charset=utf-8", HTML.encode("utf-8"))
        file = (BASE_DIR / path.lstrip("/")).resolve()
        ctype = IMAGE_TYPES.get(file.suffix.lower())
        if ctype and file.parent == BASE_DIR and file.is_file():
            return self._send(200, ctype, file.read_bytes())
        self._send(404, "text/plain; charset=utf-8", b"Not found")

    def _send(self, code, ctype, body):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):
        pass


def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    server = HTTPServer(("127.0.0.1", port), Handler)
    url = f"http://localhost:{port}"
    print(f"Muscle War running at {url}  (Ctrl+C to stop)")
    threading.Timer(0.8, lambda: webbrowser.open(url)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
