

if __name__ == "__main__":
    for key, value in var.items():
        rounded_tuple = tuple(round(x, 3) for x in value)
        print(f"{key}: {rounded_tuple}")