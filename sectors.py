"""
Sector registry for GroundLens.

Each entry fully describes one decision domain: what's being ranked, what
data drives it, which factors matter, and how those factors should be
worded for a normal person to understand. The scoring engine itself
(decision_engine.py) never changes -- only this config does. That's the
whole trick behind the "pick a sector" demo: same brain, new context.

To add a new sector: add a CSV under data/, add an entry below, done.
The dashboard (app.py) builds its sliders and charts from this file
automatically -- no UI code to touch.
"""

SECTORS = {
    "community": {
        "label": "Community & social impact",
        "icon": "\U0001F4A7",  # droplet
        "tagline": "Decide where limited resources go first -- boreholes, clinics, school support.",
        "user_line": "You're an NGO or local government with limited resources and many communities asking for help.",
        "data_path": "data/communities.csv",
        "name_col": "community",
        "entity_label": "community",
        "factors": {
            "water_access": {
                "column": "water_distance_km", "direction": "higher_priority",
                "label": "Water access", "help": "Farther from clean water = higher priority.",
                "default_weight": 35,
            },
            "health_risk": {
                "column": "disease_rate_per_1000", "direction": "higher_priority",
                "label": "Health risk", "help": "Higher disease rate = higher priority.",
                "default_weight": 30,
            },
            "education_gap": {
                "column": "school_enrollment_pct", "direction": "lower_priority",
                "label": "Education gap", "help": "Lower school enrollment = higher priority.",
                "default_weight": 10,
            },
            "population": {
                "column": "population", "direction": "higher_priority",
                "label": "Population affected", "help": "More people reached = higher priority.",
                "default_weight": 15,
            },
            "drought_risk": {
                "column": "drought_risk_index", "direction": "higher_priority",
                "label": "Drought risk", "help": "Higher drought risk = higher priority.",
                "default_weight": 10,
            },
        },
    },

    "business": {
        "label": "Business & product",
        "icon": "\U0001F4BC",  # briefcase
        "tagline": "Decide which product, market, or initiative to invest in next.",
        "user_line": "You're a founder or exec with one budget and several promising initiatives competing for it.",
        "data_path": "data/business_options.csv",
        "name_col": "initiative",
        "entity_label": "initiative",
        "factors": {
            "market_demand": {
                "column": "market_demand", "direction": "higher_priority",
                "label": "Market demand", "help": "Stronger demand signal = higher priority.",
                "default_weight": 25,
            },
            "projected_roi": {
                "column": "projected_roi_pct", "direction": "higher_priority",
                "label": "Projected ROI", "help": "Higher projected return = higher priority.",
                "default_weight": 30,
            },
            "cost_to_build": {
                "column": "cost_to_build_musd", "direction": "lower_priority",
                "label": "Cost to build", "help": "Cheaper to build = higher priority.",
                "default_weight": 20,
            },
            "competitive_risk": {
                "column": "competitive_risk", "direction": "lower_priority",
                "label": "Competitive risk", "help": "Lower risk of being out-competed = higher priority.",
                "default_weight": 10,
            },
            "team_readiness": {
                "column": "team_readiness", "direction": "higher_priority",
                "label": "Team readiness", "help": "More team skill/capacity already in place = higher priority.",
                "default_weight": 15,
            },
        },
    },

    "government": {
        "label": "Government & public policy",
        "icon": "\U0001F3DB",  # classical building
        "tagline": "Decide which public project or policy to fund first.",
        "user_line": "You're a ministry or council allocating a public budget across competing projects.",
        "data_path": "data/policy_projects.csv",
        "name_col": "project",
        "entity_label": "project",
        "factors": {
            "population_impact": {
                "column": "population_impact", "direction": "higher_priority",
                "label": "Population impact", "help": "More people reached = higher priority.",
                "default_weight": 25,
            },
            "cost": {
                "column": "cost_musd", "direction": "lower_priority",
                "label": "Cost", "help": "Lower cost = higher priority.",
                "default_weight": 20,
            },
            "urgency": {
                "column": "urgency", "direction": "higher_priority",
                "label": "Urgency", "help": "More time-critical = higher priority.",
                "default_weight": 25,
            },
            "political_feasibility": {
                "column": "political_feasibility", "direction": "higher_priority",
                "label": "Political feasibility", "help": "Easier to get approved and implemented = higher priority.",
                "default_weight": 10,
            },
            "long_term_roi": {
                "column": "long_term_roi", "direction": "higher_priority",
                "label": "Long-term ROI", "help": "Stronger long-term payoff = higher priority.",
                "default_weight": 20,
            },
        },
    },

    "career": {
        "label": "Personal & career",
        "icon": "\U0001F3AF",  # target
        "tagline": "Decide between job offers, schools, or life paths -- with your own priorities made explicit.",
        "user_line": "You have more than one real option in front of you and no obvious right answer.",
        "data_path": "data/career_options.csv",
        "name_col": "option",
        "entity_label": "option",
        "factors": {
            "salary": {
                "column": "salary_musd", "direction": "higher_priority",
                "label": "Salary", "help": "Higher salary = higher priority.",
                "default_weight": 20,
            },
            "growth_potential": {
                "column": "growth_potential", "direction": "higher_priority",
                "label": "Growth potential", "help": "More room to grow = higher priority.",
                "default_weight": 25,
            },
            "work_life_balance": {
                "column": "work_life_balance", "direction": "higher_priority",
                "label": "Work-life balance", "help": "Better balance = higher priority.",
                "default_weight": 20,
            },
            "location_fit": {
                "column": "location_fit", "direction": "higher_priority",
                "label": "Location fit", "help": "Better fits where you want to live = higher priority.",
                "default_weight": 15,
            },
            "mission_alignment": {
                "column": "mission_alignment", "direction": "higher_priority",
                "label": "Mission alignment", "help": "Closer to work you find meaningful = higher priority.",
                "default_weight": 20,
            },
        },
    },
}
