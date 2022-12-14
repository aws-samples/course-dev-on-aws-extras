#!/bin/bash
pylint back-end-python/gameactions/app.py
pytest back-end-python/tests/unit --cov-report=html --cov=gameactions --cov-branch
