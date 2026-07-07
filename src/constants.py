"""
RetailPulse
Global Constants

This module contains all application-wide constants used across the
dashboard. Keeping everything centralized makes the project easier
to maintain and scale.
"""

from pathlib import Path


# ==========================================================
# PROJECT INFORMATION
# ==========================================================

APP_NAME = "RetailPulse"
APP_TAGLINE = "AI-Powered Retail Analytics Dashboard"

AUTHOR = "Junaid"

VERSION = "1.0.0"


# ==========================================================
# DIRECTORY STRUCTURE
# ==========================================================

ROOT_DIR = Path(__file__).resolve().parent.parent

ASSETS_DIR = ROOT_DIR / "assets"

DATA_DIR = ASSETS_DIR / "data"

IMAGE_DIR = ASSETS_DIR / "images"

ICON_DIR = ASSETS_DIR / "icons"


# ==========================================================
# DATA FILES
# ==========================================================

SUPERSTORE_DATA = DATA_DIR / "superstore.csv"

CUSTOMER_DATA = DATA_DIR / "customers.csv"

ROSSMANN_DATA = DATA_DIR / "rossmann_processed.csv"

CHURN_DATA = DATA_DIR / "customer_churn.csv"

INVENTORY_DATA = DATA_DIR / "inventory.csv"


# ==========================================================
# PAGE INFORMATION
# ==========================================================

PAGE_TITLES = {
    "home": "Home",
    "customer_segmentation": "Customer Segmentation",
    "demand_forecasting": "Demand Forecasting",
    "churn_prediction": "Customer Churn Prediction",
    "inventory_optimization": "Inventory Optimization",
    "business_insights": "Business Insights",
}


PAGE_ICONS = {
    "home": "🏠",
    "customer_segmentation": "👥",
    "demand_forecasting": "📈",
    "churn_prediction": "🔄",
    "inventory_optimization": "📦",
    "business_insights": "💼",
}


# ==========================================================
# DASHBOARD THEME
# ==========================================================

PRIMARY_COLOR = "#4F46E5"

SECONDARY_COLOR = "#7C3AED"

SUCCESS_COLOR = "#22C55E"

WARNING_COLOR = "#F59E0B"

ERROR_COLOR = "#EF4444"

INFO_COLOR = "#0EA5E9"

BACKGROUND_COLOR = "#0F172A"

CARD_BACKGROUND = "#1E293B"

BORDER_COLOR = "#334155"

TEXT_PRIMARY = "#F8FAFC"

TEXT_SECONDARY = "#CBD5E1"

TEXT_MUTED = "#94A3B8"


# ==========================================================
# CHART COLORS
# ==========================================================

CHART_COLORS = [
    "#4F46E5",
    "#3B82F6",
    "#06B6D4",
    "#10B981",
    "#F59E0B",
    "#EF4444",
    "#8B5CF6",
    "#EC4899",
]

PLOTLY_TEMPLATE = "plotly_dark"


# ==========================================================
# KPI SETTINGS
# ==========================================================

KPI_CARD_HEIGHT = 150

KPI_ICON_SIZE = 30

KPI_VALUE_SIZE = 34

KPI_LABEL_SIZE = 16

KPI_BORDER_RADIUS = 18


# ==========================================================
# SIDEBAR
# ==========================================================

SIDEBAR_WIDTH = 320

SIDEBAR_LOGO_HEIGHT = 90


# ==========================================================
# LAYOUT
# ==========================================================

PAGE_PADDING = 1.5

CONTENT_MAX_WIDTH = 1600

DEFAULT_GAP = "medium"

DEFAULT_CHART_HEIGHT = 420


# ==========================================================
# TABLE SETTINGS
# ==========================================================

TABLE_HEIGHT = 500

ROWS_PER_PAGE = 15


# ==========================================================
# MAP SETTINGS
# ==========================================================

DEFAULT_ZOOM = 4


# ==========================================================
# ANIMATIONS
# ==========================================================

TRANSITION_SPEED = 0.25

CARD_SHADOW = (
    "0px 8px 20px rgba(0,0,0,0.25)"
)

CARD_RADIUS = "18px"


# ==========================================================
# CACHE SETTINGS
# ==========================================================

CACHE_TTL = 3600

CACHE_MAX_ENTRIES = 20


# ==========================================================
# DEFAULT FILTER VALUES
# ==========================================================

ALL_OPTION = "All"

TOP_N = 10


# ==========================================================
# EXPORT SETTINGS
# ==========================================================

CSV_FILENAME = "RetailPulse_Export.csv"

EXCEL_FILENAME = "RetailPulse_Report.xlsx"


# ==========================================================
# MODEL SETTINGS
# ==========================================================

RANDOM_STATE = 42

TEST_SIZE = 0.20


# ==========================================================
# FORECAST SETTINGS
# ==========================================================

FORECAST_PERIODS = 30


# ==========================================================
# CHURN SETTINGS
# ==========================================================

CHURN_THRESHOLD = 0.50


# ==========================================================
# INVENTORY SETTINGS
# ==========================================================

DEFAULT_SERVICE_LEVEL = 0.95


# ==========================================================
# BUSINESS INSIGHTS
# ==========================================================

TOP_PRODUCTS = 10

TOP_CUSTOMERS = 10

TOP_REGIONS = 10