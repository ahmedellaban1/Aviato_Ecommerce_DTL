# ETC – Internal Shared Logic for Django Projects

This package (`etc/`) is a centralized module for reusable constants, uploaders, Celery setup, and utility functions used across all Django projects by Ahmed Ellaban.

> 🧠 Use it to keep your code DRY, clean, and maintainable across projects.

---

## 🔖 Folder Structure

## etc/
    ├── celery.py # Global Celery setup
    ├── celery_task.py # Placeholder for shared Celery tasks
    ├── choices.py # Central constants for model choices
    ├── helper_functions.py # Shared uploader logic and file utils
    ├── init.py # Init module

---

## 🧠 Contribution Rules

### ✅ General Guidelines

- Do **not** mix project-specific logic here — this package is meant to be **general-purpose and reusable**.
- All names should be clear, lowercase, and snake_case.
- Document any new logic with a short comment above it.

---

## 🎯 `choices.py` Guidelines

> Central place for reusable field choices (e.g. gender, user type, product size, media type, etc.)

### ✅ RULES for Adding New Choices

1. **Append new choices at the end** of the list.
   - ✅ Good:
     ```python
     MEDIA_TYPE_CHOICES = [
         ('image', 'Image'),
         ('video', 'Video'),
         ('audio', 'Audio'),
         ('document', 'Document'),
         ('pdf', 'PDF'),  # added at the end
         ('other', 'Other'),
     ]
     ```

   - ❌ BAD:
     ```python
     MEDIA_TYPE_CHOICES = [
         ('pdf', 'PDF'),  # ❌ Do not put new types first!
         ('image', 'Image'),
         ...
     ]
     ```

2. This avoids breaking any code that relies on fixed ordering like:
   ```python
   media_type = MEDIA_TYPE_CHOICES[0][0]  # Assumes 'image'
   
