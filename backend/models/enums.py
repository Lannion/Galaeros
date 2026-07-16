# backend/app/models/enums.py
"""
Core enumerations for the Galaeros platform.

Every registered account is a contributor from creation — Galaeros has no
passive "viewer" role; browsing, saving routes, and submitting contributions
are available to everyone. UserRole therefore models an escalating trust /
permission ladder built on top of that shared contributor identity, rather
than treating "contributor" as a tier some users opt into.

Community rank (the cultivation-inspired progression from the gamification
system) is tracked separately in ContributorRank, since it reflects earned
experience and engagement, not platform trust or permissions. A brand-new
CONTRIBUTOR can be a Mortal Traveler or, after enough activity, a Grand
Cartographer — rank and role move independently.
"""

from enum import Enum


class UserRole(str, Enum):
    """Trust / permission ladder. Every account starts at CONTRIBUTOR."""
    CONTRIBUTOR = "contributor"                    # default role for every account
    TRUSTED_CONTRIBUTOR = "trusted_contributor"     # earned via reputation/trust score
    MODERATOR = "moderator"
    ADMINISTRATOR = "administrator"


class ContributorRank(str, Enum):
    """
    Gamification progression (cultivation-inspired). Independent of
    UserRole — this reflects earned experience, not permissions.
    """
    MORTAL_TRAVELER = "mortal_traveler"
    PATH_SEEKER = "path_seeker"
    ROUTE_DISCIPLE = "route_disciple"
    MAP_ADEPT = "map_adept"
    TRANSIT_MASTER = "transit_master"
    GRAND_CARTOGRAPHER = "grand_cartographer"
    ARCH_NAVIGATOR = "arch_navigator"
    CELESTIAL_PATHFINDER = "celestial_pathfinder"
    MYTHIC_WAYFINDER = "mythic_wayfinder"
    GALAEROS_IMMORTAL = "galaeros_immortal"


class VehicleType(str, Enum):
    # --- Urban & Inner-City Transit ---
    JEEPNEY = "jeepney"
    MODERN_JEEPNEY = "modern_jeepney"
    TRICYCLE = "tricycle"
    PEDICAB = "pedicab"
    TAXI = "taxi"
    RIDE_HAILING_CAR = "ride_hailing_car"
    RIDE_HAILING_MC = "ride_hailing_motorcycle"  # e.g., Angkas, JoyRide

    # --- Mass Rapid Transit (Rail) ---
    MRT = "mrt"
    LRT = "lrt"
    PNR = "pnr"

    # --- Provincial & Inter-City Land Transit ---
    BUS = "bus"
    PROVINCIAL_BUS = "provincial_bus"
    UV_EXPRESS = "uv_express"
    MULTICAB = "multicab"
    KALESA = "kalesa"

    # --- Rugged, Off-Road, & Highland Transit ---
    HABAL_HABAL = "habal_habal"
    MOTORELA = "motorela"
    RAIL_TROLLEY = "rail_trolley"  # Hand-pushed rail carts

    # --- Maritime & Water-based Transit ---
    FERRY = "ferry"                     # City ferries (e.g., Pasig River)
    FAST_CRAFT = "fast_craft"           # High-speed passenger catamarans
    RORO = "roro"                       # Roll-on/Roll-off vehicle ferries
    PUMP_BOAT = "pump_boat"             # Motorized bangka/outrigger boats
    PASSENGER_SHIP = "passenger_ship"   # Overnight long-distance liners

    # --- Air Transit (Remote Islands) ---
    DOMESTIC_FLIGHT = "domestic_flight"

    # --- Active Transit ---
    WALKING = "walking"
    BICYCLE = "bicycle"


class RouteStatus(str, Enum):
    PENDING = "pending"
    ACTIVE = "active"
    SUSPENDED = "suspended"
    DEPRECATED = "deprecated"


class StopType(str, Enum):
    STANDARD = "standard"
    TERMINAL = "terminal"
    SPUR_STOP = "spur_stop"
    INTERCHANGE = "interchange"
    PORT = "port"       # Added for maritime stops
    AIRPORT = "airport"  # Added for flight stops


class ContributionTargetType(str, Enum):
    """Which entity a Contribution is about. See contribution.py."""
    STOP = "stop"
    ROUTE = "route"


class ContributionStatus(str, Enum):
    """
    Lifecycle of a single community contribution, per ARCHITECTURE.md >
    Community Verification: duplicate check -> GPS validation -> community
    voting -> trusted contributor review -> published.
    """
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    DUPLICATE = "duplicate"