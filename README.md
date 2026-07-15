# Galaeros – Community‑Powered Transit Navigation for the Philippines

**Every commuter a cartographer. Every journey a building block.**

[![License: AGPL v3](https://img.shields.io/badge/License-AGPL_v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)
[![Data License: ODbL](https://img.shields.io/badge/Data%20License-ODbL-brightgreen.svg)](DATA_LICENSE)

Galaeros is a community‑driven platform that maps the entire Philippine public transport system – from jeepneys and tricycles to ferries and buses. The app combines crowdsourced contributions, AI verification, and a rewarding gamification system to provide accurate, real‑time transit information, even in areas that are invisible to existing map services.

---

## 📚 Table of Contents

- [Vision & Mission](#vision--mission)
- [Why Galaeros?](#why-galaeros)
- [Core Features](#core-features)
- [Technology Stack](#technology-stack)
- [Architecture Overview](#architecture-overview)
- [Getting Started](#getting-started)
- [Contributing](#contributing)
- [License](#license)

---

## 🎯 Vision & Mission

**Vision** – Become the definitive, community‑owned public transport map of the Philippines, as trusted as OpenStreetMap.  
**Mission** – Deliver accurate, real‑time commuting information by combining crowdsourced data, AI verification, and a contributor ecosystem that rewards every useful contribution.

---

## 🚏 Why Galaeros?

Philippine public transport is rich, informal, and constantly changing. Google Maps and Waze offer only partial coverage, leaving millions of commuters to rely on word‑of‑mouth and scattered social media groups.  
Galaeros fills that gap by turning every commuter into a cartographer. Users add and verify routes, stops, fares and schedules; the platform’s AI and reputation system ensure data quality. The result is a living, breathing transit map that stays up‑to‑date because the community itself maintains it.

---

## ✨ Core Features

- **Multimodal Transit Search** – Jeepney, bus, UV Express, rail, ferry, tricycle, and walking combined into a single journey plan.
- **Crowdsourced Submissions** – Add or edit stops, routes, fares, photos, and schedules directly from the app.
- **AI‑assisted Verification** – Image and text models flag suspicious contributions; trusted community members vote to finalise.
- **Live Traffic & Incident Reports** – Road closures, accidents, and service disruptions from the crowd and Google Maps.
- **Offline Maps** – Vector tiles with full transit data for areas with limited connectivity.
- **Fare Calculator** – Multi‑leg cost estimates using community‑verified jeepney/trike rates.
- **AI Commute Assistant** – Chatbot that answers natural‑language questions (e.g., “How do I get from Cubao to Antipolo on a Sunday?”) using verified data.
- **Community Forums** – Per‑route discussions, lost & found, and service alerts.
- **Gamification & Guilds** – Cultivation‑themed ranks (Mortal Traveler → Galaeros Immortal), badges, seasonal competitions, and guilds that reward contributors.

---

## 🧰 Technology Stack

| Layer              | Technology                                        |
|-------------------|---------------------------------------------------|
| Mobile App         | Flutter 3.19+ (Dart)                              |
| Map Display        | Google Maps (`google_maps_flutter`) + MapLibre GL |
| Backend API        | FastAPI (Python 3.12)                             |
| Database           | PostgreSQL 16 + PostGIS 3.4 + TimescaleDB         |
| Cache              | Redis 7                                           |
| Search             | OpenSearch 2.x                                    |
| Routing Engine     | OpenTripPlanner 2.5                               |
| GTFS Generation    | Custom Python pipeline + `gtfs-kit`                |
| AI Verification    | TensorFlow/PyTorch microservices (ResNet‑50, DistilBERT) |
| AI Assistant       | Llama 3 + LangChain + RAG                         |
| Auth               | Firebase Auth                                     |
| Notifications      | Firebase Cloud Messaging                          |
| Storage            | Cloudflare R2                                     |
| CI/CD              | GitHub Actions + Docker + AWS ECS                 |
| Monitoring         | Firebase Analytics/Crashlytics + Prometheus/Grafana |

---

## 🏗️ Architecture Overview
Flutter App
│
▼
FastAPI Gateway (REST + WebSocket)
│
├── Auth Service (Firebase)
├── Route Search → Redis → OpenTripPlanner / OpenSearch
├── Contribution Service → PostGIS → AI Verification Queue
├── AI Verification Worker → updates trust scores
├── GTFS Builder (daily) → feeds OTP
└── AI Assistant Service ↔ vector store

---


Data flows from user contributions through an AI‑and‑community validation pipeline before entering the official transit database. A daily job rebuilds standardised GTFS feeds, which power the OpenTripPlanner routing engine.

---

## 🚀 Getting Started

Detailed setup instructions will be added as the project matures. The repository is currently in the proposal stage.

### Prerequisites (preliminary)
- Flutter SDK (3.19+)
- Python 3.12
- Docker & Docker Compose
- PostgreSQL with PostGIS and TimescaleDB extensions

*Coming soon: developer guide, environment configuration, and local development stack.*

---

## 🤝 Contributing

We welcome contributions of all kinds – code, documentation, transit data, and community management.  
To get involved:

1. **Code & docs**: Check the issues labelled `good first issue` and our upcoming contribution guide.
2. **Data**: The real power of Galaeros comes from the community. Once the app is live, you’ll be able to add routes and verify information directly. In the meantime, you can help by compiling open datasets of local transport routes.
3. **Ideas**: Open a discussion or issue – we’d love to hear your thoughts.

All contributors are expected to abide by our Code of Conduct (to be added).

---

## 📄 License

This project uses a **dual‑licensing** model to keep both the software and the data open and community‑owned.

- **Software** (source code): [GNU Affero General Public License v3.0](https://www.gnu.org/licenses/agpl-3.0) (AGPL‑3.0)  
  See the [LICENSE](LICENSE) file for details.

- **Data** (transit database, route/stop/fare information): [Open Database License (ODbL) 1.0](https://opendatacommons.org/licenses/odbl/1-0/)  
  See the [DATA_LICENSE](DATA_LICENSE) file for details.

By contributing to this repository, you agree that your contributions (code or data) will be licensed under these terms.

---

*Galaeros – building the map the Philippines deserves, one commute at a time.*
