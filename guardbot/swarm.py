"""Finds groups of new accounts that look like they belong together: same name pattern, same profile picture or accounts created within minutes of each other."""

import re
import unicodedata

CREATED_GAP = 600  # accounts created within ten minutes of the previous one count as one batch


def stem(name):
    """The letters of a name without digits, marks and separators, lower case. Names with fewer than three letters give None."""
    t = unicodedata.normalize("NFKD", name or "")
    t = "".join(ch for ch in t if not unicodedata.combining(ch)).casefold()
    t = re.sub(r"[^a-z]+", "", t)
    return t if len(t) >= 3 else None


def find_groups(entries, minimum):
    """Look for groups of at least `minimum` entries. Each entry is (member id, name, avatar hash or None, account creation timestamp).
    Returns a list of (kind, key, member ids) with kind name, avatar or created."""
    out = []
    by_name, by_avatar = {}, {}
    for uid, name, avatar, created in entries:
        s = stem(name)
        if s:
            by_name.setdefault(s, []).append(uid)
        if avatar:
            by_avatar.setdefault(avatar, []).append(uid)
    for kind, groups in (("name", by_name), ("avatar", by_avatar)):
        for key, ids in groups.items():
            if len(set(ids)) >= minimum:
                out.append((kind, key, sorted(set(ids))))
    ordered = sorted(entries, key=lambda e: e[3])
    batch = []
    for entry in ordered + [None]:
        if entry is not None and (not batch or entry[3] - batch[-1][3] <= CREATED_GAP):
            batch.append(entry)
            continue
        if len({b[0] for b in batch}) >= minimum:
            out.append(("created", str(int(batch[0][3])), sorted({b[0] for b in batch})))
        batch = [entry] if entry is not None else []
    return out
