#!/usr/bin/env python3
"""
Hotel Management Schedule System
A comprehensive CLI-based system for managing hotel room bookings,
staff schedules, and housekeeping tasks.
"""

import json
import os
from datetime import datetime, date, timedelta
from typing import Optional

# ─────────────────────────────────────────────
# DATA STORE  (in-memory; persisted to JSON)
# ─────────────────────────────────────────────
DATA_FILE = "hotel_data.json"

def load_data() -> dict:
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    # Default data
    return {
        "rooms": {
            "101": {"type": "Single",  "rate": 80,  "status": "Available"},
            "102": {"type": "Single",  "rate": 80,  "status": "Available"},
            "201": {"type": "Double",  "rate": 120, "status": "Available"},
            "202": {"type": "Double",  "rate": 120, "status": "Available"},
            "301": {"type": "Suite",   "rate": 220, "status": "Available"},
            "302": {"type": "Suite",   "rate": 220, "status": "Available"},
        },
        "bookings": {},          # booking_id -> booking dict
        "staff": {
            "S001": {"name": "Ali Hassan",    "role": "Front Desk",   "shift": "Morning"},
            "S002": {"name": "Sara Khan",     "role": "Front Desk",   "shift": "Evening"},
            "S003": {"name": "Usman Raza",    "role": "Housekeeping", "shift": "Morning"},
            "S004": {"name": "Fatima Malik",  "role": "Housekeeping", "shift": "Afternoon"},
            "S005": {"name": "Bilal Ahmed",   "role": "Security",     "shift": "Night"},
        },
        "housekeeping": {},      # room_no -> {"status": ..., "last_cleaned": ...}
        "next_booking_id": 1,
    }

def save_data(data: dict):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────
def clear():
    os.system("cls" if os.name == "nt" else "clear")

def header(title: str):
    width = 60
    print("\n" + "═" * width)
    print(f"  🏨  {title}")
    print("═" * width)

def pause():
    input("\n  Press Enter to continue...")

def today_str() -> str:
    return date.today().isoformat()

def date_from_str(s: str) -> Optional[date]:
    try:
        return date.fromisoformat(s.strip())
    except ValueError:
        return None

def nights_between(check_in: str, check_out: str) -> int:
    ci = date.fromisoformat(check_in)
    co = date.fromisoformat(check_out)
    return max((co - ci).days, 0)

# ─────────────────────────────────────────────
# ROOMS
# ─────────────────────────────────────────────
def view_rooms(data: dict):
    header("ROOM STATUS OVERVIEW")
    fmt = "  {:<6} {:<12} {:>10}  {}"
    print(fmt.format("Room", "Type", "Rate/Night", "Status"))
    print("  " + "─" * 48)
    for room_no, info in sorted(data["rooms"].items()):
        status = info["status"]
        icon = "✅" if status == "Available" else ("🛏️ " if status == "Occupied" else "🔧")
        print(fmt.format(room_no, info["type"], f"${info['rate']}", f"{icon} {status}"))

def update_room_status(data: dict):
    header("UPDATE ROOM STATUS")
    view_rooms(data)
    room_no = input("\n  Enter room number: ").strip()
    if room_no not in data["rooms"]:
        print("  ❌ Room not found.")
        return
    print("  Status options: 1) Available  2) Occupied  3) Maintenance")
    choice = input("  Select [1-3]: ").strip()
    statuses = {"1": "Available", "2": "Occupied", "3": "Maintenance"}
    if choice not in statuses:
        print("  ❌ Invalid choice.")
        return
    data["rooms"][room_no]["status"] = statuses[choice]
    save_data(data)
    print(f"  ✅ Room {room_no} status updated to '{statuses[choice]}'.")

