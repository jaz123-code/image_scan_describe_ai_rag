AI Document Intelligence Platform

An end-to-end AI system that processes documents, extracts structured data,
automatically approves or flags them using confidence scoring,
and continuously improves through feedback-driven learning.

Key Features
Real-time document scanning with OCR + vision models
Confidence-based auto-approval system
Active learning with human feedback loop
Automated retraining pipeline (scheduled + manual)
Model performance tracking and promotion
Cost-aware AI routing
Admin dashboard with system analytics
WebSocket-based real-time progress tracking

Describe flow:

Frontend (React)
    ↓
FastAPI Backend
    ↓
Celery Workers (Async Processing)
    ↓
Redis (Queue + Pub/Sub)
    ↓
ML Pipeline (Routing + Scoring + Validation)
    ↓
Database (Results + Feedback + Models)

The system collects user feedback on predictions,
builds training datasets automatically,
and retrains models to improve future decisions.