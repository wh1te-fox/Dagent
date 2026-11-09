"""Authentication and session management module with bcrypt password hashing."""
import threading
import time

import bcrypt

from services.database import (
    count_users,
    create_database,
    create_user,
    get_user_by_name,
    update_password,
)

MAX_ATTEMPTS = 5
LOCKOUT_SECONDS = 60
SESSION_DURATION = 8 * 60 * 60
SESSION_KEY = "dagent_sesion"

_attempts = {}
_attempts_lock = threading.Lock()
_dummy_hash = None


def hash_password(password):
    """Returns the bcrypt hash of a password (only the hash is stored)."""
    password_bytes = password.encode("utf-8")[:72]
    return bcrypt.hashpw(password_bytes, bcrypt.gensalt(rounds=12)).decode("utf-8")


def verify_password(password, password_hash):
    """Securely compares a password against its stored hash."""
    try:
        password_bytes = password.encode("utf-8")[:72]
        return bcrypt.checkpw(password_bytes, password_hash.encode("utf-8"))
    except (TypeError, ValueError):
        return False


def _get_dummy_hash():
    """Generates a dummy hash to equalize the work when the user does not exist."""
    global _dummy_hash
    if _dummy_hash is None:
        _dummy_hash = hash_password("verificacion-ficticia")
    return _dummy_hash


def _attempts_state(username):
    with _attempts_lock:
        return _attempts.get(username, (0, 0.0))


def _lockout_remaining(username):
    failures, unlock_at = _attempts_state(username)
    remaining = unlock_at - time.time()
    return int(remaining) + 1 if remaining > 0 else 0


def _record_attempt(username, correct):
    """Records the authentication result to apply a temporary lockout."""
    if correct:
        with _attempts_lock:
            _attempts.pop(username, None)
        return

    failures, unlock_at = _attempts_state(username)
    if time.time() >= unlock_at > 0:
        failures = 0

    with _attempts_lock:
        _attempts[username] = (failures + 1, unlock_at if time.time() < unlock_at else 0.0)

    failures, unlock_at = _attempts_state(username)
    if failures >= MAX_ATTEMPTS:
        with _attempts_lock:
            _attempts[username] = (MAX_ATTEMPTS, time.time() + LOCKOUT_SECONDS)


def initialize_users():
    """Prepares the users table and registers the default user on the first run.

    Returns True when it was necessary to create the default user.
    """
    create_database()
    if count_users() > 0:
        return False
    create_user("admin", hash_password("admin123"))
    return True


def authenticate(page, username, password):
    """Validates the credentials and opens the session of the correct user.

    Returns (success, message). The message never reveals whether the user exists
    and the work performed is the same in both cases (constant time).
    """
    username = (username or "").strip()
    password = password or ""

    if username:
        seconds = _lockout_remaining(username)
        if seconds > 0:
            return False, f"Demasiados intentos fallidos. Intente de nuevo en {seconds} s."

    record = get_user_by_name(username)
    target_hash = record[2] if record else _get_dummy_hash()
    matches = verify_password(password, target_hash)
    success = record is not None and matches

    _record_attempt(username, success)

    if not success:
        return False, "Usuario o contraseña incorrectos."

    _open_session(page, username)
    return True, "Acceso concedido"


def _get_storage(page):
    """Returns the session storage of the page (or the page itself as a fallback)."""
    storage = getattr(page, "session", None)
    if storage is not None and hasattr(storage, "get") and hasattr(storage, "set"):
        return storage
    return page


def _save_session(page, data):
    storage = _get_storage(page)
    if storage is page:
        setattr(page, SESSION_KEY, data)
    else:
        storage.set(SESSION_KEY, data)


def _read_session(page):
    storage = _get_storage(page)
    if storage is page:
        return getattr(page, SESSION_KEY, None)
    return storage.get(SESSION_KEY)


def _clear_session(page):
    storage = _get_storage(page)
    if storage is page:
        if hasattr(page, SESSION_KEY):
            delattr(page, SESSION_KEY)
    else:
        storage.set(SESSION_KEY, None)


def _open_session(page, username):
    """Registers the active session with its expiration time."""
    _save_session(page, {
        "usuario": username,
        "expira": time.time() + SESSION_DURATION,
    })


def active_session(page):
    """Returns the name of the user with a valid session, or None."""
    data = _read_session(page)
    if not isinstance(data, dict):
        return None

    username = data.get("usuario")
    if not username or time.time() >= data.get("expira", 0):
        _clear_session(page)
        return None

    if get_user_by_name(username) is None:
        _clear_session(page)
        return None

    return username


def _real_page(page):
    """Unwraps ContentProxy pages (layout sections) to the real ft.Page."""
    return getattr(page, "_page", page)


def logout(page):
    """Closes the current session and returns to the login screen."""
    real_page = _real_page(page)
    _clear_session(real_page)

    # Unmount the app shell so the login screen is rendered standalone
    # instead of nested inside the layout's content area.
    if hasattr(real_page, "_app_layout"):
        try:
            delattr(real_page, "_app_layout")
        except AttributeError:
            pass

    from views.login_view import login
    login(real_page)


def change_password(page, current, new):
    """Changes the password of the user with an active session."""
    username = active_session(page)
    if not username:
        return False, "Sesión no válida. Inicie sesión nuevamente."

    if not new or len(new) < 6:
        return False, "La nueva contraseña debe tener al menos 6 caracteres"

    record = get_user_by_name(username)
    if not record or not verify_password(current or "", record[2]):
        return False, "La contraseña actual es incorrecta"

    update_password(username, hash_password(new))
    return True, "Contraseña actualizada correctamente"
