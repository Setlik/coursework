from src.views import generate_json_response


def main():
    result_json = generate_json_response("23.12.2021 14:00:00")
    print(result_json)


if __name__ == "__main__":
    main()
