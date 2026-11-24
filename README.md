# ArtNest — Artwork E-commerce Platform

A Django-based artwork e-commerce platform built by a four-member team, where artists sell their work and buyers browse, customize and order artwork.

## Current status

**Work in progress; not currently deployed.** The platform is not finished. Cart quantity increase/decrease (+/−) behavior has known issues and needs correction and workflow testing. Other features also need further testing and refinement.

## Project areas

- Custom users with buyer, seller and staff roles, plus profiles
- Artwork catalogue and management
- Orders and shopping workflows
- Reviews, notifications and messaging
- Administrative dashboard
- A payments module; its presence does not establish a production payment integration

**Asma-Ul-Husna Oishee:** full-stack developer and primary contributor in the collaborative project.

## Stack and layout

Python, Django, server-rendered templates, SQLite and uploaded media. Settings identify the project as Django 5.2-era code and include `widget_tweaks`.

| Folder | Purpose |
| --- | --- |
| `ProjectArtGallery/` | Project settings, URL routing and server entry points |
| `users/`, `artworks/` | Accounts/profiles and art catalogue |
| `orders/`, `payments/`, `reviews/` | Marketplace workflows |
| `messaging/`, `notifications/` | Communication features |
| `admin_dashboard/` | Administrative screens |
| `templates/`, `static/` | UI templates and static assets |

## Local development — provisional

No dependency manifest is currently supplied. These steps are an initial setup guide inferred from settings, not a clean-install verification.

1. Clone the repository into a private development workspace.
2. Create an environment:

   ```powershell
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   python -m pip install "Django>=5.2,<5.3" Pillow django-widget-tweaks
   ```

   This is an initial dependency set, not a complete lockfile. Resolve additional imports against the actual source and pin the tested environment.

3. Review `ProjectArtGallery/settings.py`. Use your own local secret and database; the current settings are development-oriented. Environment variables are not automatically consumed unless the settings code is adapted to read them.
4. Use a fresh local SQLite database or an explicitly permitted synthetic fixture. Preserve existing data privately before replacing anything; do not depend on committed databases as public demo fixtures.
5. From the repository root:

   ```powershell
   python manage.py check
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py runserver
   ```

6. Open `http://127.0.0.1:8000/`; Django admin is at `/admin/`, with project administration at `/admin-dashboard/`.

Fresh migrations and runtime behavior were not executed for this README update. Do not resolve migration issues by deleting migrations or real data without understanding their history.

## Public demo and deployment

There is currently no deployed website or public live demo. Before deployment, pin dependencies, configure secrets outside source, set DEBUG/allowed hosts appropriately, serve static/media files deliberately, review permissions and test the supported workflows.

Database files and uploaded media require a separate privacy/redistribution review. This README does not certify that existing data is synthetic or that credential cleanup has been performed.

## Next improvements

- Fix cart quantity (+/−) controls and verify item quantities, subtotals and order totals

- Reproducible dependency file and clean-database setup
- Screenshots with synthetic accounts/content
- Feature and authorization tests
- Team contribution summary and media licences
- Documented deployment and payment-module scope

No project-wide software licence is asserted by this README.
