"""
Calculation utilities for FESP 11-block diagnostic
"""
from typing import List, Dict, Any
from app.fesp_items import (
    FESP_ITEMS, get_all_items, get_total_max_points,
    calculate_compliance_level, get_capabilities, get_policy_cycles
)


def calculate_traffic_light(percentage: float) -> str:
    """Calculate traffic light color based on percentage (0-100)"""
    level = calculate_compliance_level(percentage)
    return level["color"]


def calculate_fesp_scores(items: List[Dict]) -> List[Dict]:
    """Calculate compliance percentage per FESP"""
    results = []
    
    # Group items by FESP
    fesp_data = {}
    for item in items:
        f_id = item["fesp_id"]
        if f_id not in fesp_data:
            fesp_def = FESP_ITEMS.get(f_id, {})
            fesp_data[f_id] = {
                "id": f_id,
                "name": fesp_def.get("name", f_id),
                "number": fesp_def.get("number", 0),
                "earned": 0,
                "max": fesp_def.get("max_points", 1),
                "items": []
            }
        fesp_data[f_id]["earned"] += item["score"]
        fesp_data[f_id]["items"].append(item)
    
    # Calculate percentages
    for f_id, data in fesp_data.items():
        percentage = (data["earned"] / data["max"]) * 100 if data["max"] > 0 else 0
        level = calculate_compliance_level(percentage)
        results.append({
            "fesp_id": f_id,
            "fesp_name": data["name"],
            "fesp_number": data["number"],
            "earned_points": data["earned"],
            "max_points": data["max"],
            "compliance_percentage": round(percentage, 2),
            "level": level["label"],
            "color": level["color"]
        })
    
    # Sort by number
    results.sort(key=lambda x: x["fesp_number"])
    return results


def calculate_capability_scores(items: List[Dict]) -> List[Dict]:
    """Calculate compliance percentage per Institutional Capability"""
    results = []
    capabilities = get_capabilities()
    
    # We need to map item_id to capability
    all_defs = {it["id"]: it for it in get_all_items()}
    
    cap_stats = {cap: {"earned": 0, "max": 0} for cap in capabilities}
    
    for item in items:
        item_def = all_defs.get(item["item_id"])
        if item_def:
            cap = item_def["capability"]
            if cap in cap_stats:
                cap_stats[cap]["earned"] += item["score"]
                cap_stats[cap]["max"] += item_def["max_points"]
    
    for cap in capabilities:
        data = cap_stats[cap]
        percentage = (data["earned"] / data["max"]) * 100 if data["max"] > 0 else 0
        level = calculate_compliance_level(percentage)
        results.append({
            "capability": cap,
            "earned_points": data["earned"],
            "max_points": data["max"],
            "compliance_percentage": round(percentage, 2),
            "level": level["label"],
            "color": level["color"]
        })
    
    return results


def calculate_policy_cycle_scores(items: List[Dict]) -> List[Dict]:
    """Calculate compliance percentage per Policy Cycle stage"""
    results = []
    cycles = get_policy_cycles()
    
    # Policy cycle is defined at FESP level
    fesp_cycles = {f_id: f_def["policy_cycle"] for f_id, f_def in FESP_ITEMS.items()}
    all_defs = {it["id"]: it for it in get_all_items()}
    
    cycle_stats = {cycle: {"earned": 0, "max": 0} for cycle in cycles}
    
    for item in items:
        f_id = item["fesp_id"]
        cycle = fesp_cycles.get(f_id)
        item_def = all_defs.get(item["item_id"])
        
        if cycle and item_def:
            cycle_stats[cycle]["earned"] += item["score"]
            cycle_stats[cycle]["max"] += item_def["max_points"]
            
    for cycle in cycles:
        data = cycle_stats[cycle]
        percentage = (data["earned"] / data["max"]) * 100 if data["max"] > 0 else 0
        level = calculate_compliance_level(percentage)
        results.append({
            "cycle": cycle,
            "earned_points": data["earned"],
            "max_points": data["max"],
            "compliance_percentage": round(percentage, 2),
            "level": level["label"],
            "color": level["color"]
        })
        
    return results


def calculate_gaps(items: List[Dict]) -> List[Dict]:
    """Identify items with low scores as gaps"""
    gaps = []
    all_defs = {it["id"]: it for it in get_all_items()}
    
    for item in items:
        item_def = all_defs.get(item["item_id"])
        if not item_def: continue
        
        # Calculate percentage for this item
        percentage = (item["score"] / item_def["max_points"]) * 100 if item_def["max_points"] > 0 else 0
        
        if percentage < 60:  # Below "Intermedio"
            priority = "high" if percentage < 40 else "medium"
            gaps.append({
                "item_id": item["item_id"],
                "item_name": item_def["name"],
                "fesp_id": item["fesp_id"],
                "score": item["score"],
                "max_points": item_def["max_points"],
                "percentage": round(percentage, 2),
                "priority": priority,
                "recommendation": f"Fortalecer la capacidad institucional en '{item_def['name']}' mediante acciones específicas en el componente {item_def['capability']}."
            })
            
    # Sort by priority then percentage
    gaps.sort(key=lambda x: (0 if x["priority"] == "high" else 1, x["percentage"]))
    return gaps


def calculate_overall_compliance(items: List[Dict]) -> float:
    """Calculate the overall compliance percentage of the instrument"""
    total_earned = sum(item["score"] for item in items)
    total_max = get_total_max_points()
    
    if total_max == 0: return 0.0
    return round((total_earned / total_max) * 100, 2)
