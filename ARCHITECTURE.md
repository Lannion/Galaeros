# Galaeros Architecture

> **Version:** 0.1.0 (MVP Planning)
>
> This document describes the system architecture, design philosophy, and long-term scalability plan for Galaeros. It is intentionally designed to start simple while allowing future expansion without major rewrites.

---

## Table of Contents

- [System Philosophy](#system-philosophy)
- [Design Principles](#design-principles)
- [High-Level Architecture](#high-level-architecture)
- [MVP Architecture](#mvp-architecture)
- [Future Architecture](#future-architecture)
- [Core Components](#core-components)
- [Routing Engine](#routing-engine)
- [Community Verification](#community-verification)
- [Reputation System](#reputation-system)
- [AI Roadmap](#ai-roadmap)
- [Database Overview](#database-overview)
- [Security](#security)
- [Scalability](#scalability)
- [Deployment](#deployment)
- [Future Improvements](#future-improvements)
- [Architecture Goals](#architecture-goals)

---

## System Philosophy

Galaeros follows a progressive architecture: **Simple → Reliable → Community Driven → Scalable → Intelligent.**

The MVP focuses on solving one problem well: helping commuters discover and contribute public transportation information. Everything else builds on that foundation.

---

## Design Principles

- **Community first.** The community is the primary source of transportation data; AI assists it, and never replaces it.
- **Open data.** Transportation information should remain open and accessible wherever legally possible.
- **Offline friendly.** Internet access isn't always available — the system should eventually support offline navigation.
- **Modular.** Every major component can be developed independently (e.g. the routing engine can evolve without touching the mobile app).
- **API first.** Every feature communicates through APIs, enabling future web, desktop, and third-party integrations.

---

## High-Level Architecture

```
                Flutter Mobile App
                        │
                        ▼
                FastAPI REST API
                        │
        ┌───────────────┼───────────────┐
        │               │               │
        ▼               ▼               ▼
 PostgreSQL       Redis Cache     Cloud Storage
   + PostGIS                        (Images)
        │
        ▼
 Community Verification
        │
        ▼
 Official Transit Database
```

---

## MVP Architecture

```
Flutter → FastAPI → PostgreSQL + PostGIS → Redis → Cloud Storage
```

**In scope:** authentication, search, routes, stops, contributions, verification, reputation, gamification.

**Explicitly out of scope for MVP:** AI models, OpenTripPlanner, Kubernetes.

---

## Future Architecture

```
                    Flutter
                       │
                       ▼
                 API Gateway
                       │
    ┌───────────┬────────────┬─────────────┐
    │           │            │             │
    ▼           ▼            ▼             ▼
 Auth      Route Search  Contributions   AI Assistant
    │           │            │
    ▼           ▼            ▼
 PostgreSQL   Redis      AI Verification
        │
        ▼
 OpenTripPlanner
        │
        ▼
 Transit Database
```

Every new service should be optional — nothing should break if a service is temporarily unavailable.

---

## Core Components

### Mobile Application

**Technology:** Flutter

**Responsibilities:** map interface, route search, navigation display, contribution submission, notifications, gamification, user profile.

### Backend API

**Technology:** FastAPI

**Responsibilities:** authentication, CRUD operations, route search, user management, contribution processing, reputation calculations, notifications.

**Future:** GraphQL, WebSockets, public API.

### Database

**Technology:** PostgreSQL + PostGIS

**Stores:** users, routes, stops, cities, barangays, contributions, photos, reports, achievements.

PostGIS provides the geographic query support (proximity search, route geometry) the platform depends on.

### Cache

**Technology:** Redis

**Uses:** frequently searched routes, sessions, leaderboards, notifications.

### Storage

**Technology:** Cloudflare R2

**Stores:** photos, user avatars, route images, documents.

---

## Routing Engine

### MVP

A lightweight Python graph engine (NetworkX) where each stop is a node and each route is a set of edges:

```
Stop A → Jeepney → Stop B → Walk → Bus → Stop C
```

**Advantages:** easy to maintain, lightweight, free.

### Future

Once sufficient GTFS data exists, migrate to OpenTripPlanner for better transfers, timetable support, multiple optimization algorithms, and GTFS compatibility.

---

## Community Verification

```
User submits route
        ↓
Duplicate check
        ↓
GPS validation
        ↓
Community voting
        ↓
Trusted contributor review
        ↓
Published
```

This keeps the database accurate while remaining scalable.

---

## Reputation System

Every user has a trust score.

**Trust increases** when contributions are accepted, reports are confirmed, or routes are verified.

**Trust decreases** with spam, false reports, or incorrect data.

**Higher trust unlocks** faster approvals, moderator privileges, new titles, and higher cultivation-rank progression.

---

## AI Roadmap

| Phase | Scope |
|---|---|
| Phase 1 | No machine learning — duplicate detection, GPS validation, rule-based checks only. |
| Phase 2 | ML-assisted moderation — image similarity, route anomaly detection, duplicate route detection. |
| Phase 3 | Natural language assistant that retrieves verified transportation data before generating a response (e.g. *"How do I commute from Bacoor to Tagaytay?"*). |

---

## Database Overview

Main entities: Users, Routes, Stops, Vehicles, Cities, Barangays, Fares, Schedules, Contributions, Verification Votes, Achievements, Guilds, Experience, Reports, Notifications.

Everything revolves around **Contributions**, since Galaeros is a community-driven platform.

---

## Security

**Authentication:** Firebase Authentication — Google, email, phone today; Apple and Facebook planned.

**Authorization:** Role-based access control — User, Trusted Contributor, Moderator, Administrator.

**Data protection:** HTTPS, JWT, secure file uploads, rate limiting, audit logs.

---

## Scalability

| Stage | Setup |
|---|---|
| 1 | Single VPS, Docker Compose, PostgreSQL + PostGIS locally for both development and production. |
| 2 | API, database, and storage separated into independent services. |
| 3 | Microservices for search, AI, routing, and notifications. |
| 4 | Nationwide deployment: load balancer, multiple API instances, Redis Cluster, OpenSearch, OpenTripPlanner. |

---

## Deployment

**Development**

```
Flutter → FastAPI → Docker Compose → PostgreSQL + PostGIS
```

**Production**

```
Flutter → FastAPI → Docker → PostgreSQL + PostGIS → Cloudflare R2 → Redis
```

**Future**

```
Kubernetes → Multiple Services → OpenSearch → OpenTripPlanner
```

---

## Future Improvements

Live vehicle GPS, LGU dashboards, operator portal, route analytics, disaster response mode, tourism mode, offline province packages, smart fare prediction, predictive arrival time, AI-assisted moderation, public developer API.

---

## Architecture Goals

- **Simplicity** — a solo developer should be able to understand and maintain the system.
- **Scalability** — support millions of users without requiring a major redesign.
- **Reliability** — transportation information stays available even when some services are offline.
- **Community ownership** — the map improves through contributor participation, not solely a central authority.
- **Sustainability** — every technology choice prioritizes open-source solutions, low operational cost, and long-term maintainability.

---

> Architecture isn't about building everything on day one. It's about creating a foundation that lets Galaeros grow from a local commuting tool into the community-maintained transportation platform for the Philippines.