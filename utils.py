def abbreviate_name(full_name):
    parts = full_name.split()
    if len(parts) < 2:
        raise ValueError(f"Full name {full_name} must consist of three parts or two parts: last name, first name, and patronymic")

    if len(parts) == 2:
        last_name, first_name = parts
        abbreviated_name = f"{last_name} {first_name[0]}."
        return abbreviated_name
    if len(parts) == 3:
        last_name, first_name, patronymic = parts
        abbreviated_name = f"{last_name} {first_name[0]}.{patronymic[0]}."
        return abbreviated_name


def pretify_name(name):
    parts = name.split()
    if len(parts) < 2:
        raise ValueError(f"Name {name} must consist of three parts or two parts: last name, first name, and patronymic")
    parts = [part.strip() for part in parts]
    pretified_name = f"{parts[0]} {''.join(parts[1:])}"
    return pretified_name