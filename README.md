# 🛰️ ISS Tracker

A desktop GUI application built with **Python** and **Tkinter** that tracks the International Space Station (ISS) in real time, displays its current position on a world map, shows your local time and location, and sends you an **email alert** when the ISS is passing overhead.

---

## Screenshot
![alt text](<Ekran Görüntüsü (959).png>)

## Features

- 🌍 **Live ISS tracking** — displays the ISS's current position on a world map, updated at regular intervals.
- 📍 **Your location & local time** — shows where you are and the current time.
- ✉️ **Overhead email alerts** — automatically sends you an email notification when the ISS is close to your location and it's dark enough to potentially see it.
- 🌙 **Day/night awareness** — uses sunrise/sunset data to determine visibility conditions.

---

## How It Works

1. The app periodically requests the ISS's current latitude/longitude from the **Open Notify API**.
2. It converts those coordinates into pixel coordinates on the world map and updates the ISS icon's position on the canvas.
3. It fetches sunrise/sunset times for your location from the **Sunrise-Sunset API** to determine if it's currently dark.
4. If the ISS is near your coordinates **and** it's nighttime at your location, the app sends you an email via `smtplib` letting you know it's a good time to look up.

---

## Getting Started

### Requirements

- Python 3.x
- `requests` library

Install dependencies:

```bash
pip install requests
```

> `tkinter`, `smtplib`, and `datetime` are part of Python's standard library — no separate installation needed.


---

## APIs Used

| Purpose | API |
|---|---|
| ISS current location | [Open Notify](http://open-notify.org/) |
| Sunrise & sunset times | [Sunrise-Sunset.org](https://sunrise-sunset.org/) |

---

## Assets & Attribution

This project uses the following free icons and map, used under their respective licenses with attribution:

- World map: [World map – Wikipedia](https://en.wikipedia.org/wiki/World_map)
- <a href="https://www.flaticon.com/free-icons/moon" title="moon icons">Moon icons created by Magnific - Flaticon</a>
- <a href="https://www.flaticon.com/free-icons/summer" title="summer icons">Summer icons created by Magnific - Flaticon</a>
- <a href="https://www.flaticon.com/free-icons/satellite" title="satellite icons">Satellite icons created by Magnific - Flaticon</a>

---

## Notes

- Email alerts require a valid sender email account with SMTP access enabled (e.g. an app password if using Gmail).
- Position updates and email-check frequency can be adjusted in the script to balance responsiveness against API rate limits.

---
