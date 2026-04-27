def generate_company_code(name):
    ignore = ["LTD", "LIMITED", "PLC"]

    words = name.upper().split()
    words = [w for w in words if w not in ignore]

    code = "-".join(words)

    if len(code) <= 50:
        return code

    # 🔥 smart trimming word by word
    result = []
    total_length = 0

    for w in words:
        extra = len(w) + (1 if result else 0)  # dash

        if total_length + extra > 50:
            break

        result.append(w)
        total_length += extra

    return "-".join(result)