# ─────────────────────────────────────────────
# BOOKINGS
# ─────────────────────────────────────────────
def make_booking(data: dict):
    header("NEW BOOKING")
    guest = input("  Guest name        : ").strip()
    if not guest:
        print("  ❌ Name cannot be empty.")
        return

    phone = input("  Phone number      : ").strip()

    # Show available rooms
    available = {k: v for k, v in data["rooms"].items() if v["status"] == "Available"}
    if not available:
        print("  ❌ No rooms available at the moment.")
        return

    print("\n  Available Rooms:")
    for r, info in sorted(available.items()):
        print(f"    Room {r} — {info['type']} — ${info['rate']}/night")

    room_no = input("\n  Room number       : ").strip()
    if room_no not in available:
        print("  ❌ Room not available or not found.")
        return

    ci_str = input(f"  Check-in  (YYYY-MM-DD, default today [{today_str()}]): ").strip()
    if not ci_str:
        ci_str = today_str()
    ci = date_from_str(ci_str)
    if not ci:
        print("  ❌ Invalid date format.")
        return

    co_str = input("  Check-out (YYYY-MM-DD): ").strip()
    co = date_from_str(co_str)
    if not co or co <= ci:
        print("  ❌ Check-out must be after check-in.")
        return

    nights = nights_between(ci_str, co_str)
    rate   = data["rooms"][room_no]["rate"]
    total  = nights * rate

    print(f"\n  📋 Booking Summary")
    print(f"     Guest     : {guest}")
    print(f"     Room      : {room_no} ({data['rooms'][room_no]['type']})")
    print(f"     Check-in  : {ci_str}")
    print(f"     Check-out : {co_str}")
    print(f"     Nights    : {nights}")
    print(f"     Total     : ${total}")

    confirm = input("\n  Confirm booking? [y/n]: ").strip().lower()
    if confirm != "y":
        print("  Booking cancelled.")
        return

    bid = f"BK{data['next_booking_id']:04d}"
    data["bookings"][bid] = {
        "guest": guest,
        "phone": phone,
        "room": room_no,
        "check_in": ci_str,
        "check_out": co_str,
        "nights": nights,
        "total": total,
        "status": "Active",
        "booked_on": today_str(),
    }
    data["rooms"][room_no]["status"] = "Occupied"
    data["next_booking_id"] += 1
    save_data(data)
    print(f"\n  ✅ Booking confirmed! ID: {bid}")

def view_bookings(data: dict, filter_status: str = "All"):
    header("BOOKING RECORDS")
    bookings = data["bookings"]
    if not bookings:
        print("  No bookings on record.")
        return

    fmt = "  {:<8} {:<18} {:<6} {:<12} {:<12} {:>8}  {}"
    print(fmt.format("ID", "Guest", "Room", "Check-In", "Check-Out", "Total", "Status"))
    print("  " + "─" * 76)
    for bid, b in sorted(bookings.items()):
        if filter_status != "All" and b["status"] != filter_status:
            continue
        icon = "🟢" if b["status"] == "Active" else ("🔴" if b["status"] == "Cancelled" else "🏁")
        print(fmt.format(bid, b["guest"][:17], b["room"],
                         b["check_in"], b["check_out"],
                         f"${b['total']}", f"{icon} {b['status']}"))

def cancel_booking(data: dict):
    header("CANCEL BOOKING")
    view_bookings(data, "Active")
    bid = input("\n  Enter Booking ID to cancel: ").strip().upper()
    if bid not in data["bookings"]:
        print("  ❌ Booking ID not found.")
        return
    if data["bookings"][bid]["status"] != "Active":
        print("  ❌ Booking is not active.")
        return
    confirm = input(f"  Cancel booking {bid} for {data['bookings'][bid]['guest']}? [y/n]: ").strip().lower()
    if confirm != "y":
        return
    room_no = data["bookings"][bid]["room"]
    data["bookings"][bid]["status"] = "Cancelled"
    data["rooms"][room_no]["status"] = "Available"
    save_data(data)
    print(f"  ✅ Booking {bid} cancelled. Room {room_no} is now available.")

def checkout_guest(data: dict):
    header("CHECK-OUT GUEST")
    view_bookings(data, "Active")
    bid = input("\n  Enter Booking ID for check-out: ").strip().upper()
    if bid not in data["bookings"]:
        print("  ❌ Booking ID not found.")
        return
    b = data["bookings"][bid]
    if b["status"] != "Active":
        print("  ❌ Booking is not active.")
        return

    print(f"\n  Guest    : {b['guest']}")
    print(f"  Room     : {b['room']}")
    print(f"  Total Due: ${b['total']}")
    confirm = input("\n  Confirm check-out? [y/n]: ").strip().lower()
    if confirm != "y":
        return
    data["bookings"][bid]["status"] = "Completed"
    data["rooms"][b["room"]]["status"] = "Available"
    # Mark room for housekeeping
    data["housekeeping"][b["room"]] = {
        "status": "Needs Cleaning",
        "last_cleaned": None,
        "guest": b["guest"],
    }
    save_data(data)
    print(f"  ✅ Check-out complete. Room {b['room']} queued for housekeeping.")

# ─────────────────────────────────────────────
# STAFF SCHEDULE
# ─────────────────────────────────────────────
SHIFT_TIMES = {
    "Morning":   "06:00 – 14:00",
    "Afternoon": "14:00 – 22:00",
    "Evening":   "16:00 – 00:00",
    "Night":     "22:00 – 06:00",
}

