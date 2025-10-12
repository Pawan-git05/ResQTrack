# ResQTrack – Product Requirement Document (PRD)

Mission: Empowering compassion with technology — so no injured animal is left unattended.

## Core Objectives
- Enable quick and accessible reporting of animal emergencies.
- Provide efficient communication and assignment between NGOs, volunteers, and hospitals.
- Build transparency and trust via tracking and updates.
- Encourage community participation through donations, volunteering, and awareness.

## User Roles
- Citizen / General User: Report cases, donate, view gallery
- Volunteer: Register, accept assigned cases, update rescue status
- NGO / Shelter Admin: Approve cases, assign volunteers, manage rescues
- Hospital Staff (Optional): Register as treatment partner
- Platform Admin: Approve NGO & volunteers, manage content, monitor data integrity

## Platform Structure & Pages
- Homepage (banner, mission, CTAs, counters)
- Report Animal Case (form + media)
- NGO & Volunteer Registration (tabs)
- Donation (one-time/monthly)
- Case Tracking Dashboard (color-coded statuses)
- Hospital Directory (map + filters)
- Integration Page (live rescues)
- Gallery / Media

## Technical Requirements
Backend: Flask (REST), MySQL, JWT auth, Mail, optional S3
Frontend: HTML/CSS/JS (Bootstrap), responsive
DevOps: Postman, GitHub, optional hosting

## Entities
NGO, Volunteer, AnimalCase, Hospital, Donation, Admin

## Non-Functional
- Security: validation, SSL, payment encryption
- Scalability: modular APIs
- Performance: <2s for critical endpoints
- Accessibility: high contrast, large fonts, alt-text
- Backup: weekly dumps

## Deliverables
- Working website with DB + UI + core features
- MySQL schema + export
- Flask APIs
- Documentation (PRD, ER, DFD, architecture)
- Presentation & demo (optional)
