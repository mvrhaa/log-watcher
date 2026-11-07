"""Format the text report."""


def format_section(title, rows):
    lines = [title]
    if not rows:
        lines.append("  none")
    for name, value in rows:
        lines.append(f"  {name:<20}{value}")
    return "\n".join(lines)


def format_warnings(suspicious, threshold):
    lines = ["Warnings"]
    if not suspicious:
        lines.append("  none")
    for ip, count in suspicious:
        lines.append(f"  WARNING: {ip} has {count} failed logins (threshold {threshold})")
    return "\n".join(lines)
