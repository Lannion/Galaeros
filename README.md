# Galaeros – Community-Powered Transit Navigation for the Philippines

> **Every commuter is a cartographer. Every contribution improves someone's journey.**

[![License: AGPL v3](https://img.shields.io/badge/License-AGPL_v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)
[![Data License: ODbL](https://img.shields.io/badge/Data%20License-ODbL-brightgreen.svg)](DATA_LICENSE)
[![Status](https://img.shields.io/badge/Status-MVP%20Planning-orange)]()

Galaeros is an **open-source, community-powered public transportation platform** built specifically for the Philippines.

Our goal is to make commuting easier by creating a living transportation map that includes jeepneys, tricycles, buses, ferries, UV Express, rail systems, and other local transportation methods that are often missing or incomplete in existing navigation apps.

Unlike traditional mapping platforms, Galaeros believes that **the people who use public transportation every day are the best people to map it.**

---

# 🚧 Project Status

> **Planning & Early MVP Development**

Galaeros is currently in its planning and early development stage.

The first release **will NOT attempt to map the entire Philippines.**

Instead, the project follows an incremental approach:

```
Pilot Area
      ↓
City
      ↓
Province
      ↓
Region
      ↓
Nationwide
```

Our first goal is to successfully build and validate the platform within a small pilot region before expanding through community contributions.

---

# 🌏 Vision

To become the **community-owned transportation map of the Philippines**, providing accurate, open, and constantly updated commuting information for everyone.

Inspired by projects like:

- OpenStreetMap
- Wikipedia
- Waze Community Map Editors

But built specifically around the unique transportation system of the Philippines.

---

# 🎯 Mission

Empower commuters to improve public transportation information by combining:

- Community contributions
- Open data
- Reputation-based verification
- Practical AI assistance
- Open-source collaboration

---

# ❓ Why Galaeros?

Public transportation in the Philippines is dynamic.

Routes change.

Fares change.

Loading areas move.

New terminals appear.

Many routes only exist through local knowledge shared in Facebook groups or by asking strangers.

Even popular navigation apps often have limited information for:

- Jeepneys
- Tricycles
- UV Express
- Provincial buses
- Ferry routes
- Island transportation

Galaeros aims to preserve and organize that knowledge through a collaborative platform where everyone can contribute.

---

# ✨ Core Features

## 🚍 Multimodal Route Search

Search complete commuting journeys using combinations of:

- Jeepneys
- Modern Jeepneys
- Tricycles
- UV Express
- Bus
- MRT
- LRT
- PNR
- Ferry
- Walking

Example:

```
SM Bacoor → PITX
```

Results include:

- Estimated travel time
- Estimated fare
- Transfers
- Walking distance

---

## 🗺 Community Contributions

Users can contribute:

- New routes
- Stops
- Terminals
- Fare updates
- Photos
- Schedule changes
- Route corrections
- Service alerts

Every contribution helps improve the transportation map.

---

## ✅ Community Verification

Data quality is maintained through community validation.

Instead of relying solely on AI, Galaeros starts with:

- Reputation system
- Community voting
- Duplicate detection
- GPS validation

As the project grows, AI-assisted verification will help moderators review contributions more efficiently.

---

## 🧭 Fare Calculator

Estimate commuting expenses across multiple transportation types.

Supports:

- Regular Fare
- Student Discount
- Senior Citizen Discount
- PWD Discount

---

## 📍 Saved Routes

Save:

- Home
- Work
- School
- Favorite destinations

for faster navigation.

---

## 🏆 Gamification

Contributors earn experience by improving the map.

Inspired by Eastern fantasy cultivation systems.

Progression:

```
Mortal Traveler

↓

Path Seeker

↓

Route Disciple

↓

Map Adept

↓

Transit Master

↓

Grand Cartographer

↓

Arch Navigator

↓

Celestial Pathfinder

↓

Mythic Wayfinder

↓

Galaeros Immortal
```

Players also earn:

- Badges
- Titles
- Achievements
- Seasonal Rankings

The goal is simple:

> Reward people who help commuters.

---

# 🌱 Project Principles

Galaeros follows a few simple principles.

- Community before automation.
- Open data whenever legally possible.
- Offline-first whenever possible.
- Accuracy over speed.
- Local knowledge matters.
- Every commuter can contribute.

---

# 🗺 Initial Coverage

The first public release focuses on a limited pilot area.

Planned MVP coverage:

- Bacoor
- Imus
- Dasmariñas
- PITX

Future expansion:

- Cavite
- Metro Manila
- CALABARZON
- Luzon
- Visayas
- Mindanao

Eventually:

🇵🇭 Entire Philippines

---

# 🚀 MVP Roadmap

## Phase 1 — Foundation

- Flutter Mobile App
- Authentication
- Interactive Map
- Search Stops
- Search Routes
- Favorite Routes

---

## Phase 2 — Community Mapping

- Add Routes
- Add Stops
- Upload Photos
- Fare Updates
- Community Verification
- Reputation System

---

## Phase 3 — Smarter Navigation

- Route Planning
- Notifications
- Offline Maps
- Better Search
- Community Moderation

---

## Phase 4 — Intelligent Features

- AI-assisted Verification
- Natural Language Search
- Advanced Routing
- Province Expansion
- Public API

---

# 🧰 Technology Stack

The technology stack is intentionally simple for the MVP and will evolve as the project grows.

| Layer | MVP | Future |
|---------|------|----------|
| Mobile | Flutter | Flutter |
| Backend | FastAPI | FastAPI |
| Database | PostgreSQL + PostGIS | PostgreSQL + TimescaleDB |
| Maps | MapLibre + OpenStreetMap | Optional Google Maps Layer |
| Authentication | Firebase Auth | Firebase/Auth0 |
| Search | PostgreSQL Full Text Search | OpenSearch |
| Cache | Redis | Redis Cluster |
| Storage | Cloudflare R2 | Cloudflare R2 / S3 |
| Routing | Python Graph Engine | OpenTripPlanner |
| AI | Rule-based Verification | Machine Learning + LLM |
| Hosting | Docker | Kubernetes / Cloud |

---

# 🏗 Architecture

```
Flutter Mobile App
        │
        ▼
FastAPI Backend
        │
 ┌──────┼─────────┐
 │      │         │
 ▼      ▼         ▼
PostGIS Redis  Cloud Storage
 │
 ▼
Community Verification
 │
 ▼
Official Transit Database
```

Future services such as AI verification, OpenTripPlanner, and AI assistants will be introduced gradually as the project matures.

---

# 🤖 AI Philosophy

Artificial Intelligence is **not the foundation** of Galaeros.

The community is.

The first versions prioritize practical verification methods:

- Duplicate detection
- GPS consistency
- Reputation scores
- Community voting

Machine learning models will assist moderators once enough transportation data has been collected.

---

# ❤️ Why Open Source?

Transportation changes every day.

No single company or developer can keep every jeepney, tricycle, ferry, and bus route updated.

The only sustainable solution is a community-driven one.

Open source allows:

- Transparency
- Collaboration
- Community ownership
- Faster improvements
- Long-term sustainability

Every contribution—whether code, documentation, or transit data—helps improve commuting for millions of Filipinos.

---

# 📂 Repository Structure

```
galaeros/

├── apps/
│   └── mobile_flutter/
│
├── backend/
│   ├── api/
│   ├── services/
│   └── workers/
│
├── database/
│
├── docs/
│
├── scripts/
│
├── docker/
│
├── data/
│
└── README.md
```

---

# 🚀 Getting Started

The project is currently under active planning.

Developer setup instructions, Docker configuration, and contribution guides will be added as development progresses.

---

# 🤝 Contributing

Galaeros welcomes contributions from everyone.

You can help by:

- Improving the codebase
- Writing documentation
- Reporting issues
- Suggesting features
- Contributing transportation data
- Verifying community submissions

Our long-term success depends on the community.

Whether you're a software developer, commuter, student, or transport enthusiast, your contributions are valuable.

---

# 📜 License

This project uses a dual-license model.

### Software

Licensed under the **GNU Affero General Public License v3.0 (AGPL-3.0)**.

See [LICENSE](LICENSE).

### Transportation Data

Licensed under the **Open Database License (ODbL 1.0)**.

See [DATA_LICENSE](DATA_LICENSE).

By contributing to Galaeros, you agree that your code and data contributions will be released under these licenses.

---

# 🌟 Long-Term Vision

Galaeros isn't trying to replace Google Maps.

It aims to become the **community-maintained transportation knowledge base for the Philippines**—a platform where commuters collectively preserve and improve the country's unique public transit network.

Every route added.

Every fare corrected.

Every stop verified.

Brings millions of Filipinos one step closer to a smarter and more accessible commute.

---

> **Galaeros — Building the transportation map the Philippines deserves, one contribution at a time.**
