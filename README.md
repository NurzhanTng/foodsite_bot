<p align="center">
  <img src="public/assets/images/banner.png" alt="banner" />
</p>

# 🍽️ RESTOLAND — Telegram Bot for Restaurant Ordering & Loyalty System

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Aiogram](https://img.shields.io/badge/Aiogram-00A5E0?style=for-the-badge)
![Aiohttp](https://img.shields.io/badge/Aiohttp-005571?style=for-the-badge)
![GeoPy](https://img.shields.io/badge/GeoPy-c7aAaB?style=for-the-badge&logo=OpenStreetMap&logoColor=white)
![Websockets](https://img.shields.io/badge/Websockets-333333?style=for-the-badge)
![APScheduler](https://img.shields.io/badge/APScheduler-FFB300?style=for-the-badge)

**RESTOLAND** is a powerful and user-friendly Telegram bot tailored for restaurant businesses. It enables customers to explore menus, place orders, choose delivery or pickup, pay within the chat, and track orders — all from one seamless Telegram interface.

It also includes a **loyalty system**, **promotional campaigns**, **broadcast messaging**, and **detailed analytics**, making it a complete digital solution for modern restaurant chains.

## 🍕 Features

- **Multi-location Support**: Customers can select a specific restaurant branch for delivery or pickup.
- **Menu & Ordering**: Intuitive inline navigation through the menu and order flow.
- **Payment Integration**: Supports in-bot payments for fast and secure transactions.
- **Order Tracking**: Real-time updates and notifications for every order.
- **Loyalty System**: Points accumulation, promotional codes, and discounts.
- **Broadcast & Campaigns**: Create and schedule messages with rich segmentation.
- **Analytics Dashboard**: Get insights on orders, user behavior, and campaign performance.
- **Geolocation Support**: Automatically detect the user's location and suggest nearby restaurants.

## ⚙️ Tech Stack

- **Telegram Bot Framework**: [`aiogram`](https://github.com/aiogram/aiogram) 3.x
- **Asynchronous Networking**: `aiohttp`, `websockets`
- **Geolocation Services**: `geopy`
- **Task Scheduling**: `apscheduler` for reminders, campaigns, and timed actions
- **Security**: `cryptography` for secure payment links and data protection
- **Environment Config**: `environs` for managing secrets and environment variables

## 🚀 Getting Started

1. Clone the repository:
   ```bash
   git clone https://github.com/NurzhanTng/foodsite_bot.git
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Add your bot token and configuration to `.env`:
   ```env
    BOT_TOKEN=your_token
    API_PATH=your_server
    SITE_PATH=path_to_bots_website
    PAYMENTS_TOKEN=payment_system_token
    WS_PATH=your_server_events_path
   ```

4. Run the bot:
   ```bash
   python main.py
   ```

## 📸 Screenshots

_Showcasing a seamless restaurant ordering experience in Telegram._

<p align="center">
    <img src="public/assets/images/menu.jpg" alt="Menu Preview" width="400" />
</p>
<p align="center"><i>Menu navigation</i></p>

<p align="center"> 
    <img src="public/assets/images/tracking.jpg" alt="Order Tracking" width="400" /> 
</p>
<p align="center"><i>Live order status updates</i></p>

<p align="center">
     <img src="public/assets/images/promo.jpg" alt="Promotions" width="400" /> 
</p>
<p align="center"><i>Loyalty promotions and offers</i></p>

## 📎 Links

- [Русская версия README.md](./README.ru.md)

---

**RESTOLAND** is open-source and ready to scale. Contributions, feature requests, and feedback are welcome — let’s make restaurant experiences smoother and smarter together!
