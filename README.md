# Galaeros – Community-Powered Transit Navigation for the Philippines

> **Every commuter is a cartographer. Every contribution improves someone's journey.**

[![License: AGPL v3](https://img.shields.io/badge/License-AGPL_v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)
[![Data License: ODbL](https://img.shields.io/badge/Data%20License-ODbL-brightgreen.svg)](DATA_LICENSE)
[![Status](https://img.shields.io/badge/Status-MVP%20Planning-orange)]()

Galaeros is an open-source, community-powered public transportation platform built specifically for the Philippines. Our goal is to make commuting easier by building a living transportation map that includes jeepneys, tricycles, buses, ferries, UV Express, rail systems, and other local transportation methods that are often missing or incomplete in existing navigation apps.

Unlike traditional mapping platforms, Galaeros is built on a simple premise: **the people who use public transportation every day are the best people to map it.**

---

## 🚧 Project Status

**Planning & Early MVP Development**

The first release will **not** attempt to map the entire Philippines. Instead, the project follows an incremental rollout:

```
Pilot Area → City → Province → Region → Nationwide
```

The first goal is to build and validate the platform within a small pilot region before expanding through community contributions.

---

## 🌏 Vision

To become the community-owned transportation map of the Philippines — providing accurate, open, and constantly updated commuting information for everyone. Inspired by OpenStreetMap, Wikipedia, and Waze's community map editors, but built specifically around the unique transportation system of the Philippines.

---

## 🎯 Mission

Empower commuters to improve public transportation information by combining community contributions, open data, reputation-based verification, practical AI assistance, and open-source collaboration.

---

## ❓ Why Galaeros?

Public transportation in the Philippines is dynamic — routes change, fares change, loading areas move, new terminals appear. Much of this exists only as local knowledge shared in Facebook groups or by asking strangers.

Even popular navigation apps often have limited coverage for jeepneys, tricycles, UV Express, provincial buses, ferry routes, and island transportation. Galaeros aims to preserve and organize that knowledge through a collaborative platform where everyone can contribute.

---

## ✨ Core Features

### 🚍 Multimodal Route Search

Search complete commuting journeys across jeepneys, modern jeepneys, tricycles, UV Express, bus, MRT, LRT, PNR, ferry, and walking.

Example: `SM Bacoor → PITX`

Results include estimated travel time, estimated fare, transfers, and walking distance.

### 🗺 Community Contributions

Users can contribute new routes, stops, terminals, fare updates, photos, schedule changes, route corrections, and service alerts. Every contribution improves the transportation map.

### ✅ Community Verification

Data quality is maintained through community validation rather than AI alone. The MVP relies on a reputation system, community voting, duplicate detection, and GPS validation. AI-assisted verification will help moderators review contributions more efficiently as the project grows.

### 🧭 Fare Calculator

Estimate commuting expenses across transportation types, including regular fare, student discount, senior citizen discount, and PWD discount.

### 📍 Saved Routes

Save home, work, school, and favorite destinations for faster navigation.

### 🏆 Gamification

Contributors earn experience by improving the map. Progression is inspired by Eastern fantasy cultivation systems:

```
Mortal Traveler → Path Seeker → Route Disciple → Map Adept → Transit Master
→ Grand Cartographer → Arch Navigator → Celestial Pathfinder
→ Mythic Wayfinder → Galaeros Immortal
```

Contributors also earn badges, titles, achievements, and seasonal rankings. The goal: reward the people who help commuters.

---

## 🌱 Project Principles

- Community before automation.
- Open data whenever legally possible.
- Offline-first whenever possible.
- Accuracy over speed.
- Local knowledge matters.
- Every commuter can contribute.

---

## 🗺 Initial Coverage

The first public release focuses on a limited pilot area:

- Bacoor
- Imus
- Dasmariñas
- PITX

**Future expansion:** Cavite → Metro Manila → CALABARZON → Luzon → Visayas → Mindanao → 🇵🇭 entire Philippines.

---

## 🚀 MVP Roadmap

**Phase 1 — Foundation:** Flutter mobile app, authentication, interactive map, stop search, route search, favorite routes.

**Phase 2 — Community Mapping:** add routes, add stops, upload photos, fare updates, community verification, reputation system.

**Phase 3 — Smarter Navigation:** route planning, notifications, offline maps, improved search, community moderation.

**Phase 4 — Intelligent Features:** AI-assisted verification, natural language search, advanced routing, province expansion, public API.

---

## 🧰 Technology Stack

| Layer | MVP | Future |
|---|---|---|
| Mobile | Flutter | Flutter |
| Backend | FastAPI | FastAPI |
| Database | PostgreSQL + PostGIS | PostgreSQL + TimescaleDB |
| Maps | MapLibre + OpenStreetMap | Optional Google Maps layer |
| Authentication | Firebase Auth | Firebase / Auth0 |
| Search | PostgreSQL full-text search | OpenSearch |
| Cache | Redis | Redis Cluster |
| Storage | Cloudflare R2 | Cloudflare R2 / S3 |
| Routing | Python graph engine | OpenTripPlanner |
| AI | Rule-based verification | Machine learning + LLM |
| Hosting | Docker | Kubernetes / cloud |

---

## 🏗 Architecture

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

Future services such as AI verification, OpenTripPlanner, and AI assistants will be introduced gradually as the project matures. See [`ARCHITECTURE.md`](ARCHITECTURE.md) for the full system design.

---

## 🤖 AI Philosophy

Artificial intelligence is not the foundation of Galaeros — the community is. The first versions prioritize practical verification methods: duplicate detection, GPS consistency, reputation scores, and community voting. Machine learning models will assist moderators once enough transportation data has been collected.

---

## ❤️ Why Open Source?

Transportation changes every day. No single company or developer can keep every jeepney, tricycle, ferry, and bus route updated — the only sustainable solution is a community-driven one. Open source enables transparency, collaboration, community ownership, faster improvements, and long-term sustainability.

---

## 📂 Repository Structure

```
galaeros/
├── backend/
│   ├── api/
│   ├── core/
│   ├── migrations/
│   ├── models/
│   ├── repositories/
│   ├── schemas/
│   ├── services/
│   ├── workers/
│   └── tests/
├── frontend/
│   └── lib/
│       ├── core/
│       ├── features/
│       ├── shared/
│       └── theme/
├── database/
├── docs/
├── scripts/
├── docker/
├── data/
└── README.md
```

This mirrors the structure defined in [`skills.md`](skills.md) — keep both in sync when the layout changes.

---

## 🚀 Getting Started

The project is currently under active planning. Developer setup instructions, Docker configuration, and contribution guides will be added as development progresses.

---

## 🤝 Contributing

Galaeros welcomes contributions from everyone — improving the codebase, writing documentation, reporting issues, suggesting features, contributing transportation data, or verifying community submissions. Whether you're a developer, commuter, student, or transport enthusiast, your contributions matter.

---

## 📜 License

This project uses a dual-license model.

**Software:** GNU Affero General Public License v3.0 (AGPL-3.0). See [LICENSE](LICENSE).

**Transportation data:** Open Database License (ODbL 1.0). See [DATA_LICENSE](DATA_LICENSE).

By contributing to Galaeros, you agree that your code and data contributions will be released under these licenses.

---

## 🌟 Long-Term Vision

Galaeros isn't trying to replace Google Maps. It aims to become the community-maintained transportation knowledge base for the Philippines — a platform where commuters collectively preserve and improve the country's unique public transit network, one route, fare, and stop at a time.

---

> **Galaeros — Building the transportation map the Philippines deserves, one contribution at a time.**