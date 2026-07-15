# Galaeros Architecture

> **Version:** 0.1.0 (MVP Planning)
>
> This document describes the overall system architecture, design philosophy, and future scalability of Galaeros.
>
> The architecture is intentionally designed to start simple while allowing future expansion without major rewrites.

---

# Table of Contents

- System Philosophy
- High-Level Architecture
- MVP Architecture
- Future Architecture
- Core Services
- Data Flow
- Database Design
- Routing Engine
- AI Roadmap
- Security
- Scalability
- Deployment
- Future Improvements

---

# System Philosophy

Galaeros follows a **progressive architecture**.

Instead of building a large enterprise system immediately, the project evolves in stages.

```
Simple

↓

Reliable

↓

Community Driven

↓

Scalable

↓

Intelligent
```

The MVP focuses on solving one problem well:

> Helping commuters discover and contribute public transportation information.

Everything else builds upon that foundation.

---

# Design Principles

The system follows these principles.

## Community First

The community is the primary source of transportation data.

AI assists the community.

It does not replace it.

---

## Open Data

Whenever legally possible,

transportation information should remain open and accessible.

---

## Offline Friendly

Internet access isn't always available.

The system should eventually support offline navigation.

---

## Modular

Every major component can be developed independently.

For example,

the routing engine can evolve without changing the mobile application.

---

## API First

Every feature communicates through APIs.

This allows future support for:

- Web application
- Desktop application
- Third-party integrations
- Public API

---

# High-Level Architecture

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

# MVP Architecture

The first version intentionally avoids unnecessary complexity.

```
Flutter

↓

FastAPI

↓

PostgreSQL + PostGIS

↓

Redis

↓

Cloud Storage
```

Features included

- Authentication
- Search
- Routes
- Stops
- Contributions
- Verification
- Reputation
- Gamification

No AI models.

No OpenTripPlanner.

No Kubernetes.

---

# Future Architecture

As Galaeros grows,

additional services can be introduced.

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

Every new service should be optional.

Nothing should break if a service is temporarily unavailable.

---

# Core Components

## Mobile Application

Technology

Flutter

Responsibilities

- Map interface
- Search routes
- Display navigation
- Submit contributions
- Receive notifications
- Gamification
- User profile

---

## Backend API

Technology

FastAPI

Responsibilities

- Authentication
- CRUD operations
- Route search
- User management
- Contribution processing
- Reputation calculations
- Notifications

Future

- GraphQL
- WebSockets
- Public API

---

## Database

Technology

PostgreSQL

Extension

PostGIS

Stores

- Users
- Routes
- Stops
- Cities
- Barangays
- Contributions
- Photos
- Reports
- Achievements

Reason

PostGIS provides powerful geographic queries.

---

## Cache

Technology

Redis

Uses

- Frequently searched routes
- Sessions
- Leaderboards
- Notifications

---

## Storage

Cloudflare R2

Stores

- Photos
- User avatars
- Route images
- Documents

---

# Routing Engine

## MVP

A lightweight Python graph engine.

Each stop becomes a node.

Each route becomes an edge.

Example

```
Stop A

↓

Jeepney

↓

Stop B

↓

Walk

↓

Bus

↓

Stop C
```

Libraries

- NetworkX

Advantages

- Easy to maintain
- Lightweight
- Free

---

## Future

Once sufficient GTFS data exists,

the routing engine can migrate to

OpenTripPlanner.

Advantages

- Better transfers
- Timetable support
- Multiple optimization algorithms
- GTFS compatibility

---

# Community Verification

The most important component of Galaeros.

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

# Reputation System

Every user has a trust score.

Trust increases when

- Contributions are accepted
- Reports are confirmed
- Routes are verified

Trust decreases when

- Spam
- False reports
- Incorrect data

Higher trust unlocks

- Faster approvals
- Moderator privileges
- New titles
- Higher cultivation realm

---

# AI Roadmap

Artificial Intelligence is introduced gradually.

## Phase 1

No machine learning.

Only

- Duplicate detection
- GPS validation
- Rule-based checks

---

## Phase 2

Machine learning assists moderation.

Possible models

- Image similarity
- Route anomaly detection
- Duplicate route detection

---

## Phase 3

Natural language assistant.

Example

```
How do I commute from
Bacoor to Tagaytay?
```

The assistant retrieves verified transportation data before generating a response.

---

# Database Overview

Main entities

```
Users

Routes

Stops

Vehicles

Cities

Barangays

Fares

Schedules

Contributions

Verification Votes

Achievements

Guilds

Experience

Reports

Notifications
```

Everything revolves around

Contributions

because Galaeros is a community-driven platform.

---

# Security

Authentication

Firebase Authentication

Supports

- Google
- Email
- Phone

Future

- Apple
- Facebook

---

Authorization

Role Based Access Control

Roles

- User
- Trusted Contributor
- Moderator
- Administrator

---

Data Protection

- HTTPS
- JWT
- Secure file uploads
- Rate limiting
- Audit logs

---

# Scalability

The architecture is designed for gradual growth.

## Stage 1

Single VPS

Docker

SQLite (development)

PostgreSQL (production)

---

## Stage 2

Separate

- API
- Database
- Storage

---

## Stage 3

Microservices

- Search
- AI
- Routing
- Notifications

---

## Stage 4

Nationwide deployment

Load balancer

Multiple API instances

Redis Cluster

OpenSearch

OpenTripPlanner

---

# Deployment

Development

```
Flutter

↓

FastAPI

↓

Docker Compose

↓

PostgreSQL
```

Production

```
Flutter

↓

FastAPI

↓

Docker

↓

PostgreSQL

↓

Cloudflare R2

↓

Redis
```

Future

```
Kubernetes

↓

Multiple Services

↓

OpenSearch

↓

OpenTripPlanner
```

---

# Future Improvements

Potential future modules

- Live vehicle GPS
- LGU dashboards
- Operator portal
- Route analytics
- Disaster response mode
- Tourism mode
- Offline province packages
- Smart fare prediction
- Predictive arrival time
- AI-assisted moderation
- Public Developer API

---

# Architecture Goals

The Galaeros architecture is designed to achieve five long-term goals.

## Simplicity

A solo developer should be able to understand and maintain the system.

---

## Scalability

The architecture should support millions of users without requiring major redesign.

---

## Reliability

Transportation information should remain available even when some services are offline.

---

## Community Ownership

The transportation map improves through contributor participation rather than relying solely on a central authority.

---

## Sustainability

Every technology choice should prioritize open-source solutions, low operational costs, and long-term maintainability.

---

> **Architecture is not about building everything on day one.**
>
> It is about creating a foundation that allows Galaeros to grow from a local commuting tool into the community-maintained transportation platform for the Philippines.
