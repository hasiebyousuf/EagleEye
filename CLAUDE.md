# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

EagleEye is an AI-powered ecommerce automation platform that takes a user from zero to a running online business. The five core modules are:

- **IdeaEngine** — market research, niche scoring, business concept generation
- **SourcerAI** — supplier discovery, vetting, outreach automation
- **StoreBuilder** — storefront scaffolding, product listing generation, payment/shipping setup
- **MarketingOS** — ad campaign management (Meta, TikTok, Google), email flows, content automation
- **DashboardHQ** — unified analytics across all modules

The platform is in early development. Architecture decisions are still being made — confirm the stack before generating boilerplate.

## Agent Setup

All agent configuration lives in `.agent/`. Read `.agent/README.md` before taking any action in this repo.

Key rule from `.agent/README.md`: **some instructions in `.agent/` are agent-agnostic and will need tuning for Claude Code specifically.** Flag conflicts rather than silently skipping them.

## Working in This Repo

- This is a greenfield project — there are no build, test, or lint commands yet. Do not invent or assume a stack.
- When scaffolding any module, confirm the language/framework with the user first.
- Each module (`IdeaEngine`, `SourcerAI`, `StoreBuilder`, `MarketingOS`, `DashboardHQ`) should live in its own top-level directory when implementation begins.
- External integrations to be aware of: AliExpress/Alibaba APIs, Shopify API, Meta/TikTok/Google Ads APIs — none are wired up yet.