def view_staff(data: dict):
    header("STAFF SCHEDULE")
    fmt = "  {:<6} {:<20} {:<16} {:<12} {}"
    print(fmt.format("ID", "Name", "Role", "Shift", "Hours"))
    print("  " + "─" * 64)
    for sid, s in sorted(data["staff"].items()):
        hours = SHIFT_TIMES.get(s["shift"], "—")
        print(fmt.format(sid, s["name"], s["role"], s["shift"], hours))

def add_staff(data: dict):
    header("ADD STAFF MEMBER")
    name  = input("  Full name    : ").strip()
    role  = input("  Role         : ").strip()
    print("  Shifts: 1) Morning  2) Afternoon  3) Evening  4) Night")
    shift_map = {"1": "Morning", "2": "Afternoon", "3": "Evening", "4": "Night"}
    sc = input("  Select shift [1-4]: ").strip()
    if sc not in shift_map:
        print("  ❌ Invalid shift.")
        return
    shift = shift_map[sc]
    # Generate new ID
    existing_ids = [int(k[1:]) for k in data["staff"]]
    new_num = max(existing_ids, default=0) + 1
    sid = f"S{new_num:03d}"
    data["staff"][sid] = {"name": name, "role": role, "shift": shift}
    save_data(data)
    print(f"  ✅ Staff member {name} added with ID {sid}.")

def remove_staff(data: dict):
    header("REMOVE STAFF MEMBER")
    view_staff(data)
    sid = input("\n  Enter Staff ID to remove: ").strip().upper()
    if sid not in data["staff"]:
        print("  ❌ Staff ID not found.")
        return
    name = data["staff"][sid]["name"]
    confirm = input(f"  Remove {name}? [y/n]: ").strip().lower()
    if confirm != "y":
        return
    del data["staff"][sid]
    save_data(data)
    print(f"  ✅ {name} removed from staff records.")

def edit_staff_shift(data: dict):
    header("EDIT STAFF SHIFT")
    view_staff(data)
    sid = input("\n  Enter Staff ID: ").strip().upper()
    if sid not in data["staff"]:
        print("  ❌ Staff ID not found.")
        return
    print("  Shifts: 1) Morning  2) Afternoon  3) Evening  4) Night")
    shift_map = {"1": "Morning", "2": "Afternoon", "3": "Evening", "4": "Night"}
    sc = input("  New shift [1-4]: ").strip()
    if sc not in shift_map:
        print("  ❌ Invalid.")
        return
    data["staff"][sid]["shift"] = shift_map[sc]
    save_data(data)
    print(f"  ✅ Shift updated for {data['staff'][sid]['name']}.")

# ─────────────────────────────────────────────
# HOUSEKEEPING
# ─────────────────────────────────────────────
def view_housekeeping(data: dict):
    header("HOUSEKEEPING STATUS")
    hk = data["housekeeping"]
    if not hk:
        print("  No housekeeping tasks at the moment. ✨")
        return
    fmt = "  {:<6} {:<20} {}"
    print(fmt.format("Room", "Status", "Last Cleaned"))
    print("  " + "─" * 44)
    for room, info in sorted(hk.items()):
        lc = info.get("last_cleaned") or "Never"
        icon = "🧹" if info["status"] == "Needs Cleaning" else "✅"
        print(fmt.format(room, f"{icon} {info['status']}", lc))

def mark_room_cleaned(data: dict):
    header("MARK ROOM AS CLEANED")
    view_housekeeping(data)
    room_no = input("\n  Enter room number: ").strip()
    hk = data["housekeeping"]
    if room_no not in hk:
        print("  ❌ Room not in housekeeping queue.")
        return
    hk[room_no]["status"] = "Clean"
    hk[room_no]["last_cleaned"] = datetime.now().strftime("%Y-%m-%d %H:%M")
    data["rooms"][room_no]["status"] = "Available"
    save_data(data)
    print(f"  ✅ Room {room_no} marked as clean and set to Available.")

def add_housekeeping_task(data: dict):
    header("ADD HOUSEKEEPING TASK")
    view_rooms(data)
    room_no = input("\n  Enter room number: ").strip()
    if room_no not in data["rooms"]:
        print("  ❌ Room not found.")
        return
    data["housekeeping"][room_no] = {
        "status": "Needs Cleaning",
        "last_cleaned": data["housekeeping"].get(room_no, {}).get("last_cleaned"),
        "guest": "Manual Task",
    }
    save_data(data)
    print(f"  ✅ Housekeeping task added for room {room_no}.")

