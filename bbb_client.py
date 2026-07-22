"""Cliente BigBlueButton API (create / join / getRecordings)."""

from __future__ import annotations

import hashlib
import xml.etree.ElementTree as ET
from typing import Any, Dict, List, Optional
from urllib.parse import quote_plus, urlencode
from urllib.request import urlopen


def _checksum(api_call: str, query: str, secret: str) -> str:
    return hashlib.sha1(f"{api_call}{query}{secret}".encode("utf-8")).hexdigest()


def build_api_url(base_url: str, secret: str, api_call: str, params: Dict[str, Any]) -> str:
    base = base_url.rstrip("/") + "/"
    if not base.endswith("bigbluebutton/"):
        if "bigbluebutton" not in base:
            base = base.rstrip("/") + "/bigbluebutton/"
    api_base = base if base.endswith("api/") else base + "api/"
    query = urlencode({k: v for k, v in params.items() if v is not None}, quote_via=quote_plus)
    cs = _checksum(api_call, query, secret)
    return f"{api_base}{api_call}?{query}&checksum={cs}"


def call_api(base_url: str, secret: str, api_call: str, params: Dict[str, Any], timeout: int = 30) -> ET.Element:
    url = build_api_url(base_url, secret, api_call, params)
    with urlopen(url, timeout=timeout) as resp:
        raw = resp.read()
    root = ET.fromstring(raw)
    return_code = (root.findtext("returncode") or "").strip()
    if return_code != "SUCCESS":
        msg = (root.findtext("message") or root.findtext("messageKey") or "BBB error").strip()
        raise RuntimeError(msg)
    return root


def ensure_meeting(
    base_url: str,
    secret: str,
    meeting_id: str,
    name: str,
    attendee_pw: str = "ap",
    moderator_pw: str = "mp",
    record: bool = True,
) -> Dict[str, str]:
    """Crea la reunión si no existe. Devuelve passwords usados."""
    call_api(
        base_url,
        secret,
        "create",
        {
            "name": name,
            "meetingID": meeting_id,
            "attendeePW": attendee_pw,
            "moderatorPW": moderator_pw,
            "record": "true" if record else "false",
            "autoStartRecording": "true" if record else "false",
            "allowStartStopRecording": "true",
            "welcome": "Bienvenido a Metabolic Academy — clase en vivo",
        },
    )
    return {"attendee_pw": attendee_pw, "moderator_pw": moderator_pw}


def join_url(
    base_url: str,
    secret: str,
    meeting_id: str,
    full_name: str,
    password: str,
    user_id: Optional[str] = None,
    redirect: bool = True,
) -> str:
    params: Dict[str, Any] = {
        "fullName": full_name,
        "meetingID": meeting_id,
        "password": password,
        "redirect": "true" if redirect else "false",
    }
    if user_id:
        params["userID"] = user_id
    return build_api_url(base_url, secret, "join", params)


def list_recordings(base_url: str, secret: str, meeting_id: Optional[str] = None) -> List[Dict[str, Any]]:
    params: Dict[str, Any] = {}
    if meeting_id:
        params["meetingID"] = meeting_id
    root = call_api(base_url, secret, "getRecordings", params)
    out: List[Dict[str, Any]] = []
    recordings = root.find("recordings")
    if recordings is None:
        return out
    for rec in recordings.findall("recording"):
        rec_id = (rec.findtext("recordID") or "").strip()
        mid = (rec.findtext("meetingID") or "").strip()
        name = (rec.findtext("name") or "").strip()
        published = (rec.findtext("published") or "").strip().lower() == "true"
        playback_url = ""
        formats = rec.find("playback")
        if formats is not None:
            for fmt in formats.findall("format"):
                url = (fmt.findtext("url") or "").strip()
                if url:
                    playback_url = url
                    break
        if rec_id:
            out.append(
                {
                    "recording_id": rec_id,
                    "meeting_id": mid,
                    "name": name,
                    "published": published,
                    "playback_url": playback_url,
                }
            )
    return out
