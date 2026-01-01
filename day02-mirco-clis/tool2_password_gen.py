import argparse
import secrets
import string


def build_parser():
    p = argparse.ArgumentParser(description="Generate secure passwords.")
    p.add_argument("--length", type=int, default=16, help="Password length (default: 16)")
    p.add_argument("--count", type=int, default=5, help="How many passwords to generate (default: 5)")
    p.add_argument("--no-symbols", action="store_true", help="Disable symbols")
    return p


def generate_password(length: int, use_symbols: bool) -> str:
    lowers = string.ascii_lowercase
    uppers = string.ascii_uppercase
    digits = string.digits
    symbols = "!@#$%^&*()-_=+[]{};:,.?/"

    min_length = 4 if use_symbols else 3
    if length < min_length:
        raise ValueError(f"Password length must be at least {min_length}")

    chars = []
    chars.append(secrets.choice(lowers))
    chars.append(secrets.choice(uppers))
    chars.append(secrets.choice(digits))
    if use_symbols:
        chars.append(secrets.choice(symbols))

    # 4) fill remaining characters from allowed pool
    # (you implement)
    pool = lowers + uppers + digits
    if use_symbols:
        pool += symbols

    while len(chars) < length:
        chars.append(secrets.choice(pool))

    # 5) shuffle to remove predictability
    # (you implement)
    secrets.SystemRandom().shuffle(chars)

    # 6) return as string
    # (you implement)
    return "".join(chars)


def main(argv=None):
    args = build_parser().parse_args(argv)
    use_symbols = not args.no_symbols

    # validate count and length are sane
    if args.length <= 0:
        raise SystemExit("ERROR: --length must be a positive integer")
    if args.count <= 0:
        raise SystemExit("ERROR: --count must be a positive integer")

    try:
        for _ in range(args.count):
            print(generate_password(args.length, use_symbols))
    except ValueError as e:
        raise SystemExit(f"ERROR: {e}")



if __name__ == "__main__":
    main()