# ─────────────────────────────────────────────
# REPORTS
# ─────────────────────────────────────────────
def daily_report(data: dict):
    header("DAILY REPORT — " + today_str())
    rooms    = data["rooms"]
    bookings = data["bookings"]

    total_rooms    = len(rooms)
    occupied       = sum(1 for r in rooms.values() if r["status"] == "Occupied")
    available      = sum(1 for r in rooms.values() if r["status"] == "Available")
    maintenance    = sum(1 for r in rooms.values() if r["status"] == "Maintenance")
    occupancy_pct  = (occupied / total_rooms * 100) if total_rooms else 0

    active_bookings   = [b for b in bookings.values() if b["status"] == "Active"]
    checkins_today    = [b for b in active_bookings if b["check_in"] == today_str()]
    checkouts_today   = [b for b in bookings.values() if b["check_out"] == today_str()]
    revenue_today     = sum(b["total"] for b in bookings.values()
                            if b["status"] == "Completed" and b["check_out"] == today_str())

    print(f"\n  📊 Room Overview")
    print(f"     Total Rooms  : {total_rooms}")
    print(f"     Occupied     : {occupied}")
    print(f"     Available    : {available}")
    print(f"     Maintenance  : {maintenance}")
    print(f"     Occupancy    : {occupancy_pct:.1f}%")

    print(f"\n  📅 Today's Activity")
    print(f"     Check-Ins    : {len(checkins_today)}")
    print(f"     Check-Outs   : {len(checkouts_today)}")
    print(f"     Active Bookings: {len(active_bookings)}")
    print(f"     Revenue Today: ${revenue_today}")

    total_revenue = sum(b["total"] for b in bookings.values() if b["status"] == "Completed")
    print(f"\n  💰 All-Time Revenue : ${total_revenue}")

    print(f"\n  👥 Staff on Duty Today")
    morning_staff = [s["name"] for s in data["staff"].values() if s["shift"] in ("Morning", "Afternoon")]
    for name in morning_staff:
        print(f"     • {name}")

# ─────────────────────────────────────────────
# MENUS
# ─────────────────────────────────────────────
def booking_menu(data: dict):
    while True:
        header("BOOKING MANAGEMENT")
        print("  1) View All Bookings")
        print("  2) New Booking")
        print("  3) Cancel Booking")
        print("  4) Check-Out Guest")
        print("  0) Back")
        choice = input("\n  Select: ").strip()
        if   choice == "1": view_bookings(data); pause()
        elif choice == "2": make_booking(data); pause()
        elif choice == "3": cancel_booking(data); pause()
        elif choice == "4": checkout_guest(data); pause()
        elif choice == "0": break
        else: print("  ❌ Invalid choice.")

def staff_menu(data: dict):
    while True:
        header("STAFF SCHEDULE")
        print("  1) View Staff Schedule")
        print("  2) Add Staff Member")
        print("  3) Edit Staff Shift")
        print("  4) Remove Staff Member")
        print("  0) Back")
        choice = input("\n  Select: ").strip()
        if   choice == "1": view_staff(data); pause()
        elif choice == "2": add_staff(data); pause()
        elif choice == "3": edit_staff_shift(data); pause()
        elif choice == "4": remove_staff(data); pause()
        elif choice == "0": break
        else: print("  ❌ Invalid choice.")

def housekeeping_menu(data: dict):
    while True:
        header("HOUSEKEEPING")
        print("  1) View Housekeeping Tasks")
        print("  2) Mark Room as Cleaned")
        print("  3) Add Manual Task")
        print("  0) Back")
        choice = input("\n  Select: ").strip()
        if   choice == "1": view_housekeeping(data); pause()
        elif choice == "2": mark_room_cleaned(data); pause()
        elif choice == "3": add_housekeeping_task(data); pause()
        elif choice == "0": break
        else: print("  ❌ Invalid choice.")

def main_menu():
    data = load_data()
    while True:
        clear()
        print("\n" + "═" * 60)
        print("  🏨  HOTEL MANAGEMENT SCHEDULE SYSTEM")
        print(f"      {datetime.now().strftime('%A, %d %B %Y  %H:%M')}")
        print("═" * 60)
        print("  1) Room Status")
        print("  2) Bookings")
        print("  3) Staff Schedule")
        print("  4) Housekeeping")
        print("  5) Daily Report")
        print("  0) Exit")
        print("─" * 60)
        choice = input("  Select option: ").strip()

        if   choice == "1":
            clear(); view_rooms(data)
            print()
            sub = input("  Update a room status? [y/n]: ").strip().lower()
            if sub == "y":
                update_room_status(data)
            pause()
        elif choice == "2": booking_menu(data)
        elif choice == "3": staff_menu(data)
        elif choice == "4": housekeeping_menu(data)
        elif choice == "5": daily_report(data); pause()
        elif choice == "0":
            print("\n  👋 Goodbye! Have a great shift.\n")
            break
        else:
            print("  ❌ Invalid option. Try again.")

# ─────────────────────────────────────────────
if __name__ == "__main__":
    main_menu()
