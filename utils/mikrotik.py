import routeros_api

# ── Connection ──────────────────────────────────────────────────────────────

def get_connection(host='192.168.88.1', username='admin', password='', port=8728):
    """Create and return a RouterOS API connection."""
    connection = routeros_api.RouterOsApiPool(
        host,
        username=username,
        password=password,
        port=port,
        plaintext_login=True
    )
    return connection.get_api()


# ── Hotspot User Functions ───────────────────────────────────────────────────

def create_hotspot_user(api, username, password, profile='default', 
                         limit_uptime=None, limit_bytes_total=None, comment=None):
    """
    Create a new hotspot user.

    Args:
        api          : RouterOS API object
        username     : username for the hotspot user
        password     : password for the hotspot user
        profile      : hotspot user profile (default: 'default')
        limit_uptime : e.g. '01:00:00' for 1 hour (optional)
        limit_bytes_total : e.g. '104857600' for 100MB (optional)
        comment      : optional comment/note
    """
    hotspot_users = api.get_resource('/ip/hotspot/user')

    params = {
        'name': username,
        'password': password,
        'profile': profile,
    }
    if limit_uptime:
        params['limit-uptime'] = limit_uptime
    if limit_bytes_total:
        params['limit-bytes-total'] = str(limit_bytes_total)
    if comment:
        params['comment'] = comment

    hotspot_users.add(**params)
    print(f"[+] Hotspot user '{username}' created successfully.")


def remove_hotspot_user(api, username):
    """
    Remove a hotspot user by username.

    Args:
        api      : RouterOS API object
        username : username of the hotspot user to remove
    """
    hotspot_users = api.get_resource('/ip/hotspot/user')
    users = hotspot_users.get(name=username)

    if not users:
        print(f"[-] User '{username}' not found.")
        return False

    user_id = users[0]['id']
    hotspot_users.remove(id=user_id)
    print(f"[+] Hotspot user '{username}' removed successfully.")
    return True


def list_hotspot_users(api):
    """
    List all hotspot users with their details.

    Returns:
        list of dicts with user details
    """
    hotspot_users = api.get_resource('/ip/hotspot/user')
    users = hotspot_users.get()

    if not users:
        print("No hotspot users found.")
        return []

    print(f"\n{'Username':<20} {'Profile':<15} {'Uptime Limit':<15} {'Bytes Limit':<15} {'Comment'}")
    print("-" * 80)
    for user in users:
        print(
            f"{user.get('name',''):<20} "
            f"{user.get('profile',''):<15} "
            f"{user.get('limit-uptime', 'unlimited'):<15} "
            f"{user.get('limit-bytes-total', 'unlimited'):<15} "
            f"{user.get('comment', '')}"
        )

    return users


def list_active_hotspot_users(api):
    """
    List currently active/connected hotspot users with session details
    including time remaining if a limit is set.

    Returns:
        list of dicts with active session details
    """
    active = api.get_resource('/ip/hotspot/active')
    sessions = active.get()

    if not sessions:
        print("No active hotspot sessions.")
        return []

    print(f"\n{'Username':<20} {'IP':<16} {'MAC':<20} {'Uptime':<12} {'Session Timeout'}")
    print("-" * 85)
    for s in sessions:
        print(
            f"{s.get('user',''):<20} "
            f"{s.get('address',''):<16} "
            f"{s.get('mac-address',''):<20} "
            f"{s.get('uptime',''):<12} "
            f"{s.get('session-time-left', 'unlimited')}"
        )

    return sessions


def get_hotspot_user(api, username):
    """
    Get full details of a specific hotspot user.

    Returns:
        dict with user details, or None if not found
    """
    hotspot_users = api.get_resource('/ip/hotspot/user')
    users = hotspot_users.get(name=username)

    if not users:
        print(f"[-] User '{username}' not found.")
        return None

    user = users[0]
    print(f"\n── Details for '{username}' ──")
    for key, value in user.items():
        print(f"  {key:<25}: {value}")
    return user


# ── Example Usage ────────────────────────────────────────────────────────────

if __name__ == '__main__':
    api = get_connection('192.168.88.1', username='admin', password='Mmxsp65$$$')

    # Create a user with a 1-hour time limit
    create_hotspot_user(api, 'john', 'pass123', profile='default', limit_uptime='01:00:00')

    # Create a user with a 100MB data limit
    create_hotspot_user(api, 'jane', 'pass456', limit_bytes_total=100 * 1024 * 1024)

    # List all users
    list_hotspot_users(api)

    # Get a specific user's details
    get_hotspot_user(api, 'john')

    # List active sessions (with time remaining)
    list_active_hotspot_users(api)

    # Remove a user
    remove_hotspot_user(api, 'john')